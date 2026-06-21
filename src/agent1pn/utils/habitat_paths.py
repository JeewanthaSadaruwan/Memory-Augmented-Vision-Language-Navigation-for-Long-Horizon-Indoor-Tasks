"""Habitat dataset path helpers."""

from __future__ import annotations

from pathlib import Path


EXPECTED_SCENES_LINK = Path("data/scene_datasets/habitat-test-scenes")
LOCAL_SCENES_DIR = Path("data/versioned_data/habitat_test_scenes")


def ensure_scene_symlink() -> None:
    """Create/fix the habitat-test-scenes path expected by PointNav test episodes."""
    if not LOCAL_SCENES_DIR.exists():
        return

    if EXPECTED_SCENES_LINK.is_symlink() and EXPECTED_SCENES_LINK.exists():
        return

    if EXPECTED_SCENES_LINK.exists() and not EXPECTED_SCENES_LINK.is_symlink():
        return

    if EXPECTED_SCENES_LINK.is_symlink() and not EXPECTED_SCENES_LINK.exists():
        EXPECTED_SCENES_LINK.unlink()

    EXPECTED_SCENES_LINK.parent.mkdir(parents=True, exist_ok=True)
    EXPECTED_SCENES_LINK.symlink_to(LOCAL_SCENES_DIR.resolve())
