// Run with the Hermes checkout's tsx loader; no core files are modified.
import assert from 'node:assert/strict'
import fs from 'node:fs/promises'
import os from 'node:os'
import path from 'node:path'
import { pathToFileURL, fileURLToPath } from 'node:url'
const repo = process.env.HERMES_REPO
if (!repo) throw new Error('Set HERMES_REPO to a Hermes checkout')
const { materializeDesktopHalf, reconcileUnifiedDesktopHalves } = await import(pathToFileURL(path.join(repo, 'apps/desktop/electron/desktop-plugins-root.ts')))
const { isValidTheme } = await import(pathToFileURL(path.join(repo, 'apps/desktop/src/themes/types.ts')))
const home = await fs.mkdtemp(path.join(os.tmpdir(), 'tokyo-desktop-'))
try {
  const pkg = path.join(home, 'plugins/hermes-tokyo-night')
  const root = path.join(home, 'desktop-plugins')
  const sourceDir = fileURLToPath(new URL('../desktop', import.meta.url))
  await fs.mkdir(pkg, { recursive: true })
  await fs.cp(sourceDir, path.join(pkg, 'desktop'), { recursive: true })
  const target = await materializeDesktopHalf(pkg, root)
  assert.equal(target, path.join(root, 'hermes-tokyo-night'))
  const source = await fs.readFile(path.join(target, 'plugin.js'), 'utf8')
  assert.equal(source, await fs.readFile(path.join(sourceDir, 'plugin.js'), 'utf8'))
  assert.equal(JSON.parse(await fs.readFile(path.join(target, '.hermes-package.json'))).package, 'hermes-tokyo-night')
  assert.equal(await materializeDesktopHalf(pkg, root), null)
  // Evaluate the actual ESM payload with a minimal SDK harness, then apply the
  // actual host theme validator. This is not the browser blob-import loader.
  const dataURL = text => 'data:text/javascript;base64,' + Buffer.from(text).toString('base64')
  const sdk = dataURL('export const THEMES_AREA="themes", TITLEBAR_AREAS={right:"right"}, Button="button", useTheme=()=>{throw Error("unexpected theme selection")};')
  const react = dataURL('export const jsx=(type,props)=>({type,props});')
  const mod = await import(dataURL(source.replace("'@hermes/plugin-sdk'", JSON.stringify(sdk)).replace("'react/jsx-runtime'", JSON.stringify(react))))
  const contributions = []
  mod.default.register({register: c => contributions.push(c)})
  assert.ok(isValidTheme(contributions[0].data))
  await fs.rm(pkg, { recursive: true })
  await reconcileUnifiedDesktopHalves(home, root)
  await assert.rejects(fs.stat(target), { code: 'ENOENT' })
  console.log('PASS: real desktop materialization, idempotence, host theme validation, uninstall reconciliation')
} finally {
  await fs.rm(home, { recursive: true, force: true })
}
