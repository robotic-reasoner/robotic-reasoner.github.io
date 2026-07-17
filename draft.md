This is the draft for the website content and layout.
This draft include:
- structure, title, arrangement
- contents that needs to be directly copied from paper are ommitted, only new texts / summaries are written here.
- images to show. (Note: no tables are needed, even if yes, tables will be presented as screenshot images)
- any kind of layout, font, style requirements

When the draft say "see arxiv paper", please refer to `arxiv_paper` folder.


# Title
R³: Training Robots to Reason in Natural Language via Reinforcement Learning

# Author & Link & Institution
Lehong Wu, Yuxiao Qu, Zheyuan Hu, Ivan Zhang, Limin Wei, Zackory Erickson, Aviral Kumar
Carnegie Mellon University
Links: arXiv (TBD), Code (TBD)

Author's personal website link:
Lehong Wu: https://lehongwu.github.io/
Yuxiao Qu: https://cohenqu.github.io/
Zheyuan Hu: https://huzheyuan.io/
Ivan Zhang: TBD
Limin Wei: TBD
Zackory Erickson: https://zackory.com/
Aviral Kumar: https://aviralkumar2907.github.io/

# Side bar
Below shows the titles and subtitles of each section in the side bar, but full title in main content might be different.
- Abstract
- Method (full title: R^3: Robotic Reasoners via Reinforcement Learning)
    - Hierarchical policy for long-horizon manipulation (the "problem setup" part)
    - Two-stage Training Framework of R^3
- Results
    - Main results
    - Reasoning helps More than better representations
    - Understanding reasoning behaviors
    - Comparison with ECoT
- Evaluation Videos (full title: Examples of Successful Evaluation Rollouts)
- Citation

# Main Figure
Put the two-stage training pipeline fig (`figures/workflow_v3.pdf` in paper) before abstract, after institution.
Caption (brief): R³ mid-trains a VLM on expert reasoning, then improves it with single-step RL so the reasoner can steer a fixed low-level policy.

# Abstract
Reasoning in language lets models spend more test-time compute on hard problems. We study whether VLMs can reason in natural language to guide low-level robot policies. R³ mid-trains a VLM on expert reasoning traces, then improves it with single-step rubric-based RL from offline action data. On Language Table, free-form language reasoning improves exploration and generalization to unseen tasks.

# Method (full title: R^3: Robotic Reasoners via Reinforcement Learning)

## Hierarchical policy for long-horizon manipulation
This is the "problem setup" part.

- Hierarchical setup: a high-level VLM reasons and issues a short-horizon language instruction; a frozen language-conditioned low-level policy executes it.
- Image: hierarchical architecture fig (`figures/arch_v2.pdf` in paper).
- Testbed: Language Table — long-horizon block-arrangement tasks that require composing moves and reasoning about spatial relations.
- Image: show expert trajectory example (`figures/filmstrip_task_example_v2_final.pdf`) if space allows.

## Two-stage Training Framework of R^3
R³ turns expert demos into reasoning supervision in two stages.

**Stage I (mid-training).** Warm-start an off-the-shelf VLM on expert reasoning traces so it learns to reason over scene and history before emitting an instruction.
- Objective: next-token pred
- Data: expert demo with reasoning labels

**Stage II (RL).** Improve the reasoner with single-step rubric-based RL on offline instruction data (no expert reasoning needed):
- Objective: Dr.GRPO
- Data: expert demo **without reasoning labels**
- Rubric-based VLM judge (semantic match to expert instruction)
- Key design choices: history as previous response; reason over imputed prior context; filter repetitive steps to avoid reward shortcuts



# Results
Put all 4 subsections in the original arxiv paper into this website as 4 subtitles.
Each part only put the main takeaways / findings / results, as highlighted in the paper.
(Show result figs/tables as screenshot images; no interactive tables.)

## Main results
- RL alone already improves the base VLM by reinforcing useful reasoning.
- Mid-training is a strong warm start and further boosts RL, especially for OOD transfer; a modest amount of reasoning data is often enough.
- R³ matches or beats instruction-only imitation on seen tasks, and generalizes much better to OOD tasks.

