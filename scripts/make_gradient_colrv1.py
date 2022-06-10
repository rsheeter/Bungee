"""
Usage:
  python scripts/make_gradient_colrv1.py fonts/Bungee_Color_Fonts/BungeeColor-Regular_colr_Windows.ttf
"""

from fontTools.ttLib import getTableModule
from fontTools.ttLib import TTFont
from fontTools.ttLib.tables import otTables as ot
from fontTools.colorLib import builder
from fontTools import designspaceLib
from fontTools import varLib
import os
import pprint
import sys


def color(hex: str):
    return getTableModule("CPAL").Color.fromHex(hex)


# Ref https://github.com/fonttools/fonttools/blob/main/Tests/colorLib/builder_test.py

assert len(sys.argv) == 2


def _build_font(shift):
    font = TTFont(sys.argv[1])

    colr0 = font["COLR"]
    assert colr0.version == 0

    cpal = font["CPAL"]
    assert cpal.palettes == [[color("#C90900FF"), color("#FF9580FF")]]

    cpal.palettes[0].append(color("#ffd700"))
    cpal_red = 0
    grad_c1 = cpal_red
    grad_c2 = 2
    cpal.numPaletteEntries = len(cpal.palettes[0])

    def grad_c1_c2(center):
        return {
            "Format": ot.PaintFormat.PaintLinearGradient,
            "ColorLine": {
                "ColorStop": [(0.0, grad_c1), (center, grad_c2), (1.0, grad_c1)],
                "Extend": "reflect",
            },
            "x0": 0,
            "y0": 0,
            "x1": 0,
            "y1": 900,
            "x2": 100,
            "y2": 0,
        }

    def grad_c2_c1(center):
        return {
            "Format": ot.PaintFormat.PaintLinearGradient,
            "ColorLine": {
                "ColorStop": [(0.0, grad_c2), (center, grad_c1), (1.0, grad_c2)],
                "Extend": "reflect",
            },
            "x0": 0,
            "y0": 0,
            "x1": 0,
            "y1": 900,
            "x2": 100,
            "y2": 0,
        }

    def make_colrv1_map(shift):
        colrv1_map = {}

        for glyph_name, layers in colr0.ColorLayers.items():
            v1_layers = []
            colrv1_map[glyph_name] = (ot.PaintFormat.PaintColrLayers, v1_layers)
            for layer in layers:
                # Match COLRv0 fill
                # fill = {
                #   "Format": ot.PaintFormat.PaintSolid,
                #   "PaletteIndex": layer.colorID,
                #   "Alpha": 1,
                # }
                if layer.colorID == cpal_red:
                    fill = grad_c1_c2(0.5 - shift)
                else:
                    fill = grad_c2_c1(0.5 + shift)
                v1_layers.append(
                    {
                        "Format": ot.PaintFormat.PaintGlyph,
                        "Paint": fill,
                        "Glyph": layer.name,
                    }
                )
            if len(v1_layers) == 1:
                colrv1_map[glyph_name] = v1_layers[0]
        return colrv1_map

    colr = builder.buildCOLR(make_colrv1_map(shift))
    font["COLR"] = colr

    name_table = font["name"]

    def set_name(name_id, new_value):
        name_table.setName(new_value, name_id, 1, 0, 0)  # Mac
        name_table.setName(new_value, name_id, 3, 1, 0x409)  # Windows

    # I hope this is roughly reasonable :)
    # Ref https://docs.microsoft.com/en-us/typography/opentype/spec/name#name-ids
    set_name(0, "Copyright 2021 Roderick Sheeter")
    set_name(1, "Bungee Spice Regular")
    set_name(3, "0.0.1")
    set_name(4, "Bungee Spice Regular")
    set_name(5, "Version 0.0.1")
    set_name(6, "BungeeSpice-Regular")
    name_table.removeNames(nameID=7)
    set_name(8, "Rod S")
    name_table.removeNames(nameID=9)
    set_name(10, "Bungee derivative created to exhibit COLRv1 gradients")
    name_table.removeNames(nameID=11)
    name_table.removeNames(nameID=12)
    set_name(16, "Bungee Spice")
    return font


out_file = sys.argv[1] + "-colrv1.ttf"


designspace = designspaceLib.DesignSpaceDocument()

min_shift = -0.49
max_shift = -min_shift
axis_defs = [
    dict(
        tag="GRSH",
        name="Gradient Shift",
        minimum=min_shift,
        default=0,
        maximum=max_shift,
    ),
]

for axis_def in axis_defs:
    designspace.addAxisDescriptor(**axis_def)

designspace.addSourceDescriptor(
    name="All Default",
    location={"Gradient Shift": 0},
    font=_build_font(0),
)

designspace.addSourceDescriptor(
    name="Up",
    location={"Gradient Shift": max_shift},
    font=_build_font(max_shift),
)

designspace.addSourceDescriptor(
    name="Down",
    location={"Gradient Shift": min_shift},
    font=_build_font(min_shift),
)

print(designspace.tostring().decode())

# font = build_font(-0.1)
# font.save(out_file)

vf = varLib.build(
    designspace,
)[0]

vf.save(out_file)

print(f"Wrote {out_file}")
