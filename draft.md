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
Ivan Zhang: https://enspikondplusplus.github.io/
Limin Wei: https://www.linkedin.com/in/liminwei/
Zackory Erickson: https://zackory.com/
Aviral Kumar: https://aviralkumar2907.github.io/

# Side bar
Below shows the titles and subtitles of each section in the side bar, but full title in main content might be different.
- Abstract
- Method (full title: R^3: Robotic Reasoners via Reinforcement Learning)
    - Hierarchical policy for long-horizon manipulation
    - Two-stage Training Framework of R^3
    - Environments (Language Table + Grocery Packing, each a paragraph + image)
- Main Results
    - Language Table
    - Grocery Packing
- Analysis
    - Inference-time reasoning matters beyond representation learning (Evidence A/B/C)
    - Understanding reasoning behaviors
    - Comparison with ECoT
- Evaluation Videos (full title: Examples of Evaluation Rollouts)
- Citation

# Main Figure
Put the two-stage training pipeline fig (`figures/workflow_v4.pdf`) under Two-stage Training Framework, not above the abstract.

# Abstract
Reasoning in language lets models spend more test-time compute on hard problems. We study whether VLMs can reason in natural language to guide low-level robot policies. R³ mid-trains a VLM on expert reasoning traces, then improves it with single-step rubric-based RL from offline action data. Instantiated on Language Table and simulated bimanual grocery packing; outperforms instruction-only imitation on both benchmarks.

# Method (full title: R^3: Robotic Reasoners via Reinforcement Learning)

## Hierarchical policy for long-horizon manipulation
High-level VLM reasons, then issues a short-horizon instruction; a frozen language-conditioned policy executes it.
Image: architecture fig (`figures/arch_v4.pdf`).

## Two-stage Training Framework of R^3
Mid-train on limited reasoning traces, then single-step RL on instruction-only data.

**Stage I.** Next-token prediction on expert reasoning. Skipped on packing.

**Stage II.** Dr.GRPO on expert instructions. LT: VLM-judge semantic match. Packing: exact string match.

## Environments
Each domain: bold name + one short paragraph + one image.

**Language Table.** 14 block-arrangement tasks; Gemini expert + pretrained policy.
**Grocery Packing.** Dual xArm-7 packing YCB objects; human teleop + π0.5 VLA.
Images side-by-side, smaller: V-shape filmstrip (`filmstrip_app_example_V`) and packing 3-view.



# Main Results
Each part only put the main takeaways / findings / results, as highlighted in the paper.
(Show result figs/tables as screenshot images; no interactive tables.)

## Language Table
- RL alone already improves the base VLM by reinforcing useful reasoning.
- Mid-training is a strong warm start and further boosts RL, especially for OOD transfer; a modest amount of reasoning data is often enough.
- R³ matches or beats instruction-only imitation on seen tasks, and significantly outperforms it on every held-out OOD task.

Image: average bar chart exposed; per-task table in a toggle (`tab:per_task_results`).

## Grocery Packing
One short paragraph, no bullets. Fold in that the recipe transfers beyond Language Table (not as its own point).
R³ (RL only) beats instruction-only IL on 12 held-out goals (47.9% vs 38.0% mean success); mid-training can be skipped.

Image: average bar chart exposed; per-goal table in a toggle (`tab:packing_results`).

# Analysis

## Inference-time reasoning matters beyond representation learning
- Explicit test-time reasoning helps beyond using reasoning only as training-time supervision.
- Evidence A: R³ improves perception and action understanding, but those gains alone do not explain the manipulation improvements.
- Evidence B: Non-reasoning policies that pre-train or co-train on reasoning still lag behind R³, especially on OOD tasks.
- Evidence C: Truncating or removing reasoning at test time on the same checkpoint causally drops success. Harder tasks elicit longer traces.

Images: pretrain/cotrain comparison (`tab:pretrain_cotrain_results`); reasoning-token figure and truncation table (placeholders if missing: `success_vs_reasoning_tokens`, `reasoning_budget_results_table`).

