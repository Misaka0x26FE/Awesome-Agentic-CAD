# Benchmarks and evidence

This document records what public evaluations actually measure, what the numbers mean, and where they stop being comparable.

---

## 1. Metric definitions

| Metric | Definition | Direction | Failure mode |
|---|---|---|---|
| **CD** (Chamfer Distance) | Bidirectional mean nearest-neighbor distance between 30k sampled points, unit bbox normalized, ×10³ | lower | surface similarity without topology/feature correctness |
| **IR** (Invalidity Rate) | fraction of samples that fail to execute, time out (60 s), or produce empty/degenerate geometry | lower | syntax-valid but geometrically wrong outputs pass |
| **IoU** | volumetric overlap of 256³ voxelizations | higher | coarse shape agreement, insensitive to small features |
| **Validity gate** | B-rep watertight + meshable into a closed manifold | boolean | binary; a single self-intersection zeroes the score |
| **Betti match** | `(b0, b1, b2)` equality with ground truth | boolean | topology, not dimensions |
| **PF1 / CF1** | primitive / constraint F1 on sketches | higher | constraint semantics |
| **Executability** | fraction of API call sequences that run without error | higher | running ≠ solving |
| **Valid target** | target value computed and within tolerance | higher | default-value coincidences |
| **Success rate** | end-to-end task pass, including solver and graph checks | higher | depends on stage gating |
| **Joint test success** | generated tests both pass reference and catch injected faults | higher | tests may be vacuous |

**Rule:** never report IR without CD/IoU, and never report CD/IoU without IR. The pair is the minimum.

---

## 2. Text2CAD-Bench

- Scale: 600 CAD examples, 1,200 prompts, L1–L4.
- Execution: CadQuery 2.4, isolated Python 3.10, up to 3 error-feedback retries, best-of.
- Metrics: CD, IR, IoU; L4 uses a VLM judge over 8 rendered views.

| Model | L1 CD | L1 IR | L1 IoU | L3 CD | L3 IR | L3 IoU |
|---|---:|---:|---:|---:|---:|---:|
| GPT-5.2 | 44.31 | 11.1% | 0.59 | 93.46 | 68.0% | 0.23 |
| Claude-4.5-Sonnet | 52.62 | 20.3% | 0.54 | 70.13 | 70.0% | 0.25 |
| DeepSeek-V3.2 | 53.15 | 13.3% | 0.54 | 101.23 | 69.0% | 0.17 |
| Qwen3-max | 84.54 | 21.4% | 0.40 | 148.58 | 92.0% | 0.07 |
| Text2CAD (domain) | 219.57 | 11.0% | 0.08 | 234.00 | 2.0% | 0.04 |

Interpretation:

- L2→L3 is the cliff: sweep, loft, shell raise IR from ~15% to 70–90%.
- Domain-specific models can minimize IR while maximizing CD; this is the canonical **executability–fidelity decoupling**.
- Prompt style interacts with complexity: geometric descriptions win on L1–L2; sequence descriptions win on L3.

---

## 3. CADGenBench

- 81 fixtures: 49 generation, 32 editing.
- Validity gate: invalid solid → 0.
- Weighted score: geometric similarity, mating-feature correctness (keep-in/keep-out sub-volumes), topology match (Betti numbers).
- Public leaderboard snapshot 2026-08-27:

| Entry | Aggregate | Validity | Generation | Editing |
|---|---:|---:|---:|---:|
| Opus 5 + MCP + drawing evidence | 0.6771 | 98.77% | 0.658 | 0.706 |
| build123d-mcp + Opus 5 | 0.6391 | 98.77% | 0.596 | 0.706 |
| Opus 5 baseline, no MCP | 0.6268 | 92.59% | 0.631 | 0.621 |
| GPT-5.6 Sol + Claude Code | 0.5745 | 100% | 0.501 | 0.687 |
| Qwen3.8-max | 0.4363 | 95.06% | 0.344 | 0.578 |

Observations:

- MCP raises validity and editing score, not necessarily raw generation score.
- 0.68 aggregate still leaves roughly one third of weighted objectives unmet.
- Fixtures are synthetic; real assemblies add contact, tolerances, and standard parts.

