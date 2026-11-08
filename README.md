<a id="top" name="top"></a>

<div align="center">
  <img src="assets/banner.svg" alt="Awesome Agentic CAD — tools, agent interfaces, benchmarks, and failure modes for LLM-driven CAD/CAE" width="100%">
</div>

<div align="center">

**English** · [简体中文](README.zh-CN.md)

[![Awesome](https://img.shields.io/badge/awesome-agentic--cad-0ea5e9?style=flat-square)](#)
[![License: MIT](https://img.shields.io/github/license/Misaka0x26FE/Awesome-Agentic-CAD?style=flat-square&color=22c55e)](LICENSE)
[![Last commit](https://img.shields.io/github/last-commit/Misaka0x26FE/Awesome-Agentic-CAD?style=flat-square&color=8b5cf6)](https://github.com/Misaka0x26FE/Awesome-Agentic-CAD/commits/main)
[![Stars](https://img.shields.io/github/stars/Misaka0x26FE/Awesome-Agentic-CAD?style=flat-square&color=f59e0b)](https://github.com/Misaka0x26FE/Awesome-Agentic-CAD)
[![PRs welcome](https://img.shields.io/badge/PRs-welcome-22c55e?style=flat-square)](CONTRIBUTING.md)

</div>

> **A technical index of open and closed tools, agent interfaces, evaluation evidence, and failure modes for LLM-driven CAD/CAE.**
>
> Scope: parametric B-rep authoring, geometry preparation, meshing, structural/thermal/multiphysics solving, post-processing, topology optimization, and the agent surfaces that bind them.
>
> Status: living document. Every entry lists source, license, agent surface, and headless capability. Claims are tagged with their evidence level.

<table>
  <tr>
    <td align="center"><b>36</b><br/><sub>agent projects</sub></td>
    <td align="center"><b>9</b><br/><sub>benchmarks</sub></td>
    <td align="center"><b>12</b><br/><sub>failure modes</sub></td>
    <td align="center"><b>6</b><br/><sub>guides</sub></td>
    <td align="center"><b>169</b><br/><sub>links checked</sub></td>
  </tr>
</table>

> **Read this if** you are building an agent that must produce a manufacturable STEP file, a converged solve, and an auditable trail — not a screenshot.

## Contents

- [Definition](#1-definition)
- [Layer model](#2-layer-model)
- [Capability envelope](#3-capability-envelope-evidence-based)
- [Agent interface patterns](#4-agent-interface-patterns)
- [Reference architecture](#5-reference-architecture)
- [Tool catalog](#6-tool-catalog)
- [Agent ecosystem](#61-agent-ecosystem)
- [Evaluation evidence](#7-evaluation-evidence)
- [Limitations](#8-limitations)
- [Repository layout](#9-repository-layout)
- [Contributing](#10-contributing)
- [License](#11-license)
- [References](#12-references)

---

## 1. Definition

**Agentic CAD** is a closed control loop over a geometric state, not a natural-language front end to a CAD GUI.

```
s_t = (B_t, G_t, M_t, P_t, R_t)
a_t ~ π(· | s_t, h_t)
s_{t+1} = T(s_t, a_t)
V(s_{t+1}) -> {accept, reject, rollback}
```

| Symbol | Meaning | Machine-readable form |
|---|---|---|
| `B` | B-rep solid/assembly | STEP AP242, BREP, XBF |
| `G` | Assembly graph: instances, mates, contact pairs | JSON: `{instance, definition, transform, interfaces[]}` |
| `M` | Volume/surface mesh + quality fields | `.msh`, `.inp`, `.med`, `.vtk` |
| `P` | Solver model: materials, BCs, loads, step controls | `.inp`, `.comm`, `.sif`, JSON |
| `R` | Results + convergence metadata | `.frd`, `.dat`, `.vtu`, JSON |
| `V` | Deterministic verifier | Python/CLI, exit code + JSON report |

A system qualifies as agentic only if **`V` is executable and its verdict gates the next action**. Without `V`, the system is a code generator with a chat interface.

### 1.1 Invariants

Any transition must preserve a task-specific invariant set `I`:

- `watertight(B) = true`, `is_valid(B) = true`, `n_solids ≥ 1`;
- `|ΔV| / V_0 ≤ ε_v`, `|Δm| / m_0 ≤ ε_m`;
- contact set `C` preserved: `C_new ⊇ C_required`, `|C_new \ C_0| = 0` unless declared;
- mesh gate: `minSICN ≥ q_min`, `n_bad ≤ n_bad,0`;
- solver gate: `converged = true`, `residual ≤ tol`, `n_iter < n_max`;
- unit and datum consistency: `unit_system`, `datum_frame`, `tolerance_stack`.

An agent that cannot evaluate `I` cannot be trusted with `T`.

---

## 2. Layer model

| Layer | Responsibility | Open reference implementations | Closed reference implementations |
|---|---|---|---|
| L0 Geometry kernel | B-rep evaluation, booleans, fillets, defeaturing | OCCT / OCP | Parasolid, ACIS, CGM, ShapeManager |
| L1 Authoring | Features, sketches, assemblies, drawings | FreeCAD, build123d, CadQuery | SolidWorks, NX, Creo, CATIA, Inventor, Solid Edge, Fusion, Onshape |
| L2 Preparation | Healing, simplification, feature recognition | OCCT, Analysis Situs, Salome GEOM | SpaceClaim, DesignModeler, ANSA, CADdoctor |
| L3 Meshing | Tet/hex/boundary layer, quality metrics | Gmsh, Netgen, TetGen, MMG | ANSYS Meshing, HyperMesh, ANSA, STAR-CCM+ |
| L4 Solving | Structural, thermal, modal, explicit, CFD, multibody | CalculiX, Code_Aster, Elmer, FEniCSx, MOOSE, FreeFEM, OpenFOAM, MBDyn, Chrono | ANSYS Mechanical/Fluent, Abaqus, Nastran, COMSOL, Simcenter, LS-DYNA |
| L5 Post | Field visualization, extraction, reporting | ParaView, PyVista, meshio, ccx2paraview | CFD-Post, Tecplot, EnSight, HyperView |
| L6 Agent surface | Tool exposure, state, verification, rollback | freecad-mcp, build123d-mcp, agentcad, cadgen, PyAnsys MCP, PrePoMax MCP | vendor copilots / proprietary APIs |

The layer boundary is a **process boundary** where possible. GPL tools (Gmsh, CalculiX, Code_Aster, OpenFOAM) are invoked as subprocesses; permissively licensed libraries (build123d, CadQuery, meshio, PyVista) are imported in-process.

---

## 3. Capability envelope (evidence-based)

Reliability bands are derived from public benchmarks; see [`docs/benchmarks.md`](docs/benchmarks.md) for scales, metrics, and caveats.

| Task | Current band | Dominant failure | Evidence |
|---|---|---|---|
| Parametric part from text (simple primitives) | **High**: validity > 90%, CD ≈ 44–53, IoU ≈ 0.54–0.59 | dimensional drift, missing features | Text2CAD-Bench L1 |
| Parametric part with sweep/loft/shell | **Low**: invalidity 68–93% | kernel operation misuse, degenerate sections | Text2CAD-Bench L3 |
| Edit existing B-rep | **Medium**: 0.62–0.71 editing score | reference drift, feature reordering | CADGenBench editing split |
| Constraint inference on sketches | **Medium-high**: PF1 0.979, CF1 0.484 | conflicting constraints, over-constraint | CAD-Assistant / SketchGraphs |
| FEA model setup end-to-end | **Low**: 2/15 valid targets at 0.88 executability | BC/material/contact semantics | FEABench Gold |
| FEM kernel code | **High for linear**, low for nonlinear | geometric stiffness, buckling, finite rotation | FEM-Bench 2025 |
| Rigid multibody from text | **High**: 86–91% success | parameter selection, joint limits | MecEng L1–L2 |
| Flexible multibody from text | **Low**: chain of geometry → tet mesh → MOR | any single-stage error aborts the chain | MecEng L3 |
| Engineering drawing QA | **Split**: title block ≈ 97%, assembly ≈ 46% | projection rules, GD&T semantics | MechVQA |
| GD&T extraction | **Low**: recall 25–37%, precision 41–56% wrong | symbol vocabulary, datum references | A*STAR 400-drawing study |
| Long-horizon agent workflow | **Medium**: 96–97% closed / 55–78% open on one problem; 20–53% cross-domain | tool orchestration, retrieval, HPC state | EngiAI |

---

## 4. Agent interface patterns

Four patterns, ordered by determinism and blast radius.

| Pattern | Transport | State | Typical tools | Risk |
|---|---|---|---|---|
| **MCP / JSON-RPC** | stdio or Streamable HTTP | server-held session | freecad-mcp, build123d-mcp, PyMechanical-MCP | tool allowlist, auth, prompt injection |
| **In-process Python API** | function call | process memory | build123d, OCP, gmsh, PyVista | kernel crash kills the agent process |
| **CLI + artifact contract** | fork/exec | filesystem | FreeCADCmd, gmsh, ccx, FreeFEM, ParaView | exit-code ambiguity, partial outputs |
| **File exchange** | shared volume | none | STEP, BREP, `.inp`, `.frd`, `.med`, `.vtu` | schema drift, unit loss, silent healing |

### 4.1 MCP configuration (stdio)

```json
{
  "mcpServers": {
    "freecad": {
      "command": "uvx",
      "args": ["freecad-mcp"]
    },
    "build123d": {
      "command": "uv",
      "args": ["tool", "run", "--python", "3.12", "build123d-mcp@latest"]
    },
    "mechanical": {
      "command": "ansys-mechanical-mcp"
    }
  }
}
```

MCP semantics that matter for CAD:

- `tools/list` is a capability contract; cache it and hash it for reproducibility;
- `tools/call` must return **structured content** (JSON) plus optional image content, not prose;
- long operations need progress notifications and cancellation;
- session state must be explicit: document id, active body, selection set, undo depth.

### 4.2 CLI contract

Every CLI wrapper should emit a single JSON object on stdout and use exit codes:

| Exit | Meaning | Agent action |
|---|---|---|
| 0 | success, artifacts written | verify artifacts |
| 2 | invalid input / schema error | repair arguments |
| 3 | geometric failure (non-manifold, boolean failure) | rollback, adjust parameters |
| 4 | meshing failure / quality gate | remesh or simplify |
| 5 | solver non-convergence | adjust controls, do not accept results |
| 6 | external dependency missing | stop, report environment |

### 4.3 Verification loop

```python
state = load_step("part.step")
report = audit(state)                      # mass props, validity, topology
if not report.ok:
    raise GeometryRejected(report)

mesh = gmsh_mesh(state, size=2.0)
if mesh.min_sicn < 0.10:
    state = simplify(state, rules="defeature")
    mesh = gmsh_mesh(state, size=2.0)

job = write_inp(state, mesh, material, bc)
res = run_ccx(job, timeout=1800)
if not res.converged:
    rollback()
else:
    assert abs(res.f1 - ref.f1) / ref.f1 < 0.10
```

The verifier is the product. The model is replaceable.

---

## 5. Reference architecture

```
┌──────────────────────────────────────────────────────────────┐
│ agent (LLM)                                                  │
│  plan → emit action → read structured observation → repair   │
└───────────────┬──────────────────────────────────────────────┘
                │ MCP / Python / CLI
┌───────────────▼──────────────────────────────────────────────┐
│ tool layer                                                   │
│  build123d / FreeCAD / OCP  →  STEP                          │
│  OCP audit + Defeaturing    →  simplified STEP + report.json │
│  Gmsh                       →  mesh.msh + quality.json       │
│  CalculiX / Code_Aster      →  job.inp / job.comm            │
│  ccx2paraview / PyVista     →  fields.vtu + render.png       │
└───────────────┬──────────────────────────────────────────────┘
                │ artifacts + hashes
┌───────────────▼──────────────────────────────────────────────┐
│ verifier layer (deterministic, no LLM)                       │
│  validity | mass | contact | mesh quality | residual | delta │
│  accept → commit; reject → rollback to last checkpoint       │
└──────────────────────────────────────────────────────────────┘
```

Design rules:

1. **Single writer per document.** FreeCAD `App::Document` and most kernels are not concurrency-safe.
2. **Checkpoint before mutation.** Store `(STEP, JSON state, hash)` tuples; rollback is file restore, not undo.
3. **Observe numerically and visually.** Screenshots catch rigid-body displacement; mass properties catch scale errors. Neither alone is sufficient.
4. **Pin versions.** Kernel, mesher, solver, and model versions enter the reproducibility hash.
5. **Separate GPL processes.** Do not link GPL solvers into a distributed binary; invoke via `subprocess` with an artifact contract.

---

## 6. Tool catalog

Full tables with source, license, function, and agent surface: [`docs/tool-catalog.md`](docs/tool-catalog.md).

Highlights:

- **Geometry**: FreeCAD 1.1.x, build123d 0.13, CadQuery 2.8, OCCT/OCP 8.0.
- **Meshing**: Gmsh 4.15.2, Netgen/NGSolve 6.2, TetGen, MMG.
- **Solving**: CalculiX 2.23, Code_Aster 17.4 / Salome-Meca 2025.1, Elmer, FEniCSx, MOOSE 5.0, FreeFEM 4.17, OpenFOAM, MBDyn, Chrono.
- **Post**: ParaView 5.11, PyVista, meshio, ccx2paraview.
- **Agent surfaces**: freecad-ai (64 tools), freecad-mcp (17 tools), build123d-mcp (38 tools), agentcad, cadgen, PyAnsys MCP (Mechanical 28 tools, MAPDL, Fluent 20 tools), PrePoMax 3.0 MCP.
- **Closed**: SolidWorks, NX, Creo, CATIA, Inventor, Solid Edge, Fusion, Onshape, SpaceClaim, ANSYS, Abaqus, COMSOL, Simcenter, HyperMesh, ANSA, SimScale, CAD Exchanger, Datakit.

### 6.1 Agent ecosystem

A separate catalog of MCP servers and agent-native CAD projects, filtered by stars and maintenance: [`docs/agent-ecosystem.md`](docs/agent-ecosystem.md).

| Direction | Leader | Stars | Interface |
|---|---|---:|---|
| FreeCAD | `neka-nat/freecad-mcp` | 3,254 | stdio MCP + XML-RPC |
| SolidWorks | `wzyn20051216/solidworks-automation-skill` | 1,867 | MCP + skill |
| Text-to-CAD | `earthtojake/text-to-cad` | 25,810 | CLI + MCP |
| Abaqus | `Cai-aa/abaqus-mcp` | 326 | MCP + plugin |
| COMSOL | `wjc9011/COMSOL_Multiphysics_MCP` | 944 | MCP |
| CAE orchestration | `Cai-aa/CAE-Agent-Hub` | 1,297 | MCP + skills |

Thresholds: ≥ 200 stars for popular directions (FreeCAD, SolidWorks, text-to-CAD, general CAD MCP); ≥ 100 for niche directions (CATIA, NX, Onshape, Fusion, code-CAD, CAE solvers).

---

## 7. Evaluation evidence

Summary and metric definitions: [`docs/benchmarks.md`](docs/benchmarks.md).

Headline numbers, with harness caveats:

| Benchmark | Scale | Best public result | What it measures |
|---|---|---|---|
| Text2CAD-Bench | 600 CAD / 1,200 prompts | L1 CD 44.31, IR 11.1%, IoU 0.59; L3 IR 68–93% | text → CadQuery code |
| CADGenBench | 81 fixtures | 0.677 aggregate, 98.77% validity | validity-gated generation + editing |
| CAD-Assistant | 1,700 test parts | 2D 0.791, 3D 0.857, CF1 0.484 | tool-augmented VLLM over FreeCAD |
| FEABench | 15 Gold + 200 Large | 0.88 executability, 2/15 valid target | COMSOL API end-to-end |
| FEM-Bench 2025 | 33 tasks | 30/33 any-pass, 26/33 5/5 | FEM code + tests |
| MecEng | 84 tasks, 34 LLMs | 91.4% rigid / much lower flexible | multibody model synthesis |
| SCBench | 285 subtasks | 57.6% | spatial constraint satisfaction |
| MechVQA | 3,281 drawings / 21K QA | 84.85% domain-tuned; 77.28% general | drawing understanding |
| EngiAI | 2 design problems | 96–97% closed / 55–78% open | tool-connected workflow |

**Do not compare across harnesses.** Report `(model, harness, retries, n_samples, benchmark_version)` together.

---

## 8. Limitations

Full analysis: [`docs/limitations.md`](docs/limitations.md).

1. **Validity ≠ fidelity.** A watertight solid can be dimensionally wrong.
2. **Global constraint consolidation.** Local geometry is plausible; global invariants fail.
3. **Physical semantics.** Boundary conditions, materials, and contact are under-specified and often wrong.
4. **Topological naming.** Persistent references to faces/edges break under parametric rebuild.
5. **Error propagation.** Geometry → mesh → solver is multiplicative; one stage failure aborts the chain.
6. **Harness non-comparability.** Same benchmark, different scores.
7. **Data scarcity and IP.** Real assemblies, standards, and validation cases are not public.
8. **Determinism and version drift.** Model, kernel, and tool versions change outputs.
9. **Cost and latency.** Iterative loops multiply token and compute cost.
10. **Security.** `execute_code` is arbitrary code execution; drawings and STEP metadata are untrusted input.
11. **Qualification.** No public evidence that LLM-generated models satisfy code/regulatory acceptance.
12. **Responsibility.** The human remains the license holder and signatory.

---

## 9. Repository layout

| Path | Contents |
|---|---|
| [`README.md`](README.md) · [`README.zh-CN.md`](README.zh-CN.md) | Scope, layer model, capability envelope, interface patterns, reference architecture |
| [`docs/tool-catalog.md`](docs/tool-catalog.md) | Open and closed tools with version, license, source, function, agent surface, headless capability |
| [`docs/agent-ecosystem.md`](docs/agent-ecosystem.md) | 36 MCP servers and agent-native CAD projects, filtered by stars and maintenance |
| [`docs/agent-interfaces.md`](docs/agent-interfaces.md) | MCP/CLI/Python/file contracts, error taxonomy, verification gates, sandboxing |
| [`docs/benchmarks.md`](docs/benchmarks.md) | Metric definitions, benchmark results, threats to validity, evidence grading |
| [`docs/limitations.md`](docs/limitations.md) | 12 failure mechanisms with observables, mitigations, and residual risk |
| [`docs/reference-architecture.md`](docs/reference-architecture.md) | State machine, JSON schemas, rollback, determinism, anti-patterns |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | Inclusion criteria, star thresholds, evidence format, PR checklist |
| [`scripts/check_links.py`](scripts/check_links.py) | Link checker; 404/410 are hard failures, bot blocks are warnings |

---

## 10. Contributing

Inclusion criteria, evidence requirements, and PR format: [`CONTRIBUTING.md`](CONTRIBUTING.md).

Short version:

- open tools must have a public source repository and an OSI license;
- closed tools must have a public product page and a documented automation surface;
- every entry needs `source`, `license`, `function`, `agent surface`, `headless`;
- benchmark claims need `benchmark`, `version`, `n`, `metric`, `harness`;
- links are checked by `scripts/check_links.py`.

---

## 11. License

MIT. See [`LICENSE`](LICENSE).

---

## 12. References

- Text2CAD-Bench: <https://arxiv.org/html/2605.18430>
- CADGenBench metrics: <https://github.com/huggingface/cadgenbench/blob/main/docs/metrics.md>
- CAD-Assistant: <https://cadassistant.github.io/>
- FEABench: <https://arxiv.org/abs/2504.06260>
- FEM-Bench: <https://doi.org/10.1007/s00366-026-02397-z>
- MecEng: <https://arxiv.org/abs/2608.14615>
- SCBench: <https://arxiv.org/html/2604.09594v1>
- MechVQA: <https://arxiv.org/html/2605.30794v2>
- EngiBench: <https://aclanthology.org/2026.findings-acl.1810/>
- EngiAI: <https://arxiv.org/html/2605.19743v3>
- Autodesk AI Pulse 2026: <https://www.autodesk.com/design-make/articles/2026-ai-pulse>
- McKinsey State of AI 2026: <https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai>

---

## Star history

<a href="https://star-history.com/#Misaka0x26FE/Awesome-Agentic-CAD&Date">
  <img src="https://api.star-history.com/svg?repos=Misaka0x26FE/Awesome-Agentic-CAD&type=Date" alt="Star history chart">
</a>

---

<div align="center">
<sub>Built for engineers who need evidence, not demos. · <a href="#top">Back to top</a></sub>
</div>
