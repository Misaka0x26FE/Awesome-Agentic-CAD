# Agent interfaces

This document specifies how an LLM agent drives CAD/CAE tools with reproducible state, structured observations, and rollback.

---

## 1. Interface stack

```
agent runtime
  ├─ tool discovery        MCP tools/list, OpenAPI, --help schema
  ├─ tool invocation       MCP tools/call, Python call, subprocess
  ├─ observation           JSON result, artifact path, image content
  ├─ verification          deterministic checker (no LLM)
  └─ checkpoint/rollback   artifact hash + state snapshot
```

Four transports, in order of preference:

| Transport | Determinism | Isolation | State | Use when |
|---|---|---|---|---|
| CLI + files | high | process | filesystem | batch, CI, GPL tools |
| Python API | high | process | memory | tight loops, permissive libs |
| MCP stdio | high | process | server session | editor integration, interactive |
| MCP HTTP | medium | network | server session | remote/worker deployment |

GUI automation is excluded from the deterministic path. It is acceptable only for human-in-the-loop steps.

---

## 2. MCP specifics

MCP is JSON-RPC 2.0. For CAD, the relevant methods are:

| Method | CAD semantics |
|---|---|
| `initialize` | negotiate protocol version, declare capabilities |
| `tools/list` | capability contract; hash it for reproducibility |
| `tools/call` | execute one action; return `content[]` + `structuredContent` |
| `notifications/progress` | long meshing/solve progress |
| `notifications/cancelled` | abort a running solve |
| `resources/list`, `resources/read` | model state, logs, screenshots |

### 2.1 Tool schema

A CAD tool must declare units, coordinate frame, and return schema.

```json
{
  "name": "measure_shape",
  "description": "Return mass properties of the active solid in the document frame.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "document": {"type": "string"},
      "object": {"type": "string"},
      "units": {"enum": ["mm", "m", "in"], "default": "mm"}
    },
    "required": ["document", "object"]
  },
  "outputSchema": {
    "type": "object",
    "properties": {
      "volume": {"type": "number"},
      "area": {"type": "number"},
      "centroid": {"type": "array", "items": {"type": "number"}, "minItems": 3, "maxItems": 3},
      "bbox": {"type": "array", "items": {"type": "number"}, "minItems": 6, "maxItems": 6},
      "valid": {"type": "boolean"},
      "solids": {"type": "integer"},
      "faces": {"type": "integer"}
    },
    "required": ["volume", "centroid", "valid"]
  }
}
```

Rules:

1. **No prose in `structuredContent`.** Numbers, enums, ids only.
2. **Units are explicit.** A missing unit is a schema error, not a default.
3. **Frame is explicit.** Document frame vs. local frame vs. world frame.
4. **Ids are stable within a session.** Do not reuse face indices across rebuilds.

### 2.2 Session model

A CAD session must expose:

```json
{
  "session_id": "...",
  "document": "part.FCStd",
  "document_revision": 17,
  "active_body": "Body",
  "selection": ["Face12", "Edge7"],
  "undo_depth": 3,
  "units": "mm",
  "kernel": "OCCT 7.8.1"
}
```

`document_revision` increments on every mutation. A tool call that references a stale revision must fail with `E_REVISION_CONFLICT`; the agent then re-reads state.

### 2.3 Error taxonomy

| Code | Meaning | Retry |
|---|---|---|
| `E_SCHEMA` | invalid arguments | repair args, no retry |
| `E_REVISION_CONFLICT` | stale document revision | re-read, replan |
| `E_GEOMETRY` | boolean/fillet/defeature failure | adjust parameters, rollback |
| `E_MESH` | meshing failure or quality gate | remesh/simplify |
| `E_SOLVER` | non-convergence | adjust controls, do not accept |
| `E_RESOURCE` | timeout/OOM | reduce model or raise limit |
| `E_PERMISSION` | tool not allowed | stop |

---

## 3. Python API patterns

### 3.1 Authoring with build123d

```python
from build123d import Box, Cylinder, Pos, export_step

body = Box(80, 60, 20)
hole = Pos(0, 0, 0) * Cylinder(radius=6, height=40)
part = body - hole

assert part.is_valid()
assert len(part.solids()) == 1
export_step(part, "bracket.step")
```

### 3.2 Mass properties with OCP

```python
from OCP.BRepGProp import BRepGProp
from OCP.GProp import GProp_GProps
from OCP.STEPControl import STEPControl_Reader
from OCP.IFSelect import IFSelect_RetDone

reader = STEPControl_Reader()
assert reader.ReadFile("bracket.step") == IFSelect_RetDone
reader.TransferRoots()
shape = reader.OneShape()

props = GProp_GProps()
BRepGProp.VolumeProperties_s(shape, props)
print(props.Mass(), props.CentreOfMass().X())
```

### 3.3 Defeaturing

```python
from OCP.BRepAlgoAPI import BRepAlgoAPI_Defeaturing
from OCP.TopTools import TopTools_ListOfShape

defeature = BRepAlgoAPI_Defeaturing()
defeature.SetShape(shape)
faces = TopTools_ListOfShape()
for f in target_faces:
    faces.Append(f)
defeature.AddFacesToRemove(faces)
defeature.Build()
result = defeature.Shape()
```

Always compare before/after: volume delta, face count, contact area, minimum distance.

### 3.4 Meshing with Gmsh

