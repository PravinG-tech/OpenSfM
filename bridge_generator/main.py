"""FreeCADCmd entry point for parametric RCC bridge girder generation.

Usage:
  FreeCADCmd bridge_generator/main.py --input bridge_generator/templates/sample_bridge_parameters.json
"""

from __future__ import annotations

import argparse
import os
import sys

import FreeCAD as App

from alignment.centerline import AlignmentBuilder
from exports.exporters import export_ifc, export_step, export_stl
from geometry.girder import GirderGeometryBuilder
from parameters.io import load_parameters
from standards.rules import recommended_diaphragm_spacing, recommended_girder_depth
from utilities.validation import validate_parameters


class BridgeGirderGenerator:
    """Top-level orchestrator for bridge model generation."""

    def __init__(self, params: dict):
        self.params = params
        self.doc = App.newDocument(params["general"]["bridge_name"])
        self.groups = {}
        self._setup_document_tree()

    def _setup_document_tree(self):
        for name in [
            "Alignment",
            "CrossSections",
            "Deck",
            "Diaphragms",
            "Bearings",
            "Tendons",
            "ConstructionSegments",
        ]:
            self.groups[name] = self.doc.addObject("App::DocumentObjectGroup", name)

    def apply_engineering_defaults(self):
        g = self.params["general"]
        gg = self.params["girder_geometry"]
        if gg.get("girder_depth", 0) <= 0:
            gg["girder_depth"] = recommended_girder_depth(g["span_length"])
        if gg.get("diaphragm_spacing", 0) <= 0:
            gg["diaphragm_spacing"] = recommended_diaphragm_spacing(g["span_length"])

    def build(self):
        self.apply_engineering_defaults()
        validate_parameters(self.params)

        align = AlignmentBuilder(self.doc, self.params).build_straight()
        self.groups["Alignment"].addObject(align)

        geom = GirderGeometryBuilder(self.doc, self.params)
        cs_obj, deck_sweep = geom.sweep_along_alignment(align)
        self.groups["CrossSections"].addObject(cs_obj)
        self.groups["Deck"].addObject(deck_sweep)

        self.doc.recompute()

        diaphragms = geom.create_diaphragms(deck_sweep)
        for d in diaphragms:
            self.groups["Diaphragms"].addObject(d)

        segments = geom.create_segments(deck_sweep)
        for s in segments:
            self.groups["ConstructionSegments"].addObject(s)

        self.doc.recompute()
        return {"alignment": align, "cross_section": cs_obj, "deck": deck_sweep, "diaphragms": diaphragms, "segments": segments}


def parse_args(argv=None):
    p = argparse.ArgumentParser(description="Parametric RCC bridge girder generator for FreeCAD")
    p.add_argument("--input", help="JSON parameter file", default=None)
    p.add_argument("--fcstd", help="Optional output FCStd path", default="bridge_model.FCStd")
    p.add_argument("--step", help="Optional STEP output path", default=None)
    p.add_argument("--ifc", help="Optional IFC output path", default=None)
    p.add_argument("--stl", help="Optional STL output path", default=None)
    return p.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    params = load_parameters(args.input)

    gen = BridgeGirderGenerator(params)
    result = gen.build()

    if args.fcstd:
        gen.doc.saveAs(os.path.abspath(args.fcstd))
    export_targets = [result["deck"]] + result["diaphragms"] + result["segments"]
    if args.step:
        export_step(export_targets, os.path.abspath(args.step))
    if args.ifc:
        export_ifc(export_targets, os.path.abspath(args.ifc))
    if args.stl:
        export_stl(export_targets, os.path.abspath(args.stl))

    print("Bridge girder model generated successfully.")


if __name__ == "__main__":
    main(sys.argv[1:])
