import { THEMES_AREA, TITLEBAR_AREAS, Button, useTheme } from '@hermes/plugin-sdk'
import { jsx } from 'react/jsx-runtime'

// Exact custom desktop palette; a native theme, not a global CSS override.
export const theme = {
  name: 'tokyo-night',
  label: 'Tokyo Night',
  description: 'Deep navy with lavender, cyan, and rose accents',
  colors: {
    background: '#1a1b26', foreground: '#a9b1d6',
    card: '#1f2335', cardForeground: '#a9b1d6',
    muted: '#24283b', mutedForeground: '#565f89',
    popover: '#1f2335', popoverForeground: '#a9b1d6',
    primary: '#7aa2f7', primaryForeground: '#1a1b26',
    secondary: '#292e42', secondaryForeground: '#a9b1d6',
    accent: '#2ac3de', accentForeground: '#1a1b26',
    border: '#2f334d', input: '#2f334d', ring: '#bb9af7',
    midground: '#7aa2f7', destructive: '#f7768e',
    destructiveForeground: '#1a1b26', sidebarBackground: '#16161e',
    sidebarBorder: '#2f334d', userBubble: '#24283b', userBubbleBorder: '#2f334d'
  },
  typography: { fontMono: '"JetBrains Mono", ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace' }
}

export function SelectTokyoNight() {
  const { setTheme, setMode } = useTheme()
  return jsx(Button, {
    size: 'sm', variant: 'ghost',
    title: 'Select Tokyo Night and dark mode for this profile',
    onClick: () => { setTheme(theme.name); setMode('dark') },
    children: 'Tokyo Night · Dark'
  })
}

export default {
  id: 'hermes-tokyo-night',
  name: 'Tokyo Night',
  defaultEnabled: false,
  register(ctx) {
    ctx.register({ id: 'theme', area: THEMES_AREA, data: theme })
    ctx.register({ id: 'select', area: TITLEBAR_AREAS.right, render: () => jsx(SelectTokyoNight, {}) })
  }
}
