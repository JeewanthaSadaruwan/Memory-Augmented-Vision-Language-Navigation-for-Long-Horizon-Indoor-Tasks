# VLN AI Assistant

Small research workspace for Habitat-Lab PointNav experiments, simple rule-based agents, and observation/debug output generation.

## Project Phases

<details>
<summary>Phase 1</summary>

Phase 1 focused on verifying that the Habitat environment is working end to end and that a single PointNav episode can be loaded and inspected.

Completed in this phase:
- Verified the Habitat Python import and local environment setup.
- Confirmed that the simulator environment can be created successfully.
- Loaded one PointNav episode with `env.reset()`.
- Inspected the returned observations for RGB, depth, and point-goal data.
- Saved sample RGB and depth outputs to `outputs/images/`.

Scripts used in Phase 1:
- `scripts/phase_01/test_habitat_import.py` for import and environment checks.
- `scripts/phase_01/test_env.py` for simulator/environment validation.
- `scripts/phase_01/save_observation.py` for loading one episode and saving RGB/depth observations.
- `scripts/phase_01/simple_pointnav_agent.py` as the initial PointNav experimentation script.

</details>

<details>
<summary>Phase 2</summary>

Phase 2 details will be added here as the next set of experiments is defined.

</details>

## Data and Output Folders
This repository does **not** track the `data/` and `outputs/` folders in Git.

These folders are ignored because they contain downloaded datasets, 3D scene assets, generated images, videos, logs, and other experiment outputs. These files can become large and should not be committed to the repository.

```text
data/      # Habitat datasets and scene assets
outputs/   # Generated images, videos, logs, and experiment results
```

---

### Data Folder
The `data/` folder is required to run Habitat-Lab tasks such as PointNav.

In this project, the `data/` folder is linked to the Habitat-Lab data directory:

```bash
ln -s ~/habitat_projects/habitat-lab/data data
```

So the project uses the same datasets downloaded for Habitat-Lab.

Expected structure:

```text
data/
├── scene_datasets/
│   └── habitat-test-scenes/
│       ├── apartment_1.glb
│       ├── skokloster-castle.glb
│       └── van-gogh-room.glb
│
├── datasets/
│   └── pointnav/
│       └── habitat-test-scenes/
│
└── versioned_data/
		├── habitat_test_scenes/
		└── habitat_test_pointnav_dataset_1.0/
```

---

### Downloading Habitat Test Scenes
Activate the Habitat environment first:

```bash
conda activate habitat-display
```

Download the Habitat test scenes:

```bash
python -m habitat_sim.utils.datasets_download \
	--uids habitat_test_scenes \
	--data-path ~/habitat_projects/habitat-lab/data/
```

This downloads small test scenes such as:

```text
apartment_1.glb
skokloster-castle.glb
van-gogh-room.glb
```

These scenes are used as simple 3D environments for testing Habitat-Sim and Habitat-Lab.

---

### Downloading the PointNav Test Dataset
Download the PointNav test dataset:

```bash
python -m habitat_sim.utils.datasets_download \
	--uids habitat_test_pointnav_dataset \
	--data-path ~/habitat_projects/habitat-lab/data/
```

This creates PointNav episode files such as:

```text
data/versioned_data/habitat_test_pointnav_dataset_1.0/v1/train/train.json.gz
data/versioned_data/habitat_test_pointnav_dataset_1.0/v1/val/val.json.gz
data/versioned_data/habitat_test_pointnav_dataset_1.0/v1/test/test.json.gz
```

These files define PointNav navigation episodes, including:

```text
scene_id
start_position
start_rotation
goal_position
geodesic_distance
difficulty
```

The dataset does not directly store RGB or depth images. Habitat-Sim renders those observations during runtime from the 3D scene.

---

### Creating the Data Symlink
From this project root:

```bash
cd ~/habitat_projects/vln_ai_assistant
ln -s ~/habitat_projects/habitat-lab/data data
```

Check:

```bash
ls -l data
```

Expected:

```text
data -> /home/js/habitat_projects/habitat-lab/data
```

---

### Output Folder
The `outputs/` folder is used for generated files such as:

```text
outputs/images/
outputs/videos/
outputs/logs/
```

Example generated files:

```text
outputs/images/rgb_observation.png
outputs/images/depth_observation.png
```

These files are produced by scripts during experiments and are not tracked by Git.

To recreate the folder structure:

```bash
mkdir -p outputs/images outputs/videos outputs/logs
```

---

### Git Ignore Policy
The following folders are intentionally ignored:

```text
data/
outputs/
```

This keeps the repository lightweight and reproducible. Anyone cloning the repository should download the Habitat datasets again using the commands above.
