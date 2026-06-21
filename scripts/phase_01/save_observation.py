from pathlib import Path

import habitat
import imageio
import numpy as np

from agent1pn.utils import ensure_scene_symlink


OUTPUT_DIR = Path("outputs/images")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

POINTNAV_DATA_PATH = (
    "data/versioned_data/habitat_test_pointnav_dataset_1.0/v1/{split}/{split}.json.gz"
)


def main():
    ensure_scene_symlink()

    config = habitat.get_config(
        "benchmark/nav/pointnav/pointnav_habitat_test.yaml"
    )

    # This repo stores PointNav episodes under data/versioned_data/...
    # so we override Habitat's default data_path before building env.
    try:
        from habitat.config import read_write

        with read_write(config):
            config.habitat.dataset.data_path = POINTNAV_DATA_PATH
    except Exception:
        # Fallback for config variants that are not read-only.
        config.habitat.dataset.data_path = POINTNAV_DATA_PATH

    # 2. Build the simulator, dataset and PointNav task
    env = habitat.Env(config=config)


    # 3. Load the first navigation episode
    observations = env.reset()

    rgb = observations["rgb"]
    depth = observations["depth"]
    pointgoal = observations["pointgoal_with_gps_compass"]

    print("RGB shape:", rgb.shape)
    print("Depth shape:", depth.shape)
    print("PointGoal:", pointgoal)

    rgb_path = OUTPUT_DIR / "rgb_observation.png"       # Full path where the RGB image will be saved
    depth_path = OUTPUT_DIR / "depth_observation.png"   # Full path where the depth image will be saved

    imageio.imwrite(rgb_path, rgb)                       # Save the RGB array directly as a PNG file

    depth_img = (depth.squeeze() * 255).astype(np.uint8)  # Convert depth: remove extra dimension, scale 0-1 float → 0-255 uint8 so it can be saved as a grayscale image
    imageio.imwrite(depth_path, depth_img)               # Save the converted depth array as a PNG file

    env.close()

    print(f"Saved {rgb_path}")
    print(f"Saved {depth_path}")


if __name__ == "__main__":
    main()

