"""Alignment object generation for bridge centerline."""

from __future__ import annotations

import FreeCAD as App
import Part


class AlignmentBuilder:
    """Builds centerline geometry for sweeping.

    Current mode: straight alignment.
    Extensible point: replace `build_straight` with composite curve generation.
    """

    def __init__(self, doc, params: dict):
        self.doc = doc
        self.params = params

    def build_straight(self):
        a = self.params["alignment"]
        g = self.params["general"]
        start = App.Vector(a["start_chainage"], 0.0, 0.0)
        end = App.Vector(a["end_chainage"], 0.0, g["span_length"] * (a["longitudinal_gradient"] / 100.0))

        wire = Part.makeLine(start, end)
        obj = self.doc.addObject("Part::Feature", "Centerline")
        obj.Shape = wire
        return obj
