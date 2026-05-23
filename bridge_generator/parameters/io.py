"""JSON and dict parameter loading utilities."""

from __future__ import annotations

import copy
import json
from pathlib import Path

from .defaults import default_parameters


def deep_merge(base: dict, override: dict) -> dict:
    """Deep-merge dictionaries recursively and return a new dict."""
    out = copy.deepcopy(base)
    for k, v in override.items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = deep_merge(out[k], v)
        else:
            out[k] = v
    return out


def load_parameters(json_path: str | None = None, overrides: dict | None = None) -> dict:
    """Load parameters from defaults + optional JSON + optional override dict."""
    params = default_parameters()
    if json_path:
        with Path(json_path).open("r", encoding="utf-8") as fp:
            params = deep_merge(params, json.load(fp))
    if overrides:
        params = deep_merge(params, overrides)
    return params
