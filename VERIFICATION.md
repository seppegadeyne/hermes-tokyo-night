# Verification

## Tested environment

Linux/native Wayland; Node 22.23.2; real Electron and Python backend from
unmodified upstream `8863b36fd663c50d3b794c48a6505ff6c7c3c91b`.
The runtime plugin tested is package revision
`5175b32c4b900144fb4ff3da73eeb6b5567a59c1`; subsequent documentation-only changes
do not alter that code. Acceptance tests used isolated homes and userdata.

## Unit and native integration results

- Python unittest suite: **5 passed**. Idempotence, unchanged configuration,
  collision refusal, byte-exact backup restoration, user-edit refusal, separate
  homes, and symlink refusal.
- Node unit suite: **2 passed**. These use an explicitly labeled SDK/React harness,
  not a renderer, to check contribution shape and explicit-only selection.
- `hermes plugins validate`: passed, security scan safe, desktop entry stays
  inside the supported SDK surface.
- Actual standard CLI installation, discovery, registered command, native skin
  loading, selection, later-choice retention and removal: passed in two temporary
  homes, including an unpatched upstream checkout.
- Actual Electron-side unified-package materialization, byte comparison, package
  marker, idempotence, real theme validation and uninstall reconciliation: passed.

## Real rendered Desktop acceptance — passed

An isolated production renderer build was served locally to native-Wayland
Electron with dev CDP enabled, backed by the real Python service. No mocked
backend, direct theme-store calls or localStorage writes were used.

1. Chromium's debugger confirmed the actual plugin module was blob-loaded through
   Hermes' runtime loader and SDK bridges.
2. Enabling the plugin through Capabilities → Plugins mounted the titlebar button
   without changing the current theme.
3. Clicking **Tokyo Night · Dark** selected `tokyo-night` and `dark`. Computed CSS
   showed primary `#7aa2f7`, accent `#2ac3de`, and the expected navy background seed.
4. A full renderer reload retained the theme, dark mode and button.
5. A subsequent explicit **Light** choice survived plugin disable/re-enable,
   the actual **Reload desktop plugins** command, and another renderer reload.
6. A trusted CDP pointer click on the rendered titlebar button changed Light back
   to Dark and persisted the choice through Hermes' normal storage.

The host mixes palette seeds into its surfaces; the computed body background is
not claimed to equal the raw background seed. Screenshots/aesthetic approval and
cross-platform visual parity were not assessed.

## Limits

No released minimum version has been established. Native Wayland/Linux is the
only rendered platform tested. Tests did not modify core source or restart a
user's live gateway/Desktop. An initial dev-server attempt stalled during large
dependency transforms and selected Python without dotenv; the successful run
used the supported Python override, Node 22 and a production renderer build.

Fresh-profile/global default overrides are intentionally not reproduced: use
the explicit Tokyo Night · Dark action for each profile. No automatic theme or
mode selection occurs on load, reload or profile switch.
