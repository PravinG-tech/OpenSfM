"""Default parameter definitions for RCC bridge girder generation (mm-based)."""

from __future__ import annotations


def default_parameters() -> dict:
    """Return a fully-populated default parameter dictionary.

    Units:
      - Lengths: mm
      - Angles: degrees
      - Percentages: percent values (e.g., 2.5 means 2.5%)
    """
    span_length = 36000.0
    return {
        "general": {
            "bridge_name": "RCC_Box_Girder_Demo",
            "girder_type": "single_cell_box",
            "span_length": span_length,
            "total_bridge_width": 12000.0,
            "carriageway_width": 9000.0,
            "number_of_lanes": 2,
            "skew_angle": 0.0,
            "cross_fall_percent": 2.5,
        },
        "girder_geometry": {
            "girder_depth": span_length / 18.0,
            "top_slab_thickness": 250.0,
            "bottom_slab_thickness": 300.0,
            "web_thickness": 350.0,
            "cantilever_length": 1500.0,
            "inside_clear_width": 5000.0,
            "haunch_size": 120.0,
            "diaphragm_thickness": 350.0,
            "diaphragm_spacing": 6000.0,
        },
        "alignment": {
            "start_chainage": 0.0,
            "end_chainage": span_length,
            "longitudinal_gradient": 0.0,
            "horizontal_radius": 0.0,
            "vertical_curve_radius": 0.0,
        },
        "pier_data": {
            "pier_spacing": 12000.0,
            "bearing_seat_width": 1000.0,
            "bearing_seat_length": 1600.0,
        },
        "segment": {
            "segment_length": 3000.0,
            "number_of_segments": 12,
            "match_cast_joint_thickness": 25.0,
        },
        "prestressing": {
            "tendon_duct_diameter": 100.0,
            "tendon_profile_type": "parabolic_placeholder",
            "tendon_cover": 80.0,
        },
    }
