"""Visualization helper functions."""

from __future__ import annotations

import os


def load_cv2(live_display: bool):
    """Load OpenCV only when interactive display is enabled and available."""
    if not live_display:
        return None
    if not os.environ.get("DISPLAY"):
        print("DISPLAY is not set. Live display disabled.")
        return None

    try:
        import cv2 as cv2_import

        return cv2_import
    except Exception:
        print("OpenCV not available. Live display disabled.")
        return None


def render_rgb_frame(
    cv2_module,
    observations: dict,
    step: int,
    action: str,
    rho: float,
    phi_deg: float,
    window_name: str,
    wait_ms: int,
) -> bool:
    """Render the current RGB frame and return False when the user quits."""
    rgb = observations.get("rgb")
    if rgb is None:
        return True

    bgr = cv2_module.cvtColor(rgb, cv2_module.COLOR_RGB2BGR)
    overlay = (
        f"step={step:02d} action={action} dist={rho:.2f}m bearing={phi_deg:.1f}deg"
    )
    cv2_module.putText(
        bgr,
        overlay,
        (10, 24),
        cv2_module.FONT_HERSHEY_SIMPLEX,
        0.55,
        (255, 255, 255),
        2,
        cv2_module.LINE_AA,
    )
    cv2_module.putText(
        bgr,
        overlay,
        (10, 24),
        cv2_module.FONT_HERSHEY_SIMPLEX,
        0.55,
        (25, 25, 25),
        1,
        cv2_module.LINE_AA,
    )
    cv2_module.imshow(window_name, bgr)
    key = cv2_module.waitKey(wait_ms) & 0xFF
    return key != ord("q")