## Understanding reasoning behaviors
- R³ learns useful strategies: compare alternatives, self-correct, and resolve visual/historical uncertainty.
- Mid-training stabilizes the reasoning interface; RL makes reasoning more deliberate and action-oriented.
- Mid-training largely aligns the model’s instruction distribution with the expert’s. RL from the base model does not recover the expert distribution and often shifts toward a different mode; after mid-training, RL makes targeted edits and can refine an already reasonable behavior distribution.

Images (optional): reasoning examples / instruction-distribution figs from paper.

## Comparison with ECoT
- Adding ECoT-style structured state annotations generally does not help over free-form language reasoning in our setting.
- Post-hoc labeled reasoning performs comparably to reasoning recorded during data collection.

Image: ECoT comparison table screenshot (`tab:ecot_results`).

# Evaluation Videos (full title: Examples of Evaluation Rollouts)

Language Table: auto-selected first 2 successes from distinct scenes (scene_trial in filename). Jobs searched in order job0, job1, ...
Grocery packing videos: placeholder until assets are added.

## Group blocks (group)

Example trajectory 1 (job0, scene 0, trial 0): tmp/vis_vlm_qwen35_v3_1_rendered_v2/vis_group_color-qwen35_4b-grpo_v3a_S6R3_v3_1_0524_s128tj-ent0-step680-repeat12_seed200000_0618_0306/job0_seed200000/videos/custom_group_n_colors_0_0_success.mp4
Example trajectory 2 (job0, scene 1, trial 5): tmp/vis_vlm_qwen35_v3_1_rendered_v2/vis_group_color-qwen35_4b-grpo_v3a_S6R3_v3_1_0524_s128tj-ent0-step680-repeat12_seed200000_0618_0306/job0_seed200000/videos/custom_group_n_colors_1_5_success.mp4

## Make a line (line)

Example trajectory 1 (job0, scene 0, trial 0): tmp/vis_vlm_qwen35_v3_1_rendered_v2/vis_line_color-qwen35_4b-grpo_v3a_S6R3_v3_1_0524_s128tj-ent0-step680-repeat12_seed200800_0618_0306/job0_seed200800/videos/custom_make_line_n_colors_0_0_success.mp4
Example trajectory 2 (job0, scene 1, trial 8): tmp/vis_vlm_qwen35_v3_1_rendered_v2/vis_line_color-qwen35_4b-grpo_v3a_S6R3_v3_1_0524_s128tj-ent0-step680-repeat12_seed200800_0618_0306/job0_seed200800/videos/custom_make_line_n_colors_1_8_success.mp4

## Make a T-shape (T)

Example trajectory 1 (job0, scene 3, trial 10): tmp/vis_vlm_qwen35_v3_1_rendered_v2/vis_T-qwen35_4b-grpo_v3a_S6R3_v3_1_0524_s128tj-ent0-step680-repeat12_seed201600_0618_0305/job0_seed201600/videos/custom_make_T_shape_3_10_success.mp4
Example trajectory 2 (job0, scene 1, trial 3): tmp/vis_vlm_qwen35_v3_1_rendered_v2/vis_T-qwen35_4b-grpo_v3a_S6R3_v3_1_0524_s128tj-ent0-step680-repeat12_seed201600_0618_0305/job0_seed201600/videos/custom_make_T_shape_1_3_success.mp4

## Make a V-shape (V)

Example trajectory 1 (job0, scene 0, trial 0): tmp/vis_vlm_qwen35_v3_1_rendered_v2/vis_V-qwen35_4b-grpo_v3a_S6R3_v3_1_0524_s128tj-ent0-step680-repeat12_seed202400_0618_0305/job0_seed202400/videos/custom_make_V_shape_0_0_success.mp4
Example trajectory 2 (job0, scene 1, trial 0): tmp/vis_vlm_qwen35_v3_1_rendered_v2/vis_V-qwen35_4b-grpo_v3a_S6R3_v3_1_0524_s128tj-ent0-step680-repeat12_seed202400_0618_0305/job0_seed202400/videos/custom_make_V_shape_1_0_success.mp4

## Make an L-shape (L)

