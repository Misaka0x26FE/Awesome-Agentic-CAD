# Reference architecture

A minimal, reproducible AgenticCAD stack: one agent runtime, one tool layer, one deterministic verifier, one artifact store.

---

## 1. Requirements

| ID | Requirement | Acceptance |
|---|---|---|
| R1 | Every mutation is reversible | checkpoint exists before each tool call |
| R2 | Every observation is machine-readable | JSON schema, units, frame |
| R3 | Every stage has a gate | gate result stored in `report.json` |
| R4 | Every artifact is hashed | SHA-256 in manifest |
| R5 | Versions are pinned | kernel, mesher, solver, model ids in manifest |
| R6 | GPL tools are process-isolated | no linkage into distributed binaries |
| R7 | Single writer per document | document lock by id |
| R8 | Failures are typed | error taxonomy in `agent-interfaces.md` |

Non-goals: real-time collaboration, multi-user document editing, automatic qualification.

---

## 2. Topology

### 2.1 Single node (development)

```
agent runtime ── stdio MCP ──► freecad-mcp / build123d-mcp / cadgen
      │
      ├── subprocess ──► gmsh, ccx, FreeFEM
      └── filesystem ──► runs/<id>/
```

Suitable for one user, one document, models up to ~10⁶ DOF.

### 2.2 Worker node (batch)

```
agent runtime ── HTTP MCP ──► tool gateway
                                 ├── cad worker (build123d + OCP)
                                 ├── mesh worker (gmsh)
                                 └── solve worker (ccx / Aster / Elmer)
                                         │
                                   artifact store (S3/NFS)
```

Suitable for parameter sweeps and multi-case DOE. The gateway enforces per-document locks and per-user quotas.

### 2.3 Isolation boundary

| Boundary | Mechanism |
|---|---|
| agent ↔ tool | MCP or subprocess; never shared memory |
| tool ↔ kernel | one process per document |
| solver ↔ host | container or dedicated user, CPU/memory limits |
| artifact ↔ agent | read-only mount, hash verification |

---

## 3. State machine

```
INIT
 └─► SPEC_READY
      └─► GEOMETRY_DRAFT ──gate──► GEOMETRY_ACCEPTED
            ▲                         │
            └──── rollback ◄──────────┘
                                      ▼
                                 MESH_DRAFT ──gate──► MESH_ACCEPTED
                                      ▲                  │
                                      └── rollback ◄─────┘
                                                         ▼
                                                    SOLVE_RUNNING
                                                         │
                                       ┌─────────────────┴─────────────────┐
                                       ▼                                   ▼
                                 SOLVE_ACCEPTED                      SOLVE_REJECTED
                                       │                                   │
                                       ▼                                   ▼
                                  POST_READY ──► DELIVERED            rollback / replan
```

Rules:

- a state transition requires a gate record;
- `SOLVE_REJECTED` never produces a deliverable;
- `DELIVERED` requires a manifest with all upstream hashes.

---

## 4. Data contracts

### 4.1 `spec.json`

```json
{
  "task_id": "bracket-001",
  "units": "mm",
  "material": {"name": "steel", "E": 210000, "nu": 0.3, "rho": 7.85e-9},
  "loads": [{"type": "force", "magnitude": 500, "direction": [0, -1, 0], "surface": "load_face"}],
  "constraints": [{"type": "fixed", "surface": "mount_face"}],
  "acceptance": {"max_disp": 0.5, "min_f1": 800, "max_mass": 2.5},
  "tolerances": {"volume_rel": 0.01, "mass_rel": 0.01, "contact_area_rel": 0.01}
}
```

### 4.2 `geometry_report.json`

```json
{
  "stage": "geometry",
  "tool": {"name": "OCCT", "version": "8.0.1"},
  "input_sha256": "...",
  "output_sha256": "...",
  "units": "mm",
  "metrics": {
    "volume": 12345.6,
    "surface_area": 4567.8,
    "centroid": [0.0, 0.0, 12.3],
    "bbox": [-40, -30, 0, 40, 30, 20],
    "solids": 1,
    "faces": 257,
    "valid": true,
    "watertight": true
  },
  "gates": [
    {"name": "valid", "pass": true},
    {"name": "volume_delta", "value": 0.0006, "limit": 0.01, "pass": true}
  ]
}
```

### 4.3 `mesh_report.json`

```json
{
  "stage": "mesh",
  "tool": {"name": "gmsh", "version": "4.15.2"},
  "elements": {"tet4": 254557, "tri3": 18234},
  "nodes": 48211,
  "quality": {"min_sicn": 0.12, "p01_sicn": 0.31, "bad": 17, "bad_limit": 50},
  "gates": [{"name": "min_sicn", "value": 0.12, "limit": 0.10, "pass": true}]
}
```