Image: main results table screenshot (`tab:per_task_results`).

## Reasoning helps More than better representations
- Explicit test-time reasoning helps beyond using reasoning only as training-time supervision.
- R³ improves perception and action understanding, but those gains alone do not explain the manipulation improvements.
- Non-reasoning policies that pre-train or co-train on reasoning still lag behind R³, especially on OOD tasks.

Image: pretrain/cotrain comparison table screenshot (`tab:pretrain_cotrain_results`).

## Understanding reasoning behaviors
- R³ learns useful strategies: compare alternatives, self-correct, and resolve visual/historical uncertainty.
- Mid-training stabilizes the reasoning interface; RL makes reasoning more deliberate and action-oriented.
- Mid-training gives RL a good behavior prior; RL then refines it rather than rediscovering behaviors from scratch.

Images (optional): reasoning examples / instruction-distribution figs from paper.

## Comparison with ECoT
- Adding ECoT-style structured state annotations generally does not help over free-form language reasoning in our setting.
- Post-hoc labeled reasoning performs comparably to reasoning recorded during data collection.

Image: ECoT comparison table screenshot (`tab:ecot_results`).

# Evaluation Videos (full title: Examples of Successful Evaluation Rollouts)

Auto-selected: first 2 successes from distinct scenes (scene_trial in filename). Jobs searched in order job0, job1, ...

## Group blocks (group)

example 1 (job0, scene 0, trial 0): tmp/vis_vlm_qwen35_v3_1_rendered_v2/vis_group_color-qwen35_4b-grpo_v3a_S6R3_v3_1_0524_s128tj-ent0-step680-repeat12_seed200000_0618_0306/job0_seed200000/videos/custom_group_n_colors_0_0_success.mp4
example 2 (job0, scene 1, trial 5): tmp/vis_vlm_qwen35_v3_1_rendered_v2/vis_group_color-qwen35_4b-grpo_v3a_S6R3_v3_1_0524_s128tj-ent0-step680-repeat12_seed200000_0618_0306/job0_seed200000/videos/custom_group_n_colors_1_5_success.mp4

## Make a line (line)

example 1 (job0, scene 0, trial 0): tmp/vis_vlm_qwen35_v3_1_rendered_v2/vis_line_color-qwen35_4b-grpo_v3a_S6R3_v3_1_0524_s128tj-ent0-step680-repeat12_seed200800_0618_0306/job0_seed200800/videos/custom_make_line_n_colors_0_0_success.mp4
example 2 (job0, scene 1, trial 8): tmp/vis_vlm_qwen35_v3_1_rendered_v2/vis_line_color-qwen35_4b-grpo_v3a_S6R3_v3_1_0524_s128tj-ent0-step680-repeat12_seed200800_0618_0306/job0_seed200800/videos/custom_make_line_n_colors_1_8_success.mp4

## Make a T-shape (T)

example 1 (job0, scene 3, trial 10): tmp/vis_vlm_qwen35_v3_1_rendered_v2/vis_T-qwen35_4b-grpo_v3a_S6R3_v3_1_0524_s128tj-ent0-step680-repeat12_seed201600_0618_0305/job0_seed201600/videos/custom_make_T_shape_3_10_success.mp4
example 2 (job0, scene 1, trial 3): tmp/vis_vlm_qwen35_v3_1_rendered_v2/vis_T-qwen35_4b-grpo_v3a_S6R3_v3_1_0524_s128tj-ent0-step680-repeat12_seed201600_0618_0305/job0_seed201600/videos/custom_make_T_shape_1_3_success.mp4

## Make a V-shape (V)

example 1 (job0, scene 0, trial 0): tmp/vis_vlm_qwen35_v3_1_rendered_v2/vis_V-qwen35_4b-grpo_v3a_S6R3_v3_1_0524_s128tj-ent0-step680-repeat12_seed202400_0618_0305/job0_seed202400/videos/custom_make_V_shape_0_0_success.mp4
example 2 (job0, scene 1, trial 0): tmp/vis_vlm_qwen35_v3_1_rendered_v2/vis_V-qwen35_4b-grpo_v3a_S6R3_v3_1_0524_s128tj-ent0-step680-repeat12_seed202400_0618_0305/job0_seed202400/videos/custom_make_V_shape_1_0_success.mp4