Example trajectory 1 (job0, scene 0, trial 1): tmp/vis_vlm_qwen35_v3_1_rendered_v2/vis_L-qwen35_4b-grpo_v3a_S6R3_v3_1_0524_s128tj-ent0-step680-repeat12_seed205600_0618_0305/job0_seed205600/videos/custom_make_L_shape_0_1_success.mp4
Example trajectory 2 (job0, scene 1, trial 2): tmp/vis_vlm_qwen35_v3_1_rendered_v2/vis_L-qwen35_4b-grpo_v3a_S6R3_v3_1_0524_s128tj-ent0-step680-repeat12_seed205600_0618_0305/job0_seed205600/videos/custom_make_L_shape_1_2_success.mp4

## Make a rectangle (rect)

Example trajectory 1 (job0, scene 5, trial 4): tmp/vis_vlm_qwen35_v3_1_rendered_v2/vis_rect-qwen35_4b-grpo_v3a_S6R3_v3_1_0524_s128tj-ent0-step680-repeat12_seed203200_0618_1217/job0_seed203200/videos/custom_make_rectangle_5_4_success.mp4
Example trajectory 2 (job0, scene 3, trial 7): tmp/vis_vlm_qwen35_v3_1_rendered_v2/vis_rect-qwen35_4b-grpo_v3a_S6R3_v3_1_0524_s128tj-ent0-step680-repeat12_seed203200_0618_1217/job0_seed203200/videos/custom_make_rectangle_3_7_success.mp4

## Group & isolate (gris)

Example trajectory 1 (job0, scene 0, trial 2): tmp/vis_vlm_qwen35_v3_1_rendered_v2/vis_gris-qwen35_4b-grpo_v3a_S6R3_v3_1_0524_s128tj-ent0-step680-repeat12_seed204000_0618_1217/job0_seed204000/videos/custom_group_isolate_0_2_success.mp4
Example trajectory 2 (job0, scene 1, trial 0): tmp/vis_vlm_qwen35_v3_1_rendered_v2/vis_gris-qwen35_4b-grpo_v3a_S6R3_v3_1_0524_s128tj-ent0-step680-repeat12_seed204000_0618_1217/job0_seed204000/videos/custom_group_isolate_1_0_success.mp4

## Make a midpoint (mid)

Example trajectory 1 (job0, scene 0, trial 0): tmp/vis_vlm_qwen35_v3_1_rendered_v2/vis_mid-qwen35_4b-grpo_v3a_S6R3_v3_1_0524_s128tj-ent0-step680-repeat12_seed204800_0618_1217/job0_seed204800/videos/custom_midpoint_0_0_success.mp4
Example trajectory 2 (job0, scene 1, trial 0): tmp/vis_vlm_qwen35_v3_1_rendered_v2/vis_mid-qwen35_4b-grpo_v3a_S6R3_v3_1_0524_s128tj-ent0-step680-repeat12_seed204800_0618_1217/job0_seed204800/videos/custom_midpoint_1_0_success.mp4

## Clear quarter (clear_qtr)

Example trajectory 1 (job0, scene 0, trial 0): tmp/vis_vlm_qwen35_v3_1_rendered_v2/vis_clear_quarter-qwen35_4b-grpo_v3a_S6R3_v3_1_0524_s128tj-ent0-step680-repeat12_seed206400_0618_0306/job0_seed206400/videos/custom_clear_region_quarter_0_0_success.mp4
Example trajectory 2 (job0, scene 1, trial 0): tmp/vis_vlm_qwen35_v3_1_rendered_v2/vis_clear_quarter-qwen35_4b-grpo_v3a_S6R3_v3_1_0524_s128tj-ent0-step680-repeat12_seed206400_0618_0306/job0_seed206400/videos/custom_clear_region_quarter_1_0_success.mp4

## Isolate in place (iip)

