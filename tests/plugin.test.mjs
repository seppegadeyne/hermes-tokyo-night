import { test } from 'node:test'
import assert from 'node:assert/strict'
import { readFile } from 'node:fs/promises'
// Unit harness, NOT the actual Electron runtime loader.
const calls = []
globalThis.__tokyoTest = { calls }
const sdk = `export const THEMES_AREA='themes'; export const TITLEBAR_AREAS={right:'titleBar.right'};
export const Button='button'; export function useTheme(){return {
setTheme:n=>globalThis.__tokyoTest.calls.push(['theme',n]),
setMode:n=>globalThis.__tokyoTest.calls.push(['mode',n])}}`
const url = s => 'data:text/javascript;base64,' + Buffer.from(s).toString('base64')
const source = await readFile(new URL('../desktop/plugin.js', import.meta.url), 'utf8')
const mod = await import(url(source.replace("'@hermes/plugin-sdk'", JSON.stringify(url(sdk)))
  .replace("'react/jsx-runtime'", JSON.stringify(url('export const jsx=(type,props)=>({type,props})')))))
test('registers theme without selecting on load/reload', () => {
  const contributions = []
  mod.default.register({ register: c => contributions.push(c) })
  mod.default.register({ register: c => contributions.push(c) })
  assert.equal(mod.default.defaultEnabled, false)
  assert.equal(contributions[0].area, 'themes')
  assert.equal(contributions[0].data, mod.theme)
  assert.deepEqual(calls, [])
  for (const value of Object.values(mod.theme.colors)) assert.match(value, /^#[0-9a-f]{6}$/)
  assert.equal(mod.theme.colors.background, '#1a1b26')
  assert.equal(mod.theme.colors.accent, '#2ac3de')
})
test('explicit apply selects dark; rerenders leave later choices alone', () => {
  const button = mod.SelectTokyoNight()
  assert.deepEqual(calls, [])
  button.props.onClick()
  assert.deepEqual(calls, [['theme','tokyo-night'], ['mode','dark']])
  calls.length=0
  mod.SelectTokyoNight()
  mod.default.register({register:()=>{}})
  assert.deepEqual(calls, [])
})
