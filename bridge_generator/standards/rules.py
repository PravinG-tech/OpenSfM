"""Engineering helper rules and recommendations."""

from __future__ import annotations


def recommended_girder_depth(span_length_mm: float) -> float:
    return span_length_mm / 18.0


def recommended_diaphragm_spacing(span_length_mm: float) -> float:
    return min(6000.0, span_length_mm / 6.0)
