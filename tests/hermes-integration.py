"""Real CLI install, discovery, command dispatch and skin loader, isolated homes.
Run with the Hermes checkout's Python and set HERMES_REPO.
"""
import os
from pathlib import Path
import subprocess
import sys
import tempfile

repo = Path(os.environ['HERMES_REPO']).resolve()
package = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='tokyo-hermes-') as tmp:
    for name in ('a', 'b'):
        home = Path(tmp) / name
        home.mkdir()
        env = {**os.environ, 'HERMES_HOME': str(home), 'HERMES_ENABLE_PROJECT_PLUGINS': 'false'}
        def cli(*args):
            subprocess.run([sys.executable, '-m', 'hermes_cli.main', *args], cwd=repo, env=env, check=True)
        cli('plugins', 'install', package.as_uri(), '--enable', '--no-deps')
        assert not (home / 'skins/tokyo-night.yaml').exists(), 'install must not silently copy skins'
        cli('tokyo-night', 'install')
        cli('config', 'set', 'display.skin', 'tokyo-night')
        subprocess.run([sys.executable, '-c', '''
from hermes_cli.skin_engine import load_skin, list_skins
s = load_skin('tokyo-night')
assert s.name == 'tokyo-night'
assert s.colors['background'] == '#1A1B26'
assert s.colors['ui_accent'] == '#7AA2F7'
assert s.branding['agent_name'] == 'Hermes Agent'
assert any(x['name'] == 'tokyo-night' for x in list_skins())
print('PASS: real native skin loader and neutral branding')
'''], cwd=repo, env=env, check=True)
        cli('config', 'set', 'display.skin', 'default')
        config = (home / 'config.yaml').read_bytes()
        cli('tokyo-night', 'install')
        assert (home / 'config.yaml').read_bytes() == config, 'reinstall changed later selection'
        cli('tokyo-night', 'uninstall')
        assert not (home / 'skins/tokyo-night.yaml').exists()
        cli('plugins', 'remove', 'hermes-tokyo-night')
        assert not (home / 'plugins/hermes-tokyo-night').exists()
print('PASS: standard install/remove and real plugin command discovery in two isolated homes')
