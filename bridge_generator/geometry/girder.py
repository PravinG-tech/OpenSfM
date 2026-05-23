"""Parametric RCC box girder geometry generation."""

from __future__ import annotations

import FreeCAD as App
import Part


class GirderGeometryBuilder:
    def __init__(self, doc, params: dict):
        self.doc = doc
        self.params = params

    def _make_cross_section_face(self):
        g = self.params["general"]
        gg = self.params["girder_geometry"]

        tw = g["total_bridge_width"]
        depth = gg["girder_depth"]
        ts = gg["top_slab_thickness"]
        bs = gg["bottom_slab_thickness"]
        wt = gg["web_thickness"]
        iw = gg["inside_clear_width"]

        x0 = -tw / 2.0
        x1 = tw / 2.0
        y_top = 0.0
        y_bot = -depth

        outer_pts = [
            App.Vector(x0, y_top, 0),
            App.Vector(x1, y_top, 0),
            App.Vector(x1, y_bot, 0),
            App.Vector(x0, y_bot, 0),
            App.Vector(x0, y_top, 0),
        ]

        inner_x0 = -iw / 2.0
        inner_x1 = iw / 2.0
        inner_y_top = y_top - ts
        inner_y_bot = y_bot + bs
        # inner void centered, with web thickness governed indirectly by total width and inside width
        inner_pts = [
            App.Vector(inner_x0, inner_y_top, 0),
            App.Vector(inner_x1, inner_y_top, 0),
            App.Vector(inner_x1, inner_y_bot, 0),
            App.Vector(inner_x0, inner_y_bot, 0),
            App.Vector(inner_x0, inner_y_top, 0),
        ]

        outer_wire = Part.makePolygon(outer_pts)
        inner_wire = Part.makePolygon(inner_pts)

        face = Part.Face([outer_wire, inner_wire])

        # Add simple haunch proxies as fillets on inner slab-web corners.
        haunch = gg["haunch_size"]
        if haunch > 0:
            try:
                face = face.makeFillet(haunch, face.Edges)
            except Exception:
                pass

        cs_obj = self.doc.addObject("Part::Feature", "CrossSectionFace")
        cs_obj.Shape = face
        return cs_obj

    def sweep_along_alignment(self, alignment_obj):
        cs_obj = self._make_cross_section_face()
        sweep = self.doc.addObject("Part::Sweep", "DeckSweep")
        sweep.Sections = [cs_obj]
        sweep.Spine = (alignment_obj, ["Edge1"])
        sweep.Solid = True
        sweep.Frenet = False
        return cs_obj, sweep

    def create_diaphragms(self, deck_shape_obj):
        gg = self.params["girder_geometry"]
        a = self.params["alignment"]

        spacing = gg["diaphragm_spacing"]
        thickness = gg["diaphragm_thickness"]
        start = a["start_chainage"]
        end = a["end_chainage"]

        diaphragms = []
        x = start
        idx = 1
        bbox = deck_shape_obj.Shape.BoundBox
        while x <= end + 1e-6:
            box = Part.makeBox(thickness, bbox.YLength, bbox.ZLength)
            box.translate(App.Vector(x - thickness / 2.0, bbox.YMin, bbox.ZMin))
            obj = self.doc.addObject("Part::Feature", f"Diaphragm_{idx:03d}")
            obj.Shape = box.common(deck_shape_obj.Shape)
            diaphragms.append(obj)
            idx += 1
            x += spacing
        return diaphragms

    def create_segments(self, deck_shape_obj):
        seg = self.params["segment"]
        a = self.params["alignment"]

        seg_len = seg["segment_length"]
        joint = seg["match_cast_joint_thickness"]
        start = a["start_chainage"]
        end = a["end_chainage"]
        bbox = deck_shape_obj.Shape.BoundBox

        out = []
        idx = 1
        x = start
        while x < end - 1e-6:
            cut_len = min(seg_len - joint, end - x)
            prism = Part.makeBox(cut_len, bbox.YLength, bbox.ZLength)
            prism.translate(App.Vector(x, bbox.YMin, bbox.ZMin))
            obj = self.doc.addObject("Part::Feature", f"Segment_{idx:03d}")
            obj.Shape = prism.common(deck_shape_obj.Shape)
            out.append(obj)
            x += seg_len
            idx += 1
        return out