## Make an L-shape (L)

example 1 (job0, scene 0, trial 1): tmp/vis_vlm_qwen35_v3_1_rendered_v2/vis_L-qwen35_4b-grpo_v3a_S6R3_v3_1_0524_s128tj-ent0-step680-repeat12_seed205600_0618_0305/job0_seed205600/videos/custom_make_L_shape_0_1_success.mp4
example 2 (job0, scene 1, trial 2): tmp/vis_vlm_qwen35_v3_1_rendered_v2/vis_L-qwen35_4b-grpo_v3a_S6R3_v3_1_0524_s128tj-ent0-step680-repeat12_seed205600_0618_0305/job0_seed205600/videos/custom_make_L_shape_1_2_success.mp4

## Make a rectangle (rect)

example 1 (job0, scene 5, trial 4): tmp/vis_vlm_qwen35_v3_1_rendered_v2/vis_rect-qwen35_4b-grpo_v3a_S6R3_v3_1_0524_s128tj-ent0-step680-repeat12_seed203200_0618_1217/job0_seed203200/videos/custom_make_rectangle_5_4_success.mp4
example 2 (job0, scene 3, trial 7): tmp/vis_vlm_qwen35_v3_1_rendered_v2/vis_rect-qwen35_4b-grpo_v3a_S6R3_v3_1_0524_s128tj-ent0-step680-repeat12_seed203200_0618_1217/job0_seed203200/videos/custom_make_rectangle_3_7_success.mp4

## Group & isolate (gris)

example 1 (job0, scene 0, trial 2): tmp/vis_vlm_qwen35_v3_1_rendered_v2/vis_gris-qwen35_4b-grpo_v3a_S6R3_v3_1_0524_s128tj-ent0-step680-repeat12_seed204000_0618_1217/job0_seed204000/videos/custom_group_isolate_0_2_success.mp4
example 2 (job0, scene 1, trial 0): tmp/vis_vlm_qwen35_v3_1_rendered_v2/vis_gris-qwen35_4b-grpo_v3a_S6R3_v3_1_0524_s128tj-ent0-step680-repeat12_seed204000_0618_1217/job0_seed204000/videos/custom_group_isolate_1_0_success.mp4

## Make a midpoint (mid)

example 1 (job0, scene 0, trial 0): tmp/vis_vlm_qwen35_v3_1_rendered_v2/vis_mid-qwen35_4b-grpo_v3a_S6R3_v3_1_0524_s128tj-ent0-step680-repeat12_seed204800_0618_1217/job0_seed204800/videos/custom_midpoint_0_0_success.mp4
example 2 (job0, scene 1, trial 0): tmp/vis_vlm_qwen35_v3_1_rendered_v2/vis_mid-qwen35_4b-grpo_v3a_S6R3_v3_1_0524_s128tj-ent0-step680-repeat12_seed204800_0618_1217/job0_seed204800/videos/custom_midpoint_1_0_success.mp4

## Clear quarter (clear qtr)

example 1 (job0, scene 0, trial 0): tmp/vis_vlm_qwen35_v3_1_rendered_v2/vis_clear_quarter-qwen35_4b-grpo_v3a_S6R3_v3_1_0524_s128tj-ent0-step680-repeat12_seed206400_0618_0306/job0_seed206400/videos/custom_clear_region_quarter_0_0_success.mp4
example 2 (job0, scene 1, trial 0): tmp/vis_vlm_qwen35_v3_1_rendered_v2/vis_clear_quarter-qwen35_4b-grpo_v3a_S6R3_v3_1_0524_s128tj-ent0-step680-repeat12_seed206400_0618_0306/job0_seed206400/videos/custom_clear_region_quarter_1_0_success.mp4

## Isolate in place (iip)

