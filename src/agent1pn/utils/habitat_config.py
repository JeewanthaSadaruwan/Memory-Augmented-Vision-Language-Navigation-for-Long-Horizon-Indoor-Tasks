"""Habitat configuration helpers."""

from __future__ import annotations

import habitat


def get_pointnav_config(config_path: str, dataset_path: str):
    """Load a Habitat config and override the dataset path for this workspace."""
    config = habitat.get_config(config_path)

    try:
        from habitat.config import read_write

        with read_write(config):
            config.habitat.dataset.data_path = dataset_path
    except Exception:
        config.habitat.dataset.data_path = dataset_path

    return config
