# Verification

## Tested environment

Linux; Node 25.2.1; Hermes checkout at `7950876f0ba3` (a local patch-stack
checkout). SDK export availability was also checked at the pinned upstream
reference `8863b36fd663c50d3b794c48a6505ff6c7c3c91b`. Tests did not alter core
source, publish a repository, install into a real profile, or restart a gateway.

## Executed results

- `python3 -m unittest discover -s tests -v`: **5 passed**. Idempotence,
  unchanged configuration, collision refusal + byte-exact backup restoration,
  user-edit refusal, separate homes, symlink refusal.
- `node --test tests/*.test.mjs`: **2 passed**. Plain ESM evaluation, native
  contribution shape, no automatic selection on registration/reload, explicit
  dark apply, and no later rerender reset. The SDK/React in these unit tests is a
  deliberately labeled harness, not a live renderer.
- `hermes plugins validate <package>`: **Validation passed**, including isolated
  Python registration/capability probe, security scan **safe**, and desktop
  **stays inside the plugin SDK surface**.
- `tests/hermes-integration.py` with Hermes' own `.venv/bin/python`: **passed in
  two isolated temporary homes**. Real standard `plugins install file://…
  --enable --no-deps`; discovery and CLI dispatch to `tokyo-night install`;
  actual native `load_skin` / `list_skins`; safe config selection; user changes
  to `default` survive reinstall; skin uninstall and standard plugin remove
  verified by filesystem reads.
- `tests/desktop-integration.mjs` with the checkout's `tsx` loader: **passed**.
  Real Electron-side `materializeDesktopHalf`, source/target byte comparison,
  package marker, idempotence, real `isValidTheme`, and
  `reconcileUnifiedDesktopHalves` cleanup after package removal.

## Not claimed

No screenshot or rendered Electron acceptance test was performed. The browser
blob-import runtime loader and a mounted `ThemeProvider` were not exercised by
this package's tests. Materialization and native ESM evaluation are distinct
from browser loading. The exact current-window rendering, titlebar button,
light synthesis, and profile-persistence UX should receive a live acceptance
check during the separately authorized installation. Existing core Tokyo Night
presets can mask same-name plugin palette resolution until that patch is removed.

No test was run against a released minimum version or a completely unpatched
upstream checkout. No visual pixel-perfect claim is made; the host derives
additional UI tokens and may enforce contrast. The old remote font request is
intentionally omitted. Fresh-profile/global default overrides are explicitly
not reproduced: use the one-time Tokyo Night · Dark action for each profile.
