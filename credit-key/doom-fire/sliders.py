import pygame as pg


# ============================================================
# PART 1: WORDS
# All the text shown in the control panel.
# ============================================================

STRENGTH_LABEL = "STRENGTH"
STRENGTH_LEFT = "OFF"
STRENGTH_RIGHT = "FULL"

WIND_LABEL = "WIND"
WIND_LEFT = "<< LEFT"
WIND_RIGHT = "RIGHT >>"

LUMINOSITY_LABEL = "LUMINOSITY"
LUMINOSITY_LEFT = "DIM"
LUMINOSITY_RIGHT = "BRIGHT"

KEYS_HINT = "[UP/DOWN] STRENGTH   [LEFT/RIGHT] WIND   [, .] LUMINOSITY"

PLATE_TEXT_COLOR = (40, 28, 12)     # dark letters stamped into brass
LCD_COLOR = (255, 176, 0)           # amber display digits
SCALE_COLOR = (150, 140, 128)

_fonts = {}


def get_fonts():
    # Fonts can only be made after pg.init(), so make them the first time
    if not _fonts:
        _fonts["lcd"] = pg.font.SysFont("courier", 26, bold=True)
        _fonts["plate"] = pg.font.SysFont("courier", 17, bold=True)
        _fonts["small"] = pg.font.SysFont("courier", 12, bold=True)
    return _fonts


def draw_words(screen, text, x, y, size, color, center=False, right=False):
    image = get_fonts()[size].render(text, False, color)
    if center:
        x -= image.get_width() // 2
    elif right:
        x -= image.get_width()
    screen.blit(image, (x, y))


def words_width(text, size):
    return get_fonts()[size].size(text)[0]

import pygame as pg

from fire import Fire

STRENGTH = {"value": 1.0, "min": 0.0, "max": 1.0}
WIND = {"value": -1.0, "min": -2.0, "max": 2.0}
LUMINOSITY = {"value": 1.0, "min": 0.0, "max": 2.0}

if not getattr(Fire, "_uses_sliders", False):
    original_update = Fire.update
    original_get_colors = Fire.get_colors

    def update_with_sliders(self, strength=1, wind=0):
        original_update(self, STRENGTH["value"], WIND["value"])
        if STRENGTH["value"] <= 0:
            self.intensity.fill(0)

    def get_colors_with_sliders(self, luminosity=1.0):
        return original_get_colors(self, LUMINOSITY["value"])

    Fire.update = update_with_sliders
    Fire.get_colors = get_colors_with_sliders
    Fire._uses_sliders = True


def clamp(data):
    data["value"] = max(data["min"], min(data["max"], data["value"]))


STRENGTH_STEP = 0.1
WIND_SPEED = 0.03
LIGHT_SPEED = 0.02
_keys_before = {}


def handle_keys():
    keys = pg.key.get_pressed()

    for key, amount in ((pg.K_UP, STRENGTH_STEP), (pg.K_DOWN, -STRENGTH_STEP)):
        was_down = _keys_before.get(key, False)
        if keys[key] and not was_down:
            STRENGTH["value"] = round(STRENGTH["value"] + amount, 2)
            clamp(STRENGTH)
        _keys_before[key] = keys[key]

    if keys[pg.K_LEFT]:
        WIND["value"] -= WIND_SPEED
    if keys[pg.K_RIGHT]:
        WIND["value"] += WIND_SPEED
    clamp(WIND)

    if keys[pg.K_COMMA]:
        LUMINOSITY["value"] -= LIGHT_SPEED
    if keys[pg.K_PERIOD]:
        LUMINOSITY["value"] += LIGHT_SPEED
    clamp(LUMINOSITY)
