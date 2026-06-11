from pathlib import Path

import habitat
import imageio
import numpy as np


OUTPUT_DIR = Path("outputs/images")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def main():
    config = habitat.get_config(
        "benchmark/nav/pointnav/pointnav_habitat_test.yaml"
    )

    env = habitat.Env(config=config)
    observations = env.reset()

    rgb = observations["rgb"]
    depth = observations["depth"]
    pointgoal = observations["pointgoal_with_gps_compass"]

    print("RGB shape:", rgb.shape)
    print("Depth shape:", depth.shape)
    print("PointGoal:", pointgoal)

    rgb_path = OUTPUT_DIR / "rgb_observation.png"
    depth_path = OUTPUT_DIR / "depth_observation.png"

    imageio.imwrite(rgb_path, rgb)

    depth_img = (depth.squeeze() * 255).astype(np.uint8)
    imageio.imwrite(depth_path, depth_img)

    env.close()

    print(f"Saved {rgb_path}")
    print(f"Saved {depth_path}")


if __name__ == "__main__":
    main()