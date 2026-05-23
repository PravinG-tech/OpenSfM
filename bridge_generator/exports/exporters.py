"""Export routines for bridge model outputs."""

from __future__ import annotations

import Mesh
import Import
import ImportGui


def export_step(objs, path: str):
    Import.export(objs, path)


def export_ifc(objs, path: str):
    # IFC export availability depends on FreeCAD IFC workbench installation.
    ImportGui.export(objs, path)


def export_stl(objs, path: str):
    Mesh.export(objs, path)
