"""Guard the shipped skin asset: banner art present, colors stay #rrggbb. Stdlib only."""
import re
from pathlib import Path
import unittest

ASSET = Path(__file__).parents[1] / "skins" / "tokyo-night.yaml"


class SkinAssetTests(unittest.TestCase):
    def setUp(self):
        self.text = ASSET.read_text(encoding="utf-8")
        self.lines = self.text.splitlines()

    def test_banner_art_shipped(self):
        # Regression guard: the packaged skin once shipped without banner_logo/
        # banner_hero, so fresh installs fell back to the default gold banner.
        found = {}
        for line in self.lines:
            match = re.match(r"^(banner_logo|banner_hero): '(.+)$", line)
            if match:
                self.assertGreater(len(match.group(2).strip("'\"")), 40,
                                   f"{match.group(1)} art looks empty")
                found[match.group(1)] = True
        self.assertEqual(sorted(found), ["banner_hero", "banner_logo"],
                         "skin must ship both banner_logo and banner_hero")

    def test_colors_are_hex(self):
        in_colors = False
        checked = 0
        for line in self.lines:
            if re.match(r"^\S", line):
                in_colors = line.startswith("colors:")
                continue
            if not in_colors:
                continue
            match = re.match(r"^\s+(\S+): '([^']+)'$", line)
            if not match:
                continue
            self.assertRegex(match.group(2), r"^#[0-9A-Fa-f]{6}$",
                             f"color {match.group(1)} must be #rrggbb")
            checked += 1
        self.assertGreaterEqual(checked, 20, "expected the full palette to be present")

    def test_no_personal_branding_or_spinner(self):
        for key in ("branding:", "spinner:", "tool_prefix:", "tool_emojis:"):
            self.assertNotIn(f"\n{key}", f"\n{self.text}",
                             f"personal-flavor section {key} must stay out of the package")


if __name__ == "__main__":
    unittest.main()