### 4.4 `solve_report.json`

```json
{
  "stage": "solve",
  "solver": {"name": "ccx", "version": "2.23"},
  "step": "modal",
  "converged": true,
  "increments": 1,
  "iterations": 4,
  "residual": 1.2e-9,
  "results": {"f1": 1836.0, "f2": 2104.3},
  "warnings": []
}
```

---

## 5. Gates

| Stage | Gate | Reject when |
|---|---|---|
| geometry | `valid` | `BRepCheck_Analyzer` fails |
| geometry | `solids` | `< 1` or `> expected` |
| geometry | `volume_delta` | `> tol` |
| geometry | `contact_preserved` | any required pair lost |
| mesh | `min_sicn` | `< 0.10` |
| mesh | `bad_count` | `> bad_limit` |
| solve | `converged` | false |
| solve | `residual` | `> 1e-6` |
| post | `target_delta` | `> 10%` vs reference |
| delivery | `manifest_complete` | missing hash or version |

Gate thresholds are task parameters, not global constants. Store them in `spec.json`.

---

## 6. Checkpoints and rollback

Checkpoint tuple:

```
checkpoint = (step, STEP file, state.json, sha256, tool versions)
```

Rules:

- write checkpoint **before** a mutating call;
- keep the last `N` checkpoints (N ≥ 3);
- rollback restores files and clears downstream stages;
- rollback must be idempotent.

Do not rely on GUI undo stacks. They are not durable, not scriptable, and not available headless.

---

## 7. Determinism

Hash inputs:

```
run_hash = sha256(
  spec.json ||
  source.step ||
  kernel_version ||
  mesher_version ||
  solver_version ||
  model_id ||
  gate_thresholds
)
```

Sources of non-determinism to control:

| Source | Control |
|---|---|
| LLM sampling | temperature 0, fixed seed where supported |
| model alias | pin exact model id and provider version |
| kernel | pin OCCT/Parasolid build |
| mesher | pin version and random seed |
| solver | pin version and thread count |
| floating point | fix thread count, avoid `-ffast-math` |
| file order | sort directory listings |

---

## 8. Concurrency

- one document, one writer;
- parallelize across documents, not within a document;
- solvers may use MPI/OpenMP internally; do not oversubscribe;
- the artifact store is append-only; never overwrite a completed run.

---

## 9. Observability

Emit per tool call:

```json
{
  "ts": "2026-11-08T12:00:00Z",
  "run_id": "...",
  "tool": "gmsh.generate",
  "args_hash": "...",
  "duration_ms": 4210,
  "exit": 0,
  "output_hash": "...",
  "gate": "pass"
}
```

Metrics worth tracking:

- gate pass rate per stage;
- repair iterations per task;
- wall time per stage;
- token cost per accepted artifact;
- rollback frequency.

---

## 10. Deployment

### 10.1 Local

```bash
# CAD engine
cadgen doctor
cadgen status

# FreeCAD headless
flatpak run --command=FreeCADCmd org.freecad.FreeCAD script.py

# Solver
ccx -i job
```

### 10.2 Container

- one image per solver family;
- read-only root filesystem;
- `/work` as the only writable mount;
- no network by default;
- CPU and memory limits enforced by the runtime.

### 10.3 Windows-only CAD

SolidWorks, CATIA, NX, and Fusion require a Windows host. Expose them through a bridge process and keep the agent on Linux; the artifact contract stays the same (STEP in, STEP/CSV out).

---

## 11. Minimal viable pipeline

```
1. spec.json
2. build123d script → part.step
3. OCP audit → geometry_report.json
4. gmsh → part.msh + mesh_report.json
5. ccx → job.dat/job.frd + solve_report.json
6. ccx2paraview → fields.vtu
7. PyVista → render.png + metrics.json
8. manifest.json
```

Each step is a CLI with a JSON contract. The agent never parses unstructured logs.

---

## 12. Anti-patterns

| Anti-pattern | Why it fails |
|---|---|
| Chat with a GUI via screenshots only | no numeric state, no rollback |
| One MCP server per document, multiple clients | race on `App::Document` |
| Trusting solver exit code 0 | non-convergence can still exit 0 |
| Storing only the final STEP | cannot reproduce or audit |
| Global gate thresholds | part-specific tolerances differ |
| Mixing GPL solvers into a distributed binary | license obligations |
| Letting the model write the verifier | verification becomes self-assessment |
| Reusing face indices across rebuilds | topological naming failure |
