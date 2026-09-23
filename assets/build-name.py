"""Shape "Deon Roos" in Inter Tight and write the glyph outlines to name-outlines.json.

Only needed when the name, weight or size changes. Requires:
  pip install fonttools uharfbuzz
  Inter Tight variable font (OFL): https://github.com/google/fonts/tree/main/ofl/intertight

Usage: python3 assets/build-name.py path/to/InterTight[wght].ttf
"""
import json
import sys
from pathlib import Path

import uharfbuzz as hb
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

TEXT, WEIGHT, SIZE, TRACK = "Deon Roos", 800, 88, -3.5

font = instantiateVariableFont(TTFont(sys.argv[1]), {"wght": WEIGHT})
static = Path("/tmp/name-static.ttf")
font.save(static)
scale = SIZE / font["head"].unitsPerEm

hbfont = hb.Font(hb.Face(hb.Blob.from_file_path(str(static))))
buf = hb.Buffer()
buf.add_str(TEXT)
buf.guess_segment_properties()
hb.shape(hbfont, buf, {"kern": True, "liga": True})

glyphset, order = font.getGlyphSet(), font.getGlyphOrder()
paths, x = [], 0.0
for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
    pen = SVGPathPen(glyphset)
    glyphset[order[info.codepoint]].draw(
        TransformPen(pen, (scale, 0, 0, -scale, x + pos.x_offset * scale, -pos.y_offset * scale)))
    if pen.getCommands():
        paths.append(pen.getCommands())
    x += pos.x_advance * scale + TRACK

out = Path(__file__).parent / "name-outlines.json"
out.write_text(json.dumps({"text": TEXT, "font": "Inter Tight", "weight": WEIGHT, "size": SIZE,
                           "width": round(x - TRACK, 2), "paths": paths}))
print(f"{len(paths)} glyphs, {x - TRACK:.1f}px wide -> {out}")