```python
import gmsh

gmsh.initialize()
gmsh.option.setNumber("General.Terminal", 0)
gmsh.model.add("part")
gmsh.model.occ.importShapes("bracket.step")
gmsh.model.occ.synchronize()
gmsh.option.setNumber("Mesh.MeshSizeMax", 4.0)
gmsh.option.setNumber("Mesh.MeshSizeMin", 0.8)
gmsh.model.mesh.generate(3)

types, tags, _ = gmsh.model.mesh.getElements(3)
gmsh.write("bracket.msh")
gmsh.finalize()
```

Quality gate after generation:

```python
import numpy as np
sicn = gmsh.model.mesh.getElementQuality(tags[0], "minSICN")
assert np.min(sicn) >= 0.10
```

---

## 4. CLI contract

### 4.1 Process wrapper

```python
import json, subprocess

def run(cmd, timeout=1800):
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    try:
        payload = json.loads(p.stdout)
    except json.JSONDecodeError:
        payload = {"raw_stdout": p.stdout[-4000:]}
    return {"exit": p.returncode, "payload": payload, "stderr": p.stderr[-4000:]}
```

### 4.2 FreeCAD headless

```bash
flatpak run --command=FreeCADCmd org.freecad.FreeCAD script.py
```

```python
# script.py
import FreeCAD, Part, json
shape = Part.Shape()
shape.read("/data/part.step")
print(json.dumps({
    "volume": shape.Volume,
    "faces": len(shape.Faces),
    "solids": len(shape.Solids),
    "valid": shape.isValid(),
}))
```

### 4.3 CalculiX

```bash
ccx -i job
# outputs job.dat, job.frd, job.sta
```

Accept results only if `job.sta` shows convergence for all increments and `job.dat` contains the requested frequency/field block.

### 4.4 FreeFEM

```bash
FreeFem++ case.edp -nw -v 0
```

Exit code 0 is necessary but not sufficient: parse the `.vtk`/`.txt` output and assert the target quantity.

---

## 5. Artifact contracts

Each stage writes an immutable artifact directory:

```
run/<run_id>/
├── input/
│   ├── part.step
│   └── spec.json
├── stage-01-geometry/
│   ├── out.step
│   ├── report.json
│   └── sha256.txt
├── stage-02-mesh/
│   ├── out.msh
│   ├── quality.json
│   └── sha256.txt
├── stage-03-solve/
│   ├── job.inp
│   ├── job.dat
│   ├── job.frd
│   └── sha256.txt
└── stage-04-post/
    ├── fields.vtu
    ├── render.png
    └── metrics.json
```

`report.json` minimum fields:

```json
{
  "stage": "geometry",
  "tool": "OCCT 7.8.1",
  "input_sha256": "...",
  "output_sha256": "...",
  "units": "mm",
  "metrics": {"volume": 12345.6, "faces": 257, "solids": 17, "valid": true},
  "gates": [{"name": "valid", "pass": true}, {"name": "volume_delta", "value": 0.000556, "limit": 0.01, "pass": true}],
  "warnings": []
}
```

---

## 6. Verification gates

| Gate | Computation | Typical limit |
|---|---|---|
| `valid` | `BRepCheck_Analyzer` | must be true |
| `watertight` | shell closure / mesh manifold | must be true |
| `volume_delta` | `|V - V0| / V0` | 0.1%–1% |
| `mass_delta` | `|m - m0| / m0` | 0.1%–1% |
| `bbox_delta` | max component deviation | 0.01–0.5 mm |
| `centroid_delta` | Euclidean distance | 0.01–0.1 mm |
| `contact_preserved` | interface set comparison | no lost pairs |
| `contact_area_delta` | per-pair area change | < 1% |
| `min_sicn` | Gmsh element quality | ≥ 0.10 |
| `bad_elements` | count below threshold | non-increasing |
| `converged` | solver status file | true |
| `residual` | final residual | ≤ 1e-6 (linear) |
| `eigen_delta` | `|f - f_ref| / f_ref` | 1%–10% |

A gate failure is a hard stop. Do not "continue and check later".

---

## 7. Sandboxing

`execute_code` is arbitrary code execution. Minimum controls:

1. **Process isolation**: run in a container or a dedicated Unix user; no host home mount.
2. **Read-only inputs**: mount source artifacts read-only; write only to `run/<id>`.
3. **Resource limits**: `RLIMIT_CPU`, `RLIMIT_AS`, wall-clock timeout, output size cap.
4. **Network**: deny by default; allowlist package mirrors if needed.
5. **Syscall filter**: seccomp profile for Python/CAD processes where available.
6. **Artifact hashing**: every output hashed and recorded.
7. **Audit log**: tool name, arguments hash, exit code, duration, output hash.
8. **Prompt-injection boundary**: treat STEP metadata, drawing text, and file names as untrusted; never interpolate them into system prompts.

---

## 8. Cost and latency budget

| Operation | Typical wall time | Token cost driver |
|---|---|---|
| Part script generation | 1–10 s | prompt + code |
| Boolean/defeature audit | 1–30 s | measurement JSON |
| Tet mesh (10⁵–10⁶ elements) | 10 s–10 min | quality summary |
| Modal solve (10⁵ DOF) | 1–30 min | result extraction |
| Multi-turn repair loop | 3–20 iterations | context growth |

Practical rules:

- summarize observations to fixed-size JSON (≤ 2 KB per tool call);
- keep screenshots at ≤ 1024 px and only on demand;
- cap repair loops (e.g. 5) and require a different hypothesis after two identical failures;
- cache tool schemas and static docs outside the prompt.
