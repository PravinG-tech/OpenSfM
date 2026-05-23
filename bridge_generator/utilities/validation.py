"""Input validation and geometric sanity checks."""

from __future__ import annotations


class ValidationError(ValueError):
    """Raised for invalid bridge/girder parameter combinations."""


def _require_positive(name: str, value: float) -> None:
    if value <= 0:
        raise ValidationError(f"{name} must be > 0, got {value}")


def validate_parameters(params: dict) -> None:
    g = params["general"]
    gg = params["girder_geometry"]
    seg = params["segment"]

    positives = {
        "span_length": g["span_length"],
        "total_bridge_width": g["total_bridge_width"],
        "carriageway_width": g["carriageway_width"],
        "girder_depth": gg["girder_depth"],
        "top_slab_thickness": gg["top_slab_thickness"],
        "bottom_slab_thickness": gg["bottom_slab_thickness"],
        "web_thickness": gg["web_thickness"],
        "inside_clear_width": gg["inside_clear_width"],
        "diaphragm_thickness": gg["diaphragm_thickness"],
        "diaphragm_spacing": gg["diaphragm_spacing"],
        "segment_length": seg["segment_length"],
    }
    for name, value in positives.items():
        _require_positive(name, float(value))

    if g["carriageway_width"] > g["total_bridge_width"]:
        raise ValidationError("carriageway_width cannot exceed total_bridge_width")

    total_required_width = gg["inside_clear_width"] + 2.0 * gg["web_thickness"]
    if total_required_width > g["total_bridge_width"]:
        raise ValidationError("inside_clear_width + 2*web_thickness exceeds total_bridge_width")

    clear_depth = gg["girder_depth"] - gg["top_slab_thickness"] - gg["bottom_slab_thickness"]
    if clear_depth <= 0:
        raise ValidationError("girder_depth must exceed top+bottom slab thickness")

    if gg["web_thickness"] < 250.0:
        raise ValidationError("web_thickness below conservative minimum (250 mm)")

    cant_ratio = gg["cantilever_length"] / g["total_bridge_width"]
    if cant_ratio > 0.30:
        raise ValidationError("cantilever_length too large relative to total width (>30%)")

    depth_ratio = g["span_length"] / gg["girder_depth"]
    if depth_ratio < 12.0 or depth_ratio > 30.0:
        raise ValidationError("invalid span/depth ratio, expected roughly between 12 and 30")