---

## 4. CAD-Assistant (tool-augmented VLLM)

- 1,700 FreeCAD test parts from SGPBench (700 2D, 1,000 3D).
- Tools: Python, FreeCAD API, sketch parameterizer, sketch/solid recognizer, constraint checker, cross-section extractor.
- Zero-shot; no fine-tuning.

| Task | Metric | CAD-Assistant | GPT-4o baseline |
|---|---|---:|---:|
| 2D CAD QA | accuracy | 0.791 | 0.686 |
| 3D CAD QA | accuracy | 0.857 | 0.782 |
| Auto-constraining | PF1 / CF1 | 0.979 / 0.484 | 0.693 / 0.274 |
| Hand-drawn parameterization | CD | 0.680 | 1.184 |

Ablation: adding the constraint checker moves PF1 from 0.747 to 0.979. The tool that verifies geometric consequence is worth more than a larger planner.

---

## 5. FEABench

- Gold: 15 manually verified problems; Large: 200 parsed problems.
- Interface: COMSOL Java API.
- Metrics: executability, model-tree score, valid target, strict relative error.

| Strategy | Executability | Valid target |
|---|---:|---:|
| Claude 3.5 one-shot | 0.79 | 1/15 |
| GPT-4o one-shot | 0.78 | 0/15 |
| Gemini 1.5 Pro one-shot | 0.60 | 0/15 |
| Multi-turn agent | 0.88 | 2/15 |

The only strict pass produced 19.999 °C against a target of 18.3 °C — the COMSOL default temperature. This is a benchmark-level warning: numeric agreement can come from an unsolved model.

---

## 6. FEM-Bench 2025

- 33 tasks from a first graduate computational mechanics course.
- Two axes: function correctness, unit-test quality.
- Five runs per task for the top models.

| Metric | Best result |
|---|---|
| Function correctness, any of 5 | Gemini 3 Pro: 30/33 |
| Function correctness, 5/5 | Gemini 3 Pro: 26/33 |
| Joint test success | GPT-5: 73.8% |

No model completed all 33. Failures concentrate in geometric stiffness, elastic critical load, and geometric nonlinearity without helper functions.

---

## 7. MecEng

- 84 tasks, three levels; 32 open-weight + 2 proprietary LLMs.
- Pipeline: text → part geometry (Netgen) → tet mesh → Hurty–Craig–Bampton reduction → Exudyn multibody model.
- Verification: system-graph isomorphism, numerical solution, mass/geometry, eigenfrequencies.

| Model group | Rigid-body success |
|---|---:|
| Claude-Opus-4.8 | 91.4% |
| GPT-5.2 | 86.0% |
| Best open-weight (qwen3.6:27b) | 82.1% |
| Top-8 open-weight mean | 73.0% |
| All-32 open-weight mean | 37.1% |

Two findings matter more than the averages:

1. **Executable but physically wrong: 17.1%** of tasks (top-8 open-weight mean). Solver exits cleanly; joints/contacts/parameters are wrong.
2. **Chamfer edge assignment** is a recurring failure: selecting the correct edge for a chamfer defeats otherwise strong models.

---

## 8. SCBench

- 22 tasks, 285 subtasks; axiomatic, constructive, planning.
- Deterministic verifiers and physics simulators.

| Model | Overall |
|---|---:|
| Gemini 3 Pro Preview | 57.6% |
| GPT-5.2 | 57.6% |
| Claude Sonnet 4.5 | 34.9% |

Failure taxonomy: **Local-Only** dominates — locally plausible geometry that violates a global constraint. Tools shift the distribution of failure modes but do not remove the global-consolidation gap.

---

## 9. EngiBench and EngiAI

EngiBench (ACL Findings 2026):

- three levels: knowledge retrieval, contextual reasoning, open modeling;
- three variants: perturbed, knowledge-enhanced, math-abstracted;
- accuracy decreases with complexity, degrades under perturbation, and stays below human experts on open design.

EngiAI (2026-08) decomposes agent capability:

