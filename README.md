# robotic-reasoner-review.github.io

Static project website for **Training Robots to Reason in Natural Language via Reinforcement Learning**, deployed via GitHub Pages.

## Deploy

Push to `main`. The workflow in `.github/workflows/static.yml` publishes the repo to GitHub Pages automatically.

## Task rollout videos — full workflow

This section covers the end-to-end process: from raw evaluation renders to videos playing on the website.

### 1. Source layout

Rendered rollouts are stored locally under `tmp/` (gitignored). Typical structure:

```
tmp/vis_vlm_qwen35_v3_1_rendered/
  vis_<task>-qwen35_.../
    job0_seedXXXXXX/
      videos/
        custom_<task>_0_0_success.mp4
        custom_<task>_0_1_failure.mp4
        ...
    job1_seedXXXXXX/
      videos/
        ...
    job2_...
    job3_...
```

Hierarchy: **task → job → trajectory**. Success videos are named `*_success.mp4`.

Filenames encode **scene** and **trial** as `<scene>_<trial>` before `_success.mp4`:

```
custom_gris_0_2_success.mp4  →  scene 0, trial 2 (2nd successful trial in scene 0)
custom_gris_1_3_success.mp4  →  scene 1, trial 3
```

### 2. Pick successful examples

For each task, pick **N** success videos (default **2**) from **different scenes**:

- Valid pair: scene `0` + scene `1` (e.g. `0_5` and `1_3`)
- Invalid pair: two scenes the same (e.g. `0_5` and `0_7`)

**Search order:**

1. Walk jobs in order: `job0`, `job1`, `job2`, …
2. Within each job, sort successes by `(scene, trial)`
3. Take the first success for a scene not yet picked
4. Stop when N distinct scenes are found; if `job0` is not enough, continue into `job1`, etc.

Both examples may come from the same job (e.g. both from `job0`) if that job has enough distinct scenes.

**Automated selection:**

```bash
python scripts/find_task_examples.py
```

Writes `draft.md` with one line per example, including job/scene/trial metadata. Set `NUM_EXAMPLES` at the top of that script to change N.

### 3. Record paths in `draft.md`

`find_task_examples.py` generates this automatically. Example:

```markdown
## Group isolate

Example trajectory 1 (job0, scene 0, trial 2): tmp/vis_vlm_qwen35_v3_1_rendered/vis_gris-.../job0_seed204000/videos/custom_group_isolate_0_2_success.mp4
Example trajectory 2 (job0, scene 1, trial 0): tmp/vis_vlm_qwen35_v3_1_rendered/vis_gris-.../job0_seed204000/videos/custom_group_isolate_1_0_success.mp4
```

You can edit `draft.md` by hand or re-run the find script after new renders land in `tmp/`.

### 4. Copy into `static/`

Videos committed to the repo go under:

```
static/task_examples_ours/
  <task_name>/
    job0/          # job folder matches source job (job0, job1, …)
      custom_<task_name>_<scene>_<trial>_success.mp4
    job1/          # only present if an example came from job1
      ...
```

Naming rules (applied by the script):

- Shape tasks (`T`, `V`, `L`, `iV`, `iL`): `custom_<task>_shape_<scene>_<trial>_success.mp4`
- Other tasks: `custom_<task>_<scene>_<trial>_success.mp4`
- Job folder reflects the source job; both examples can live under `job0/` if selected there

Only files under `static/task_examples_ours/` are deployed. **`tmp/` is never committed.**

### 5. Update `index.html`

Each task gets a section with **two videos in one row** (Bulma `columns`):

```html
<section class="section rollout-section">
  <div class="container">
    <h2 class="title is-4 has-text-centered">Clear half</h2>
    <div class="columns is-vcentered rollout-row">
      <div class="column">
        <div class="item">
          <video controls muted playsinline preload="metadata">
            <source src="./static/task_examples_ours/clear_half/job0/custom_clear_half_0_0_success.mp4" type="video/mp4">
          </video>
          <p class="caption has-text-centered">Example trajectory 1</p>
        </div>
      </div>
      <div class="column">
        <!-- Example trajectory 2 (may be same or different job; always a different scene) -->
      </div>
    </div>
  </div>
</section>
```

When adding a **new task**, append a section like this and add the task title to `TASK_META` in `scripts/prepare_task_videos.py`.

### 6. Re-encode for web playback

Source MP4s are often **MPEG-4 Part 2 (`mp4v`)**. Browsers require **H.264 (`avc1`)** for HTML5 `<video>`. GitHub Pages may return HTTP 200 for `mp4v` files, but they still won't play.

Re-encode with `ffmpeg` (done automatically by the prepare script):

```bash
ffmpeg -i input.mp4 -c:v libx264 -pix_fmt yuv420p -preset medium -crf 23 \
  -movflags +faststart -an output.mp4
```

### 7. Commit and deploy

```bash
git add static/task_examples_ours/ index.html
git commit -m "Update task rollout videos"
git push origin main
```

Check the **Actions** tab for a green deploy, then verify videos on the live site.

---

## Quick path (automated)

```bash
python scripts/find_task_examples.py   # tmp/ → draft.md (distinct scenes)
python scripts/prepare_task_videos.py  # draft.md → static/ + index.html
```

Requires `ffmpeg` and `ffprobe`. `prepare_task_videos.py`:

1. Reads `draft.md`
2. Copies videos to `static/task_examples_ours/<task>/<jobN>/`
3. Re-encodes to H.264
4. Updates rollout sections in `index.html`

Then commit and push (step 7 above).

If you add a new task, update `VIS_PREFIX_TO_TITLE` in `find_task_examples.py` and `TASK_META` in `prepare_task_videos.py`.

### Re-encode only (no copy)

If you manually copied MP4s and only need the codec fix:

```bash
python scripts/reencode_videos_for_web.py
```

### Verify encoding

```bash
ffprobe -v error -select_streams v:0 \
  -show_entries stream=codec_name,codec_tag_string \
  -of default=noprint_wrappers=1 \
  static/task_examples_ours/group_color/job0/custom_group_color_0_0_success.mp4
```

Expected for web-ready files:

```
codec_name=h264
codec_tag_string=avc1
```

### Preview locally

```bash
python3 -m http.server 8000
# open http://localhost:8000
```

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/find_task_examples.py` | Scan `tmp/` and write `draft.md` (N successes, distinct scenes) |
| `scripts/prepare_task_videos.py` | draft → copy → re-encode → update HTML |
| `scripts/reencode_videos_for_web.py` | Re-encode existing files under `static/task_examples_ours/` |
