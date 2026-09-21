"""Explicit, reversible native skin installation. Python standard library only."""
import argparse
import base64
import hashlib
import json
import os
from pathlib import Path
import tempfile

ASSET = Path(__file__).parent / "skins" / "tokyo-night.yaml"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def atomic_write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=".tokyo-night-", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def paths(home):
    home = Path(home).expanduser().resolve()
    target = home / "skins" / "tokyo-night.yaml"
    receipt = home / "theme-packages" / "hermes-tokyo-night.json"
    # Do not follow symlinks out of the chosen profile, including directory links.
    for path in (target, receipt):
        if path.is_symlink() or not path.resolve().is_relative_to(home):
            raise RuntimeError(f"Refusing symlink or escaped target: {path}")
    return target, receipt


def install(home, replace=False):
    target, receipt = paths(home)
    data = ASSET.read_bytes()
    if receipt.exists():
        state = json.loads(receipt.read_text())
        if not target.exists() or digest(target.read_bytes()) != state["installed_sha256"]:
            raise RuntimeError("Installed skin was edited or removed; refusing to overwrite it.")
    else:
        previous = target.read_bytes() if target.exists() else None
        if previous is not None and not replace:
            raise RuntimeError("Skin already exists; use --replace to back it up explicitly.")
        state = {"previous": base64.b64encode(previous).decode() if previous is not None else None}
    if target.exists() and target.read_bytes() == data and receipt.exists():
        return "Already installed; selection unchanged."
    # Receipt first: interruption fails closed on the next run rather than destroying data.
    state["installed_sha256"] = digest(data)
    atomic_write(receipt, (json.dumps(state, indent=2) + "\n").encode())
    atomic_write(target, data)
    if target.read_bytes() != data:
        raise RuntimeError("Skin verification failed")
    return "Skin installed; selection unchanged. Use: hermes config set display.skin tokyo-night"


def uninstall(home):
    target, receipt = paths(home)
    if not receipt.exists():
        return "No managed skin installation; nothing removed."
    state = json.loads(receipt.read_text())
    if not target.exists() or digest(target.read_bytes()) != state["installed_sha256"]:
        raise RuntimeError("Installed skin was edited or removed; preserve it and resolve the receipt manually.")
    if state["previous"] is None:
        target.unlink()
    else:
        original = base64.b64decode(state["previous"], validate=True)
        atomic_write(target, original)
        if target.read_bytes() != original:
            raise RuntimeError("Restore verification failed")
    receipt.unlink()
    return "Managed skin removed (previous file restored if present); selection unchanged."


def configure_parser(parser):
    parser.add_argument("action", choices=("install", "uninstall"))
    parser.add_argument("--home", help="Explicit Hermes home; otherwise active profile/HERMES_HOME")
    parser.add_argument("--replace", action="store_true", help="Back up an existing unmanaged skin")


def run(args):
    if args.home:
        home = Path(args.home)
    else:
        # Hermes supplies profile context; standalone use also honors HERMES_HOME.
        try:
            from hermes_constants import get_hermes_home
        except ImportError:
            home = Path(os.environ.get("HERMES_HOME", str(Path.home() / ".hermes")))
        else:
            home = get_hermes_home()
    if args.action == "uninstall" and args.replace:
        raise RuntimeError("--replace is only valid for install")
    print(install(home, args.replace) if args.action == "install" else uninstall(home))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    configure_parser(parser)
    try:
        run(parser.parse_args())
    except (OSError, ValueError, RuntimeError, KeyError) as error:
        parser.exit(1, f"Tokyo Night: {error}\n")