| Capability | Result |
|---|---|
| Workflow execution, Beams2D | closed 96–97%, open 55–78% |
| Workflow execution, Photonics2D | 20–53% |
| Retrieval-assisted parameter selection | improves, not uniformly |
| HPC orchestration | Gemini-3-Flash all; GPT-5-mini 50–70% |
| Training-code authoring | reliable for small gaps, diverges for large ones |

---

## 10. Engineering drawings

MechVQA (ICML 2026): 3,281 drawings, 21K QA, 10 tasks.

| Model | Total |
|---|---:|
| MechVL-4B-RL (domain RL) | 84.85 |
| GLM-4.6V | 78.91 |
| Gemini-3-Pro-Preview | 77.28 |
| GPT-5 | 75.44 |

Subtask spread for general models: title block/table ≈ 97.73%, multi-view ≈ 58%, assembly ≈ 46%.

GD&T extraction (A*STAR/NTU, 400 drawings):

| Model | Recall | Wrong among returned |
|---|---:|---:|
| GPT-4o | 25.39% | 40.97% |
| Claude 3.5 Sonnet | 37.27% | 55.99% |

LED-BENCH (2026-10): 107 large-format sheets, 377 questions; best domain average 52.65% (GPT-5.6 Sol), mechanical 58.81%.

Elector vs Claude Opus 4.8 (486 annotated entities):

| Metric | Claude | Elector |
|---|---:|---:|
| Dimension detection F1 | 0.237 | 0.476 |
| GD&T detection F1 | 0.214 | 0.417 |
| Info-block CER | 1.48 | 0.45 |

---

## 11. Threats to validity

1. **Harness sensitivity.** Same benchmark, different tool set, retries, and prompt can move aggregate scores by 10–20 points.
2. **Survivorship bias.** CD/IoU computed only on executed samples inflate quality when IR is high.
3. **Retry budget.** Best-of-3 or best-of-5 is not single-shot capability.
4. **Judge models.** VLM judges correlate with humans but are not ground truth.
5. **Sample size.** FEABench Gold has 15 problems; one problem is 6.7 percentage points.
6. **Contamination.** Public CAD datasets may overlap with pretraining data.
7. **Version drift.** Model aliases and tool versions change without notice.
8. **Synthetic fixtures.** Benchmark parts are simpler than production assemblies.

---

## 12. Evidence grading

| Grade | Criteria | Examples |
|---|---|---|
| **A** | deterministic verifier, public data, ≥ 100 samples, independent replication | FEM-Bench (33 tasks, 5 runs), Text2CAD-Bench (600/1,200) |
| **B** | deterministic verifier, public data, < 100 samples or single run | FEABench Gold (15), CADGenBench (81) |
| **C** | LLM judge or human rubric, moderate sample | MechVQA L4, EngiBench L3 |
| **D** | vendor/self-reported, no harness disclosure | leaderboard submissions without validation |

Cite the grade with the number.

---

## 13. Reporting template

```
benchmark: <name> <version>
model: <exact id and effort>
harness: <tool set, retries, prompt>
n: <samples>
metrics: <metric=value; metric=value>
validity: <rate>
artifacts: <repo/commit>
```

A claim without this block is an anecdote.

---

## 14. References

- Text2CAD-Bench: <https://arxiv.org/html/2605.18430>
- CADGenBench: <https://github.com/huggingface/cadgenbench> · <https://benchmarklist.com/benchmarks/cadgenbench/>
- CAD-Assistant: <https://cadassistant.github.io/>
- FEABench: <https://arxiv.org/abs/2504.06260>
- FEM-Bench: <https://doi.org/10.1007/s00366-026-02397-z>
- MecEng: <https://arxiv.org/abs/2608.14615>
- SCBench: <https://arxiv.org/html/2604.09594v1>
- EngiBench: <https://aclanthology.org/2026.findings-acl.1810/>
- EngiAI: <https://arxiv.org/html/2605.19743v3>
- MechVQA: <https://arxiv.org/html/2605.30794v2>
- LED-BENCH: <https://arxiv.org/html/2610.19571>
- GD&T study summary: <https://yardwork.dev/en/blog/ai-technical-drawings>
- Elector: <https://www.calibras.dk/2026/02/10/elector-an-end-to-end-system-for-engineering-drawing-understanding/>
