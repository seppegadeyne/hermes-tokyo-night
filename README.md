# Tokyo Night for Hermes

A native **skin + desktop theme plugin**, with deep navy, lavender, cyan and rose
colors. No core patches, monkeypatches, background hooks, network calls or remote
fonts. MIT licensed. This repository is an independent community package, not an
upstream Hermes product.

## What gets installed

| Part | Delivery | Activation |
| --- | --- | --- |
| Python plugin | `plugin.yaml` + `__init__.py` | Registers only `hermes tokyo-night install/uninstall` when enabled |
| Native skin | `skins/tokyo-night.yaml` | Explicit installer copies it into the selected home's `skins/`; then select it |
| Native desktop plugin | `desktop/plugin.js` | Hermes materializes the unified desktop half; enable it separately in Capabilities → Plugins |

These are **not web-dashboard plugins**. The Python plugin does not render a UI.
The native desktop plugin contributes a `DesktopTheme` through `THEMES_AREA` and
a small **Tokyo Night · Dark** titlebar button through `TITLEBAR_AREAS.right`.
Only documented `@hermes/plugin-sdk` and React APIs are used in runtime code.

## Install

Requires a recent Hermes with unified `desktop/plugin.js` delivery, `THEMES_AREA`,
`useTheme`, and Python `ctx.register_cli_command`. The examined upstream reference
is commit `8863b36fd663c50d3b794c48a6505ff6c7c3c91b`; see [verification](VERIFICATION.md).
There is no claimed minimum numbered Hermes release.

From a local clone (no publication required):

```sh
hermes plugins install "file://$(pwd)" --enable --no-deps
hermes tokyo-night install
hermes config set display.skin tokyo-night
```

Run the first command from this repository root. After publication, the standard
remote equivalent is `hermes plugins install OWNER/REPOSITORY --enable --no-deps`.
Replace `OWNER/REPOSITORY` with the actual published repository; for reproducibility
add `--ref FULL_40_CHARACTER_COMMIT_SHA`. No pip or npm dependencies are needed.

If you already have a personal `tokyo-night.yaml`, installation refuses to clobber
it. To explicitly back it up and replace it:

```sh
hermes tokyo-night install --replace
```

In Desktop, rescan plugins if needed, enable **Tokyo Night**, then click
**Tokyo Night · Dark** once for the desired profile. This selects the theme and
sets **dark**, using the host's own per-profile persistence. Alternatively select
Tokyo Night and Dark individually in Appearance. Python enablement and desktop
enablement are deliberately separate security/user-consent switches.

For a named profile use `hermes --profile NAME ...` on each CLI command, or set
`HERMES_HOME` explicitly. Desktop plugins are app-level (one local copy across
profiles), whereas the skin and appearance selections are profile-scoped. For a
remote gateway, install the Python/skin part on that backend and the desktop half
locally using Desktop's Install from Git; a remote directory is not a local disk
plugin source.

### Dark default and user choice

**Dark is the default of the explicit apply button, not a forced global default.**
Nothing selects a theme on load, reconnect, enable, reload, profile switch or
upgrade. Subsequent light/dark/system and theme choices remain owned by Hermes.
The regular theme picker changes the theme only, not mode. Light mode uses the
host's synthesized light variant, not a separately designed Tokyo Night palette.

The supported SDK does not expose an "unset appearance preference" test or a
first-launch default override. Automatically calling `setMode('dark')` on mount
would overwrite legitimate choices. This package intentionally does not do that.
Fresh profiles retain Hermes' upstream defaults until you apply the theme.

## Uninstall / restore

First select another desktop theme/mode and, if needed, another CLI skin:

```sh
hermes config set display.skin default
hermes tokyo-night uninstall
hermes plugins remove hermes-tokyo-night
```

Run skin uninstall **before** removing the package. Desktop removes its managed
copy on rescan/reconciliation when the source package disappears. Disable the
Desktop plugin first for immediate contribution removal. A manually copied,
unmarked standalone desktop plugin is not package-managed; remove that specific
folder yourself instead.

The skin installer keeps a receipt in
`$HERMES_HOME/theme-packages/hermes-tokyo-night.json`. It restores the exact prior
file when `--replace` was used, otherwise removes only its installed skin.
Changed or missing managed files cause a refusal rather than data loss. Keep the
receipt until removal completes. Install/remove operations are intended to run
serially; an interruption between receipt and asset writes fails closed and may
need manual recovery using the receipt's base64 `previous` bytes. Config is never
rewritten by the asset installer, including during uninstall.

Standalone asset-only fallback (does not install the desktop/Python plugins):

```sh
python3 installer.py install --home /path/to/hermes-home
python3 installer.py uninstall --home /path/to/hermes-home
```

## Palette and patch migration

The desktop color tokens preserve the custom Tokyo Night preset exactly. The
native YAML preserves the existing custom CLI colors, adds an explicit navy
background and semantic text/tool/syntax colors, and deliberately leaves out
personal branding, banners and spinner text. The desktop font stack prefers a
locally installed JetBrains Mono; unlike the former preset it does not download
Google Fonts. Install that font locally for matching typography.

**The personal core styling patch can be removed after the package is installed,
enabled and Tokyo Night + Dark are explicitly selected.** Do not remove it before
migrating the currently selected profile. The package replaces the palette, but
not the patch's unconditional fallback for *all future/unconfigured profiles*.
A core-built-in Tokyo Night with the same name may take precedence while the old
patch is still present; assess plugin palette behavior on an unpatched build.
This repository does not revert any core commits or modify existing preferences.

## Development and tests

```sh
python3 -m unittest discover -s tests -v
node --test tests/*.test.mjs
export HERMES_REPO=/path/to/hermes-agent
"$HERMES_REPO/.venv/bin/python" tests/hermes-integration.py
node --import "$HERMES_REPO/node_modules/tsx/dist/loader.mjs" tests/desktop-integration.mjs
hermes plugins validate .
```

The integration scripts create temporary homes and delete them afterwards. The
Python integration uses the checkout's real CLI, plugin loader and native skin
loader. The desktop integration uses the real unified-package materializer,
uninstall reconciler and theme validator. JS unit tests explicitly use a small
SDK harness; they are not presented as a rendered Electron acceptance test.

## References

- [Python plugins](https://hermes-agent.nousresearch.com/docs/user-guide/features/plugins)
- [Desktop SDK and unified packaging](https://hermes-agent.nousresearch.com/docs/developer-guide/desktop-plugin-sdk)
- Runtime contracts inspected: `hermes_cli/skin_engine.py`,
  `hermes_cli/plugins_cmd.py`, `apps/desktop/electron/desktop-plugins-root.ts`,
  `apps/desktop/src/themes/types.ts`, `apps/desktop/src/contrib/runtime-loader.ts`.

Python plugins can ship data files, but neither the documented `ctx` API nor the
examined native installer registers/copies skin assets automatically. That is why
this package has one explicit asset command rather than an undocumented install
hook or a load-time filesystem side effect.