example 1 (job0, scene 0, trial 0): tmp/vis_vlm_qwen35_v3_1_rendered_v2/vis_iip-qwen35_4b-grpo_v3a_S6R3_v3_1_0524_s128tj-ent0-step680-repeat12_seed207200_0618_0306/job0_seed207200/videos/custom_isolate_in_place_0_0_success.mp4
example 2 (job0, scene 1, trial 0): tmp/vis_vlm_qwen35_v3_1_rendered_v2/vis_iip-qwen35_4b-grpo_v3a_S6R3_v3_1_0524_s128tj-ent0-step680-repeat12_seed207200_0618_0306/job0_seed207200/videos/custom_isolate_in_place_1_0_success.mp4

## Make an inverted V-shape (iV)

example 1 (job0, scene 0, trial 0): tmp/vis_vlm_qwen35_v3_1_rendered_v2/vis_iV-qwen35_4b-grpo_v3a_S6R3_v3_1_0524_s128tj-ent0-step680-repeat12_seed208000_0618_1216/job0_seed208000/videos/custom_make_inverted_V_shape_0_0_success.mp4
example 2 (job0, scene 1, trial 0): tmp/vis_vlm_qwen35_v3_1_rendered_v2/vis_iV-qwen35_4b-grpo_v3a_S6R3_v3_1_0524_s128tj-ent0-step680-repeat12_seed208000_0618_1216/job0_seed208000/videos/custom_make_inverted_V_shape_1_0_success.mp4

## Make an inverted L-shape (iL)

example 1 (job0, scene 0, trial 0): tmp/vis_vlm_qwen35_v3_1_rendered_v2/vis_iL-qwen35_4b-grpo_v3a_S6R3_v3_1_0524_s128tj-ent0-step680-repeat12_seed208800_0618_1217/job0_seed208800/videos/custom_make_inverted_L_shape_0_0_success.mp4
example 2 (job0, scene 1, trial 2): tmp/vis_vlm_qwen35_v3_1_rendered_v2/vis_iL-qwen35_4b-grpo_v3a_S6R3_v3_1_0524_s128tj-ent0-step680-repeat12_seed208800_0618_1217/job0_seed208800/videos/custom_make_inverted_L_shape_1_2_success.mp4

## Make a diagonal line (diag line)

example 1 (job0, scene 2, trial 5): tmp/vis_vlm_qwen35_v3_1_rendered_v2/vis_dline-qwen35_4b-grpo_v3a_S6R3_v3_1_0524_s128tj-ent0-step680-repeat12_seed209600_0618_1217/job0_seed209600/videos/custom_make_diagonal_line_2_5_success.mp4
example 2 (job0, scene 1, trial 0): tmp/vis_vlm_qwen35_v3_1_rendered_v2/vis_dline-qwen35_4b-grpo_v3a_S6R3_v3_1_0524_s128tj-ent0-step680-repeat12_seed209600_0618_1217/job0_seed209600/videos/custom_make_diagonal_line_1_0_success.mp4

## Clear half (clear half)

example 1 (job0, scene 0, trial 0): tmp/vis_vlm_qwen35_v3_1_rendered_v2/vis_clear_half-qwen35_4b-grpo_v3a_S6R3_v3_1_0524_s128tj-ent0-step680-repeat12_seed211200_0618_1217/job0_seed211200/videos/custom_clear_region_half_0_0_success.mp4
example 2 (job0, scene 1, trial 0): tmp/vis_vlm_qwen35_v3_1_rendered_v2/vis_clear_half-qwen35_4b-grpo_v3a_S6R3_v3_1_0524_s128tj-ent0-step680-repeat12_seed211200_0618_1217/job0_seed211200/videos/custom_clear_region_half_1_0_success.mp4

# Citation
```
@misc{wu2026r3roboticreasoners,
  title={R³: Training Robots to Reason in Natural Language via Reinforcement Learning},
  author={Lehong Wu and Yuxiao Qu and Zheyuan Hu and Ivan Zhang and Limin Wei and Zackory Erickson and Aviral Kumar},
  year={2026},
}
```