Example trajectory 1 (job0, scene 0, trial 0): tmp/vis_vlm_qwen35_v3_1_rendered_v2/vis_iip-qwen35_4b-grpo_v3a_S6R3_v3_1_0524_s128tj-ent0-step680-repeat12_seed207200_0618_0306/job0_seed207200/videos/custom_isolate_in_place_0_0_success.mp4
Example trajectory 2 (job0, scene 1, trial 0): tmp/vis_vlm_qwen35_v3_1_rendered_v2/vis_iip-qwen35_4b-grpo_v3a_S6R3_v3_1_0524_s128tj-ent0-step680-repeat12_seed207200_0618_0306/job0_seed207200/videos/custom_isolate_in_place_1_0_success.mp4

## Make an inverted V-shape (iV)

Example trajectory 1 (job0, scene 0, trial 0): tmp/vis_vlm_qwen35_v3_1_rendered_v2/vis_iV-qwen35_4b-grpo_v3a_S6R3_v3_1_0524_s128tj-ent0-step680-repeat12_seed208000_0618_1216/job0_seed208000/videos/custom_make_inverted_V_shape_0_0_success.mp4
Example trajectory 2 (job0, scene 1, trial 0): tmp/vis_vlm_qwen35_v3_1_rendered_v2/vis_iV-qwen35_4b-grpo_v3a_S6R3_v3_1_0524_s128tj-ent0-step680-repeat12_seed208000_0618_1216/job0_seed208000/videos/custom_make_inverted_V_shape_1_0_success.mp4

## Make an inverted L-shape (iL)

Example trajectory 1 (job0, scene 0, trial 0): tmp/vis_vlm_qwen35_v3_1_rendered_v2/vis_iL-qwen35_4b-grpo_v3a_S6R3_v3_1_0524_s128tj-ent0-step680-repeat12_seed208800_0618_1217/job0_seed208800/videos/custom_make_inverted_L_shape_0_0_success.mp4
Example trajectory 2 (job0, scene 1, trial 2): tmp/vis_vlm_qwen35_v3_1_rendered_v2/vis_iL-qwen35_4b-grpo_v3a_S6R3_v3_1_0524_s128tj-ent0-step680-repeat12_seed208800_0618_1217/job0_seed208800/videos/custom_make_inverted_L_shape_1_2_success.mp4

## Make a diagonal line (diag_line)

Example trajectory 1 (job0, scene 2, trial 5): tmp/vis_vlm_qwen35_v3_1_rendered_v2/vis_dline-qwen35_4b-grpo_v3a_S6R3_v3_1_0524_s128tj-ent0-step680-repeat12_seed209600_0618_1217/job0_seed209600/videos/custom_make_diagonal_line_2_5_success.mp4
Example trajectory 2 (job0, scene 1, trial 0): tmp/vis_vlm_qwen35_v3_1_rendered_v2/vis_dline-qwen35_4b-grpo_v3a_S6R3_v3_1_0524_s128tj-ent0-step680-repeat12_seed209600_0618_1217/job0_seed209600/videos/custom_make_diagonal_line_1_0_success.mp4

## Clear half (clear half)

Example trajectory 1 (job0, scene 0, trial 0): tmp/vis_vlm_qwen35_v3_1_rendered_v2/vis_clear_half-qwen35_4b-grpo_v3a_S6R3_v3_1_0524_s128tj-ent0-step680-repeat12_seed211200_0618_1217/job0_seed211200/videos/custom_clear_region_half_0_0_success.mp4
Example trajectory 2 (job0, scene 1, trial 0): tmp/vis_vlm_qwen35_v3_1_rendered_v2/vis_clear_half-qwen35_4b-grpo_v3a_S6R3_v3_1_0524_s128tj-ent0-step680-repeat12_seed211200_0618_1217/job0_seed211200/videos/custom_clear_region_half_1_0_success.mp4

# Citation
```
@inproceedings{wu2026r3trainingrobotsreason,
  title={$\mathcal{R}^3$: Training Robots to Reason in Natural Language via Reinforcement Learning},
  author={Lehong Wu and Yuxiao Qu and Zheyuan Hu and Ivan Zhang and Limin Wei and Zackory Erickson and Aviral Kumar},
  booktitle={Conference on Robot Learning (CoRL)},
  year={2026},
}
```
