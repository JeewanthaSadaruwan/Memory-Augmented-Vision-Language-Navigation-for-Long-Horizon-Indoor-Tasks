"""Minimal PointNav runner with a simple rule-based policy."""

from __future__ import annotations

import math
import os

import habitat

from agent1pn.agents import RuleBasedAgent, describe_action
from agent1pn.utils import (
    ensure_scene_symlink,
    get_pointnav_config,
    load_cv2,
    render_rgb_frame,
)


CONFIG_PATH = "benchmark/nav/pointnav/pointnav_habitat_test.yaml"
MAX_STEPS = 50
POINTNAV_DATA_PATH = (
    "data/versioned_data/habitat_test_pointnav_dataset_1.0/v1/{split}/{split}.json.gz"
)
LIVE_DISPLAY = os.environ.get("POINTNAV_SHOW_DISPLAY", "1") == "1"
DISPLAY_WINDOW_NAME = "PointNav Agent RGB"
DISPLAY_WAIT_MS = 60


def main() -> None:
    ensure_scene_symlink()

    config = get_pointnav_config(CONFIG_PATH, POINTNAV_DATA_PATH)

    turn_angle_deg = float(getattr(config.habitat.simulator, "turn_angle", 10.0))
    step_size_m = float(getattr(config.habitat.simulator, "forward_step_size", 0.25))
    agent = RuleBasedAgent()

    cv2 = load_cv2(LIVE_DISPLAY)

    env = habitat.Env(config=config)

    try:
        observations = env.reset()
        print("Episode loaded")

        episode = env.current_episode
        print(f"episode_id={getattr(episode, 'episode_id', 'unknown')}")
        print(f"scene_id={getattr(episode, 'scene_id', 'unknown')}")
        print(f"start_position={getattr(episode, 'start_position', 'unknown')}")
        print(f"start_rotation={getattr(episode, 'start_rotation', 'unknown')}")

        if cv2 is not None:
            cv2.namedWindow(DISPLAY_WINDOW_NAME, cv2.WINDOW_NORMAL)
            rho0, phi0 = observations["pointgoal_with_gps_compass"]
            if not render_rgb_frame(
                cv2,
                observations,
                0,
                "reset",
                float(rho0),
                math.degrees(float(phi0)),
                DISPLAY_WINDOW_NAME,
                DISPLAY_WAIT_MS,
            ):
                print("User requested exit from display window (q).")
                return

        for step in range(1, MAX_STEPS + 1):
            action = agent.act(observations)
            observations = env.step({"action": action})

            rho, phi = observations["pointgoal_with_gps_compass"]
            metrics = env.get_metrics()
            success = metrics.get("success", 0.0)
            spl = metrics.get("spl", 0.0)
            action_text = describe_action(action, turn_angle_deg, step_size_m)

            print(
                f"step={step:02d} action={action_text:24s} "
                f"distance={float(rho):.3f} bearing_deg={math.degrees(float(phi)):.1f} "
                f"success={success:.1f} spl={spl:.3f}"
            )

            if cv2 is not None:
                should_continue = render_rgb_frame(
                    cv2,
                    observations,
                    step,
                    action,
                    float(rho),
                    math.degrees(float(phi)),
                    DISPLAY_WINDOW_NAME,
                    DISPLAY_WAIT_MS,
                )
                if not should_continue:
                    print("User requested exit from display window (q).")
                    break

            if env.episode_over or action == "stop":
                break

        print("Final metrics:", env.get_metrics())
    finally:
        if cv2 is not None:
            cv2.destroyAllWindows()
        env.close()


if __name__ == "__main__":
    main()