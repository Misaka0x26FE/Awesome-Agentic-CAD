# Agent ecosystem: MCP servers and agent-native CAD projects

Snapshot: **2026-11-08**. Stars, licenses, and last-push dates were read from the GitHub API on that date.

---

## 1. Inclusion rules

Star counts are a popularity proxy, not a quality signal. The thresholds below are deliberately asymmetric because the size of the addressable audience differs by CAD system.

| Direction class | Examples | Threshold |
|---|---|---|
| Popular | FreeCAD, SolidWorks, text-to-CAD, general CAD MCP | **≥ 200 stars** |
| Niche | CATIA, NX, Onshape, Fusion, code-CAD, CAE solvers | **≥ 100 stars** |

Additional requirements:

- public repository with a README that states the interface;
- not archived;
- a license file or an explicit license statement (entries without one are marked `no license`);
- last push within 12 months, unless marked as historical.

Excluded on purpose: closed vendor copilots without a public automation surface, abandoned demos, and repositories whose only artifact is a prompt collection.

---

## 2. Summary

| Direction | Class | Entries ≥ threshold | Notable leader |
|---|---|---:|---|
| FreeCAD | popular | 4 | `neka-nat/freecad-mcp` (3,254) |
| SolidWorks | popular | 3 | `wzyn20051216/solidworks-automation-skill` (1,867) |
| Text-to-CAD | popular | 6 | `earthtojake/text-to-cad` (25,810) |
| General 2D CAD | popular | 2 | `daobataotie/CAD-MCP` (680) |
| Code-CAD (build123d / CadQuery) | niche | 4 | `Kai-Jungsthoefel/SOMA` (464) |
| Onshape | niche | 2 | `ReshefElisha/jarvis-onshape-mcp` (175) |
| Fusion 360 | niche | 2 | `faust-machines/fusion360-mcp-server` (145) |
| CATIA | niche | 2 | `daiemon12/catia-v5-mcp-server` (157) |
| Siemens NX | niche | 2 | `DreamEnding/NX_MCP` (165) |
| ANSYS | niche | 1 | `hongwenwang36-eng/ANSYS-Workbench-mcp` (106) |
| Abaqus | niche | 3 | `Cai-aa/abaqus-mcp` (326) |
| COMSOL | niche | 2 | `wjc9011/COMSOL_Multiphysics_MCP` (944) |
| OpenFOAM | niche | 1 | `webworn/openfoam-mcp-server` (127) |
| CAE platforms | niche | 3 | `Cai-aa/CAE-Agent-Hub` (1,297) |

---

## 3. FreeCAD

FreeCAD has the densest agent ecosystem because the Python API exposes both the document model and the GUI, and `FreeCADCmd` provides a headless path.

