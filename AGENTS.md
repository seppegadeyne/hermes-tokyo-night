# Development conventions

Use documented Hermes Python `ctx` and desktop `@hermes/plugin-sdk` APIs only.
Never patch core, touch real profiles during tests, or force appearance on load.
Keep the desktop entry plain ESM with SDK/React imports only. Keep all palette
values explicit. No private paths, credentials, telemetry, or remote font loads.
Run `python3 -m unittest discover -s tests` and `node --test tests/*.test.mjs`.
Integration tests require a Hermes checkout supplied explicitly; use temporary
HERMES_HOME directories and its project interpreter/runner.
