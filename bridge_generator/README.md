# Bridge Generator (FreeCAD 1.0+)

Parametric RCC box girder automation script using FreeCAD Python API.

## Run

```bash
FreeCADCmd bridge_generator/main.py --input bridge_generator/templates/sample_bridge_parameters.json --fcstd out.FCStd --step out.step --stl out.stl
```

## Notes
- Units are millimeters.
- Current alignment implementation is straight, with extension hooks for curved geometry.
- Architecture is modular for future support (multi-cell, variable depth, tendons, IFC BIM expansion).