| Repo | Stars | License | Last push | What it is | Interface |
|---|---:|---|---|---|---|
| [`neka-nat/freecad-mcp`](https://github.com/neka-nat/freecad-mcp) | 3,254 | MIT | 2026-11-07 | Two-process MCP server: stdio MCP ↔ XML-RPC `:9875` ↔ FreeCAD GUI. 17 API-level tools including `execute_code`, `execute_code_headless`, `get_view`, `run_fem_analysis`. | stdio MCP; XML-RPC bridge |
| [`ghbalf/freecad-ai`](https://github.com/ghbalf/freecad-ai) | 619 | LGPL-2.1 | 2026-10-16 | In-workbench agent + MCP server. 64 semantic tools: bodies, sketches, primitives, fillets, booleans, assemblies, variables, `describe_model`, `measure`, undo, skills. | Streamable HTTP `:3000/mcp` |
| [`spkane/freecad-addon-robust-mcp-server`](https://github.com/spkane/freecad-addon-robust-mcp-server) | 265 | Apache-2.0 | 2026-11-07 | Addon + bridge with a PyPI package (`freecad-robust-mcp`) and Docker image; focuses on connection robustness and recoverable sessions. | stdio MCP; addon bridge |
| [`bonninr/freecad_mcp`](https://github.com/bonninr/freecad_mcp) | 228 | MIT | 2025-03-20 | Early FreeCAD MCP integration for Claude/Cursor; historically relevant, less active. | stdio MCP |

Operational notes:

- `freecad-ai` and `freecad-mcp` both mutate `App::Document` on the GUI main thread. Attach one per document at a time.
- `freecad-mcp`'s `execute_code_headless` runs heavy Python in a separate process; document mutations still return to the main thread.
- Prefer `FreeCADCmd` + scripts for CI; use MCP for interactive repair.

---

## 4. SolidWorks

SolidWorks is Windows-only and COM-based; every project below is a Windows-side bridge. None runs on Linux.

| Repo | Stars | License | Last push | What it is | Interface |
|---|---:|---|---|---|---|
| [`wzyn20051216/solidworks-automation-skill`](https://github.com/wzyn20051216/solidworks-automation-skill) | 1,867 | MIT | 2026-11-04 | "AI skill + MCP toolkit" for agent-driven desktop CAD; includes a delivery gate that rejects stale artifacts and routes low-evidence results to review. | MCP + skill package |
| [`eyfel/mcp-server-solidworks`](https://github.com/eyfel/mcp-server-solidworks) | 486 | AGPL-3.0 | 2026-10-07 | SolidPilot: intent-level CAD operations compiled through a CAD-neutral intermediate representation into SolidWorks API calls. | MCP |
| [`vespo92/SolidworksMCP-TS`](https://github.com/vespo92/SolidworksMCP-TS) | 250 | MIT | 2026-09-20 | TypeScript MCP server for SolidWorks automation; Node 20+, Windows 10/11. | MCP (stdio) |

Notes:

- AGPL-3.0 on SolidPilot matters if you distribute a derivative.
- COM automation is stateful and UI-sensitive; expect single-client serialization.
- `alisamsam/Solidworks-MCP` (199) sits one star below the popular-direction threshold and is intentionally not listed as a catalog entry.

---

## 5. Code-CAD (build123d / CadQuery)

These projects treat CAD as source code. The model is a Python program; the agent edits and executes it. This is the most reproducible agent pattern because the diff is the design history.

| Repo | Stars | License | Last push | What it is | Interface |
|---|---:|---|---|---|---|
| [`Kai-Jungsthoefel/SOMA`](https://github.com/Kai-Jungsthoefel/SOMA) | 464 | GPL-3.0 | 2026-11-04 | Desktop app for parametric modeling with a coding agent; models are CadQuery Python. | desktop + agent |
| [`jdilla1277/agentcad`](https://github.com/jdilla1277/agentcad) | 208 | Apache-2.0 | 2026-11-07 | CLI + MCP for build123d: run scripts, export STEP/STL/GLB, render PNG, inspect topology, diff versions. | CLI + MCP |
| [`PhySpace/SimpleCADAPI`](https://github.com/PhySpace/SimpleCADAPI) | 180 | Apache-2.0 | 2026-11-03 | Agent-native parametric CAD SDK; a model is a notebook of code with explicit dimensions and reconstruction. | Python SDK |
| [`pzfreo/build123d-mcp`](https://github.com/pzfreo/build123d-mcp) | 144 | Apache-2.0 | 2026-10-15 | 38 tools + 12 resources over a persistent build123d session: execute, render, measure, feature recognition, export, snapshots. | stdio / HTTP MCP |

Why this layer matters:

- every change is a text diff;
- measurement is a function call, not a screenshot;
- failed code preserves the previous session state;
- deterministic export to STEP makes downstream verification possible.

---

## 6. Text-to-CAD

| Repo | Stars | License | Last push | What it is | Interface |
|---|---:|---|---|---|---|
| [`earthtojake/text-to-cad`](https://github.com/earthtojake/text-to-cad) | 25,810 | MIT | 2026-11-08 | The `cadgen` engine: build123d-native CAD for agents, CLI + MCP + viewer, STEP/GLB/STL/3MF/DXF export, snapshots, XBF documents. | CLI + MCP |
| [`amagine-ai/Amagine3D`](https://github.com/amagine-ai/Amagine3D) | 6,282 | Apache-2.0 | 2026-10-22 | Hardware requirements → editable 3D design pipeline. | app + API |
| [`Adam-CAD/CADAM`](https://github.com/Adam-CAD/CADAM) | 5,405 | GPL-3.0 | 2026-10-15 | Open-source text-to-CAD web application built on CadQuery. | web app |
| [`Pan-Chera/Multi-Agent-CAD`](https://github.com/Pan-Chera/Multi-Agent-CAD) | 1,072 | MIT | 2026-11-04 | Decoupled multi-agent framework for text-to-CAD with constrained test-time search. | research code |
| [`SadilKhan/Text2CAD`](https://github.com/SadilKhan/Text2CAD) | 493 | NOASSERTION | 2025-05-15 | NeurIPS'24 dataset + model for sequential CAD generation from beginner-to-expert prompts. | research code |
| [`KittyCAD/text-to-cad-ui`](https://github.com/KittyCAD/text-to-cad-ui) | 296 | MIT | 2026-01-16 | UI for the Zoo Text-to-CAD API. | web UI |

Caveat: the high-star projects are products and research demos, not qualification tools. Their evaluation claims are usually self-reported; see [`benchmarks.md`](benchmarks.md).

---

## 7. General 2D CAD

| Repo | Stars | License | Last push | What it is | Interface |
|---|---:|---|---|---|---|
| [`daobataotie/CAD-MCP`](https://github.com/daobataotie/CAD-MCP) | 680 | MIT | 2026-10-27 | Natural-language control of AutoCAD-family drafting: create/modify drawings, layers, blocks. | MCP |
| [`zh19980811/Easy-MCP-AutoCad`](https://github.com/zh19980811/Easy-MCP-AutoCad) | 272 | no license | 2026-10-15 | AutoCAD MCP integration for natural-language drawing operations; README states limited maintenance. | MCP |

These are 2D drafting bridges. They are useful for drawings and BOM tables, not for B-rep solid modeling.

---

## 8. Onshape

| Repo | Stars | License | Last push | What it is | Interface |
|---|---:|---|---|---|---|
| [`ReshefElisha/jarvis-onshape-mcp`](https://github.com/ReshefElisha/jarvis-onshape-mcp) | 175 | NOASSERTION | 2026-04-22 | Claude Code plugin driving Onshape: sketches, extrudes, fillets, mates, Variable Studios, FeatureScript; mutating tools return structured change/warning records and multi-view PNGs. | MCP |
| [`hedless/onshape-mcp`](https://github.com/hedless/onshape-mcp) | 163 | no license | 2026-09-10 | 45-tool Onshape REST bridge: documents, part studios, sketches, features, assemblies. | MCP |

Onshape's REST API is the most agent-friendly closed CAD surface: OAuth, documented endpoints, deterministic document revisions.

---

## 9. Fusion 360

| Repo | Stars | License | Last push | What it is | Interface |
|---|---:|---|---|---|---|
| [`faust-machines/fusion360-mcp-server`](https://github.com/faust-machines/fusion360-mcp-server) | 145 | MIT | 2026-10-06 | MCP server connecting coding agents to Fusion 360; beta. | MCP |
| [`AuraFriday/Fusion-360-MCP-Server`](https://github.com/AuraFriday/Fusion-360-MCP-Server) | 128 | NOASSERTION | 2026-01-28 | Control Fusion 360 from any MCP client. | MCP |

Fusion's API is Python-based and runs inside the application; expect GUI session coupling.

---

## 10. CATIA

| Repo | Stars | License | Last push | What it is | Interface |
|---|---:|---|---|---|---|
| [`daiemon12/catia-v5-mcp-server`](https://github.com/daiemon12/catia-v5-mcp-server) | 157 | MIT | 2026-11-08 | CATIA V5 MCP server: parts, sketches, features, native analysis. | MCP |
| [`Cai-aa/CAD-Agent-Hub`](https://github.com/Cai-aa/CAD-Agent-Hub) | 138 | MIT | 2026-11-04 | Windows-focused hub with MCP servers for CATIA V5, SolidWorks, NX/UG, EPLAN, plus skills and examples. | MCP + skills |

CATIA automation is COM/CAA-heavy and version-sensitive; pin the CATIA release and test the bridge per release.

---

## 11. Siemens NX

| Repo | Stars | License | Last push | What it is | Interface |
|---|---:|---|---|---|---|
| [`DreamEnding/NX_MCP`](https://github.com/DreamEnding/NX_MCP) | 165 | MIT | 2026-10-18 | Local NX automation with 47+ tools over the NX GUI. | MCP |
| [`Cai-aa/CAD-Agent-Hub`](https://github.com/Cai-aa/CAD-Agent-Hub) | 138 | MIT | 2026-11-04 | NX/UG MCP server and in-process bridge (shared with the CATIA entry). | MCP |

NX Open is the deepest API in the list; the MCP layer is thin relative to what NX Open exposes.

---

## 12. ANSYS

| Repo | Stars | License | Last push | What it is | Interface |
|---|---:|---|---|---|---|
| [`hongwenwang36-eng/ANSYS-Workbench-mcp`](https://github.com/hongwenwang36-eng/ANSYS-Workbench-mcp) | 106 | MIT | 2026-10-14 | Local Windows bridge to SpaceClaim, Workbench, and System Coupling via journal files, a file-queue IPC, and MAPDL batch. | MCP |

Vendor alternative: `ansys/pymechanical-mcp` (28 tools), `ansys/pymapdl-mcp`, `ansys/pyfluent-mcp` (20 tools), all built on `ansys/pyansys-common-mcp`. These are official, Apache-2.0, and require a licensed installation.

---

## 13. Abaqus

| Repo | Stars | License | Last push | What it is | Interface |
|---|---:|---|---|---|---|
| [`Cai-aa/abaqus-mcp`](https://github.com/Cai-aa/abaqus-mcp) | 326 | MIT | 2026-10-26 | Abaqus/CAE plugin using file-based IPC: job submission, ODB inspection, viewport screenshots, model info. | MCP + plugin |
| [`Whfkl/Abaqus-Control-MCP`](https://github.com/Whfkl/Abaqus-Control-MCP) | 215 | MIT | 2026-09-29 | Real-time Abaqus/CAE control bridge for Codex, Claude Code, and other MCP clients. | MCP |
| [`jianzhichun/abaqus-mcp-server`](https://github.com/jianzhichun/abaqus-mcp-server) | 107 | MIT | 2025-05-26 | MCP server for an already running Abaqus/CAE GUI. | MCP |

Abaqus is the best-covered closed solver in the MCP ecosystem. The common pattern is a plugin inside CAE plus an external MCP process, because the CAE kernel is single-threaded and GUI-bound.

---

## 14. COMSOL

| Repo | Stars | License | Last push | What it is | Interface |
|---|---:|---|---|---|---|
| [`wjc9011/COMSOL_Multiphysics_MCP`](https://github.com/wjc9011/COMSOL_Multiphysics_MCP) | 944 | MIT | 2026-10-31 | COMSOL automation through the Java API; published paper describing the server. | MCP |
| [`777gegewu/comsol-mcp`](https://github.com/777gegewu/comsol-mcp) | 125 | MIT | 2026-05-13 | Learning-oriented COMSOL MCP controlling an open Desktop GUI through Java Shell. | MCP |

COMSOL's Java API is the most complete scripting surface among commercial multiphysics tools; the MCP layer can expose model tree, parameters, and solve steps.

---

## 15. OpenFOAM

| Repo | Stars | License | Last push | What it is | Interface |
|---|---:|---|---|---|---|
| [`webworn/openfoam-mcp-server`](https://github.com/webworn/openfoam-mcp-server) | 127 | NOASSERTION | 2026-01-18 | OpenFOAM MCP with CFD education features: Socratic questioning, case setup, error resolution. | MCP |

OpenFOAM automation is file-dictionary driven; an MCP server is mostly a schema-aware file editor plus a `foamRun`/`simpleFoam` process wrapper.

---

## 16. CAE platforms

| Repo | Stars | License | Last push | What it is | Interface |
|---|---:|---|---|---|---|
| [`Cai-aa/CAE-Agent-Hub`](https://github.com/Cai-aa/CAE-Agent-Hub) | 1,297 | MIT | 2026-10-27 | Hub of MCP tools, skills, and result viewers for modeling, meshing, solving, and post-processing; the broadest CAE-oriented agent collection. | MCP + skills |
| [`tangency-labs/fieldcraft`](https://github.com/tangency-labs/fieldcraft) | 346 | Apache-2.0 | 2026-11-07 | Clean-room CAE in Rust: parametric part → tet/hex mesh → implicit/explicit/thermal/LBM solve; desktop, CLI, and MCP drive the same commands. | MCP + CLI |
| [`svd-ai-lab/sim-cli`](https://github.com/svd-ai-lab/sim-cli) | 247 | Apache-2.0 | 2026-10-27 | Parses existing CAE files (Abaqus, Nastran, etc.) into bounded structured text for agents; no solver launch. | CLI |

---

## 17. Coverage gaps

The following directions have no maintained project above the threshold on 2026-11-08:

| Direction | Status | Practical workaround |
|---|---|---|
| CalculiX MCP | no project ≥ 100 stars | PrePoMax 3.0 ships a vendor MCP; otherwise wrap `ccx` with a CLI contract |
| Gmsh MCP | no project ≥ 100 stars | call `gmsh` Python API directly; expose your own tool |
| Code_Aster / Salome-Meca MCP | no project ≥ 100 stars | `as_run` + `.comm` templates; wrap as CLI |
| Elmer MCP | none | CLI + `.sif` templates |
| FreeFEM MCP | none | `.edp` generation + CLI |
| ParaView MCP | none above threshold | `pvpython` scripts + artifact contract |

This is the gap an AgenticCAD stack should fill: **solver-side verification tools are scarcer than CAD-side chat tools.**

---

## 18. Selection matrix

| Requirement | Recommended |
|---|---|
| Local, open, headless CAD | `cadgen` / `agentcad` / `build123d-mcp` |
| Human-in-the-loop FreeCAD | `freecad-ai` |
| Scripted FreeCAD CI | `FreeCADCmd` + `freecad-mcp` `execute_code_headless` |
| Windows SolidWorks | `solidworks-automation-skill` or SolidPilot |
| Onshape (cloud, OAuth) | `jarvis-onshape-mcp` or `hedless/onshape-mcp` |
| Abaqus | `Cai-aa/abaqus-mcp` |
| ANSYS | official PyAnsys MCP if licensed; otherwise Workbench bridge |
| COMSOL | `wjc9011/COMSOL_Multiphysics_MCP` |
| OpenFOAM | `webworn/openfoam-mcp-server` or direct dictionary templates |
| CAE orchestration | `CAE-Agent-Hub` |

---

## 19. Security notes

- MCP servers that expose `execute_code` are remote code execution by design. Run them under a dedicated user or container.
- Several entries have **no license file**. Treat them as all-rights-reserved until clarified.
- AGPL-3.0 entries (SolidPilot) impose network-use obligations if you modify and host them.
- Closed-CAD bridges often require the GUI to be logged in; credentials and license seats are part of the attack surface.
- Pin the server version and hash `tools/list`; a silent tool-schema change is a supply-chain event.
