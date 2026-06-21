"""Rule-based PointNav agent policy."""

from __future__ import annotations


TURN_THRESHOLD_RAD = 0.25
STOP_DISTANCE_M = 0.2


def choose_action(
    observations: dict,
    turn_threshold_rad: float = TURN_THRESHOLD_RAD,
    stop_distance_m: float = STOP_DISTANCE_M,
) -> str:
    """Turn toward the goal bearing, then move forward until close enough to stop."""
    rho, phi = observations["pointgoal_with_gps_compass"]

    if float(rho) < stop_distance_m:
        return "stop"
    if float(phi) > turn_threshold_rad:
        return "turn_left"
    if float(phi) < -turn_threshold_rad:
        return "turn_right"
    return "move_forward"


def describe_action(action: str, turn_angle_deg: float, step_size_m: float) -> str:
    """Format the action using the simulator step sizes for readable logs."""
    if action == "turn_left":
        return f"turn_left (~{turn_angle_deg:.1f} deg)"
    if action == "turn_right":
        return f"turn_right (~{turn_angle_deg:.1f} deg)"
    if action == "move_forward":
        return f"move_forward (~{step_size_m:.2f} m)"
    return "stop"


class RuleBasedAgent:
    """Minimal wrapper around the PointNav rule-based policy."""

    def __init__(
        self,
        turn_threshold_rad: float = TURN_THRESHOLD_RAD,
        stop_distance_m: float = STOP_DISTANCE_M,
    ) -> None:
        self.turn_threshold_rad = turn_threshold_rad
        self.stop_distance_m = stop_distance_m

    def act(self, observations: dict) -> str:
        return choose_action(
            observations,
            turn_threshold_rad=self.turn_threshold_rad,
            stop_distance_m=self.stop_distance_m,
        )
