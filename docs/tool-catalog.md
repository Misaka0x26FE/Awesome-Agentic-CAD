# Tool catalog

Every row states the **agent surface** and whether the tool runs headless. Versions are the public stable release as of 2026-11 unless noted.

Legend:

- **Agent surface**: `MCP` (Model Context Protocol), `Py` (Python API), `CLI`, `C++/C`, `REST`, `GUI only`.
- **Headless**: `yes` = runs without a display server; `no` = requires a GUI session; `partial` = some operations need a GUI.
- **License**: SPDX identifier where known.

---

## 1. Geometry kernels

| Tool | License | Source | Function | Agent surface | Headless |
|---|---|---|---|---|---|
| OpenCASCADE (OCCT) | LGPL-2.1 | <https://github.com/Open-Cascade-SAS/OCCT> · <https://dev.opencascade.org> | B-rep kernel: booleans, fillets, offsets, STEP/IGES/BREP, `BRepAlgoAPI_Defeaturing`, `BRepGProp`, `BRepExtrema` | C++, Python via OCP | yes |
| OCP | Apache-2.0 | <https://github.com/CadQuery/OCP> | Python bindings to OCCT 8.x | Py | yes |
| Parasolid | commercial | <https://www.siemens.com/en-us/products/plm-components/parasolid/> | Kernel used by SolidWorks, NX, Solid Edge, Onshape | C/C++/C#/.NET | yes |
| ACIS | commercial | <https://www.spatial.com/products/3d-acis-modeling> | Kernel used by Inventor and older CAD | C++ | yes |
| CGM | commercial | <https://www.3ds.com/products/catia> | CATIA kernel, strong surfacing | CAA | yes |
| Granite | commercial | <https://www.ptc.com/en/products/creo> | Creo kernel | Toolkit | yes |

> OCCT is the only mature open B-rep kernel. Its fillet/boolean robustness is below Parasolid on thin walls, variable-radius fillets, and intersecting edges; this is a property of the kernel, not of a wrapper.

---

## 2. CAD authoring

### 2.1 Open source

| Tool | Version | License | Source | Function | Agent surface | Headless |
|---|---|---|---|---|---|---|
| FreeCAD | 1.1.4 | LGPL-2.1 | <https://github.com/FreeCAD/FreeCAD> · <https://www.freecad.org> | Parametric PartDesign, Assembly, TechDraw, FEM workbench, Python API | Py, `FreeCADCmd` CLI | yes |
| build123d | 0.13.0 | Apache-2.0 | <https://github.com/gumyr/build123d> · <https://build123d.readthedocs.io> | Pythonic B-rep modeling: builder + algebra modes, explicit topology objects | Py | yes |
| CadQuery | 2.8.0 | Apache-2.0 | <https://github.com/CadQuery/cadquery> · <https://cadquery.readthedocs.io> | Fluent Workplane API, assemblies with constraints | Py | yes |
| OpenSCAD | 2021.01 / dev | GPL-2.0 | <https://github.com/openscad/openscad> · <https://openscad.org> | CSG scripting, mesh output (STL/3MF), no B-rep | CLI, custom language | yes |
| Solvespace | 3.1 | GPL-3.0 | <https://github.com/solvespace/solvespace> · <https://solvespace.com> | Constraint sketches, lightweight solids | GUI, limited CLI | partial |
| BRL-CAD | 7.40 | BSD/LGPL | <https://github.com/BRL-CAD/brlcad> · <https://brlcad.org> | CSG modeling, ray tracing, military heritage | Tcl, C | yes |

### 2.2 Closed source

| Tool | Vendor (2026) | Kernel | Source | Function | Agent surface | Headless |
|---|---|---|---|---|---|---|
| SolidWorks | Dassault Systèmes | Parasolid | <https://www.solidworks.com> | Mid-market parametric CAD, drawings, PDM | VBA/C#/API | no |
| NX | Siemens | Parasolid | <https://plm.sw.siemens.com/en-US/nx/> | High-end CAD/CAM/CAE, NX Open | C++/Python/Journal | partial |
| Creo | PTC | Granite | <https://www.ptc.com/en/products/creo> | Parametric CAD, complex surfacing | Toolkit (C/C++) | no |
| CATIA | Dassault Systèmes | CGM | <https://www.3ds.com/products/catia> | Aerospace/automotive surfacing, large assemblies | CAA, CATScript | partial |
| Inventor | Autodesk | ShapeManager | <https://www.autodesk.com/products/inventor> | Mechanical CAD, iLogic automation | iLogic/VBA/.NET | no |
| Solid Edge | Siemens | Parasolid | <https://solidedge.siemens.com> | Synchronous + ordered modeling, sheet metal | API/.NET/Python | no |
| Fusion | Autodesk | Autodesk kernel | <https://www.autodesk.com/products/fusion-360> | CAD/CAM/CAE, cloud data | Python/C++ API | partial |
| Onshape | PTC | Parasolid | <https://www.onshape.com> | Browser CAD + PDM, FeatureScript | FeatureScript, REST | yes (cloud) |
| SpaceClaim | ANSYS (Synopsys) | Parasolid | <https://www.ansys.com/products/3d-design/ansys-spaceclaim> | Direct modeling, geometry cleanup for simulation | Python/.NET | partial |
| DesignModeler | ANSYS (Synopsys) | Parasolid/ACIS | <https://www.ansys.com/products/ansys-workbench> | Legacy ANSYS geometry preparation | JScript/Python | partial |

---

## 3. Geometry preparation and inspection

| Tool | License | Source | Function | Agent surface | Headless |
|---|---|---|---|---|---|
| OCCT Defeaturing | LGPL-2.1 | <https://dev.opencascade.org/doc/overview/html/occt_user_guides__modeling_algos.html> | Remove holes, fillets, chamfers, pockets by face set | C++/Py (OCP) | yes |
| Analysis Situs | BSD-3 | <https://gitlab.com/ssv/AnalysisSitus> · <https://analysissitus.org> | Feature recognition, small/narrow face detection, shape healing, STEP inspection | C++/Python (Tcl) | yes |
| Salome GEOM | LGPL-2.1 | <https://www.salome-platform.org> | Parametric geometry, healing, groups, STEP/IGES | Python | yes |
| FreeCAD Defeaturing WB | LGPL-2.1 | <https://github.com/FreeCAD/FreeCAD> (addon) | GUI wrapper over OCCT defeaturing | Py | partial |
| CADdoctor | commercial | <https://www.elysium-global.com/products/caddoctor/> | CAD-to-CAE healing, simplification, translation validation | CLI/batch | yes |
| ANSA | commercial | <https://www.cadence.com/en_US/home/tools/engineering-simulation/ansa-preprocessor.html> | Geometry cleanup, batch meshing, solver decks | Python | partial |

---

## 4. Meshing

| Tool | Version | License | Source | Function | Agent surface | Headless |
|---|---|---|---|---|---|---|
| Gmsh | 4.15.2 | GPL-2.0+ (linking exception) | <https://gitlab.onelab.info/gmsh/gmsh> · <https://gmsh.info> | Tet/hex/pyramid/wedge, size fields, boundary layers, `.msh` | Py, C++, CLI | yes |
| Netgen | 6.2.2608 | LGPL-2.1 | <https://github.com/NGSolve/ngsolve> · <https://ngsolve.org> | Robust tet meshing, CSG, integrated with NGSolve | Py, C++ | yes |
| TetGen | 1.6.0 | AGPL-3.0 | <https://wias-berlin.de/software/tetgen/> | High-quality tetrahedra, boundary recovery | C++, CLI | yes |
| MMG | 5.7 | LGPL-3.0 | <https://github.com/MmgTools/mmg> · <https://github.com/MmgTools/mmg> | Anisotropic remeshing, adaptation | C, CLI | yes |
| cfMesh | 1.1.2 | GPL-3.0 | <https://github.com/OpenFOAM/OpenFOAM-dev> (integration) | Automatic polyhedral/tet mesh for OpenFOAM | CLI | yes |
| snappyHexMesh | OpenFOAM | GPL-3.0 | <https://www.openfoam.com> | Cartesian + snapping + layers for CFD | CLI | yes |
| ANSYS Meshing | commercial | <https://www.ansys.com/products/ansys-workbench> | Workbench-integrated meshing | JScript/Python | partial |
| HyperMesh | commercial | <https://www.siemens.com/en-us/products/simcenter/simulation-modeling-visualization/hypermesh/> | BatchMesher, hex, solver templates | Tcl/Python | partial |
| STAR-CCM+ mesher | commercial | <https://plm.sw.siemens.com/en-US/simcenter/fluids-thermal-simulation/star-ccm/> | Polyhedral, trimmed cell, automated CFD mesh | Java/Python | partial |
| Pointwise | commercial | <https://www.pointwise.com> | Structured/unstructured CFD meshing | Glyph/Tcl | partial |

**Quality metrics are not portable.** Gmsh `minSICN`, `gamma`, `minSIGE` do not equal ANSYS Element Quality. Build a mapping by reading the same mesh in both tools and comparing quantiles before using a single threshold.

---

## 5. Structural / thermal / multiphysics solvers

| Tool | Version | License | Source | Function | Agent surface | Headless |
|---|---|---|---|---|---|---|
| CalculiX | 2.23 | GPL-2.0 | <https://github.com/Dhondtguido/CalculiX> · <http://www.dhondt.de> | Static, modal, buckling, transient, thermal, contact, `*TIE`; Abaqus-like `.inp` | CLI (`ccx`), `cgx` | yes |
| PrePoMax | 3.0.0 | GPL-3.0 | <https://github.com/PrePoMax/PrePoMax> · <https://prepomax.fs.um.si> | GUI pre/post for CalculiX; Python API + MCP server in 3.0 | MCP, Py, GUI | partial |
| Code_Aster | 17.4 (stable) | GPL-2.0 | <https://gitlab.com/codeaster/codeaster> · <https://code-aster.org> | Fatigue, fracture, damage, contact, thermo-mechanics, seismic | Python, `.comm`, `as_run` | yes |
| Salome-Meca | 2025.1 | LGPL/GPL | <https://www.open-simulation-center.org/downloads/code_aster/SALOME_MECA/2025> | Integrated GEOM/SMESH/AsterStudy + Code_Aster | Py, CLI | yes (container) |
| Elmer | 9.0 | GPL/LGPL | <https://github.com/ElmerCSC/elmerfem> · <https://www.elmerfem.org> | Multiphysics: structure, heat, flow, EM, acoustics | CLI, Py | yes |
| FEniCSx | 0.11 | LGPL-3.0 | <https://github.com/FEniCS/dolfinx> · <https://fenicsproject.org> | Weak-form PDE, MPI, Python/C++ | Py, C++ | yes |
| MOOSE | 5.0 | LGPL-2.1 | <https://github.com/idaholab/moose> · <https://mooseframework.inl.gov> | Fully coupled multiphysics, GPU (Kokkos/MFEM), NQA-1 QA | C++ apps, input files, Py | yes |
| deal.II | 9.7 | LGPL-2.1 | <https://github.com/dealii/dealii> · <https://www.dealii.org> | Adaptive FEM, hp, HPC | C++ | yes |
| MFEM | 4.8 | BSD-3 | <https://github.com/mfem/mfem> · <https://mfem.org> | High-order FEM, GPU, exascale | C++, Py | yes |
| Kratos | 10.x | BSD-3 | <https://github.com/KratosMultiphysics/Kratos> · <https://kratosmultiphysics.github.io/Kratos/> | Multiphysics apps, FSI, DEM | Py, C++ | yes |
| GetFEM | 5.4 | LGPL-2.1 | <https://github.com/GetFEM/GetFEM> · <https://getfem.org> | XFEM, contact, generic FEM | Py, C++ | yes |
| scikit-fem | 12.0 | BSD-3 | <https://github.com/kinnala/scikit-fem> · <https://scikit-fem.readthedocs.io> | Lightweight Python FEM | Py | yes |
| FreeFEM | 4.17 | LGPL-2.1+ | <https://github.com/FreeFem/FreeFem-sources> · <https://freefem.org> | PDE DSL, 2D/3D, multi-mesh interpolation, eigenvalues | DSL, CLI, MPI | yes |
| ANSYS Mechanical | commercial | <https://www.ansys.com/products/structures/ansys-mechanical> | Structural/thermal/modal/coupled, Workbench | PyAnsys, JScript, MCP | partial |
| Abaqus | commercial | <https://www.3ds.com/products/simulia/abaqus> | Nonlinear, contact, materials, explicit | Python, CLI | partial |
| MSC Nastran | commercial | <https://www.cadence.com/en_US/home/tools/engineering-simulation/msc-nastran.html> | Linear/dynamic/aeroelastic | DMAP, Python | yes |
| Simcenter Nastran | commercial | <https://www.siemens.com/en-us/products/simcenter/mechanical-simulation/nastran/> | Linear/dynamic FEA | Python | yes |
| COMSOL | commercial | <https://www.comsol.com> | Arbitrary coupled PDE, multiphysics | Java API, Python (mph) | yes |
| Simcenter 3D | commercial | <https://plm.sw.siemens.com/en-US/simcenter/mechanical-simulation/simcenter-3d/> | Structural dynamics, acoustics, durability | Python | partial |
| LS-DYNA | commercial | <https://www.ansys.com/products/structures/ansys-ls-dyna> | Explicit crash/impact | Keyword decks, CLI | yes |

---

## 6. CFD and explicit dynamics

| Tool | License | Source | Function | Agent surface | Headless |
|---|---|---|---|---|---|
| OpenFOAM | GPL-3.0 | <https://github.com/OpenFOAM/OpenFOAM-dev> · <https://openfoam.org> | Finite volume CFD, custom solvers | CLI, C++ | yes |
| SU2 | LGPL-2.1 | <https://github.com/su2code/SU2> · <https://su2code.github.io> | Compressible CFD, adjoint optimization | CLI, Python | yes |
| code_saturne | GPL-2.0 | <https://github.com/code-saturne/code_saturne> · <https://www.code-saturne.org> | Industrial CFD, large meshes | CLI, Python | yes |
| OpenCourant | AGPL-3.0 | <https://github.com/OpenCourant/OpenCourant> · <https://opencourant.org> | Community continuation of OpenRadioss (explicit crash/impact) | CLI | yes |
| Ansys Fluent | commercial | <https://www.ansys.com/products/fluids/ansys-fluent> | General CFD | PyFluent, MCP, Scheme | partial |
| STAR-CCM+ | commercial | <https://plm.sw.siemens.com/en-US/simcenter/fluids-thermal-simulation/star-ccm/> | Integrated CFD/multiphysics | Java/Python | partial |

> OpenRadioss was discontinued by Siemens on 2026-10-01; the AGPL fork OpenCourant continues from the last public code base. Treat material-card coverage as incomplete until verified.

---

## 7. Multibody dynamics

| Tool | License | Source | Function | Agent surface | Headless |
|---|---|---|---|---|---|
| MBDyn | GPL-2.0 | <https://www.mbdyn.org> | General multibody, flexible elements, co-simulation | CLI, Python peer API | yes |
| Project Chrono | BSD-3 | <https://github.com/projectchrono/chrono> · <https://projectchrono.org> | Multibody + FEA + granular + FSI, PyChrono | Py, C++ | yes |
| Adams | commercial | <https://www.cadence.com/en_US/home/tools/engineering-simulation/adams.html> | Industrial MBD, tires, vehicles | Python, GUI | partial |
| Simpack | commercial | <https://www.3ds.com/products/simulia/simpack> | Rail, wind, vehicle dynamics | Python, GUI | partial |
| RecurDyn | commercial | <https://www.functionbay.com> | Contact-rich MBD, tracked vehicles | GUI, API | partial |

---

## 8. Post-processing and data exchange

| Tool | License | Source | Function | Agent surface | Headless |
|---|---|---|---|---|---|
| ParaView | BSD-3 | <https://gitlab.kitware.com/paraview/paraview> · <https://www.paraview.org> | Large-data visualization, batch Python | `pvpython`, Py | yes |
| PyVista | MIT | <https://github.com/pyvista/pyvista> · <https://docs.pyvista.org> | Python VTK wrapper, headless rendering | Py | yes |
| meshio | MIT | <https://github.com/nschloe/meshio> | Mesh format conversion (Gmsh, Abaqus, VTK, MED, …) | Py, CLI | yes |
| ccx2paraview | GPL-2.0 | <https://github.com/calculix/ccx2paraview> | CalculiX `.frd` → VTK | Py, CLI | yes |
| VisIt | BSD-3 | <https://github.com/visit-dav/visit> · <https://visit-dav.github.io/visit-website/> | Parallel visualization | CLI, Py | yes |
| Tecplot 360 | commercial | <https://www.tecplot.com> | Engineering plots and reports | Py, CLI | partial |
| EnSight | commercial | <https://www.ansys.com/products/fluids/ansys-ensight> | Large assembly visualization | Py | partial |
| HyperView | commercial | <https://www.siemens.com/en-us/products/simcenter/simulation-modeling-visualization/hyperview/> | CAE results, fatigue | Tcl/Python | partial |

---

## 9. Topology and design optimization

| Tool | License | Source | Function | Agent surface | Headless |
|---|---|---|---|---|---|
| pyMOTO | MIT | <https://github.com/aatmdelissen/pyMOTO> | SIMP/robust topology optimization, thermal, overhang filter | Py | yes |
| beso | LGPL-3.0 | <https://github.com/calculix/beso> | BESO with CalculiX, FreeCAD workflow | Py, CLI | yes |
| dl4to | Apache-2.0 | <https://github.com/dl4to/dl4to> | PyTorch SIMP + deep-learning research | Py | yes |
| TopOpt (DTU) | — | <https://github.com/TopOpt/TopOpt_in_PETSc> | Educational SIMP, PETSc | C++ | yes |
| OptiStruct | commercial | <https://altair.com/optistruct> | Industrial topology/size/shape optimization | Python/Tcl | partial |
| Tosca | commercial | <https://www.3ds.com/products/simulia/tosca> | Topology/shape optimization | Python | partial |
| Inspire | commercial | <https://altair.com/inspire> | Concept generative design | GUI | no |

---

## 10. Agent surfaces

| Project | Version | License | Source | Exposes | Tools / scope | Transport |
|---|---|---|---|---|---|---|
| freecad-ai | 0.32.0-alpha | MIT | <https://github.com/ghbalf/freecad-ai> | FreeCAD addon + MCP server | 64 semantic tools: bodies, sketches, primitives, fillets, booleans, assemblies, variables, `describe_model`, `measure`, undo, skills | Streamable HTTP `:3000/mcp` |
| freecad-mcp | 0.1.26 | MIT | <https://github.com/neka-nat/freecad-mcp> | FreeCAD XML-RPC bridge + MCP | 17 API-level tools, `execute_code`, `execute_code_headless`, `get_view`, `run_fem_analysis` | stdio; XML-RPC `:9875` |
| build123d-mcp | 0.3.91 | Apache-2.0 | <https://github.com/pzfreo/build123d-mcp> | build123d session | 38 tools, 12 resources: execute, render, measure, feature recognition, export, snapshots | stdio / HTTP |
| agentcad | 0.7.2 | Apache-2.0 | <https://agentcad.dev> | build123d CLI + MCP | run, render, export, inspect, diff, validate | CLI / MCP |
| cadgen | 0.8.2 | — | <https://github.com/earthtojake/text-to-cad> | CAD engine + MCP + viewer | run scripts, export STEP/GLB/STL/3MF/DXF, snapshots, XBF | MCP / HTTP engine `:3245` |
| PyMechanical-MCP | 2026.x | Apache-2.0 | <https://github.com/ansys/pymechanical-mcp> | ANSYS Mechanical over gRPC | 28 tools: session, scripts, solve, results, screenshots | stdio / HTTP |
| PyMAPDL-MCP | 2026.x | Apache-2.0 | <https://github.com/ansys/pymapdl-mcp> | MAPDL | batch commands, Python execution, plots | stdio |
| PyFluent-MCP | 2026.x | Apache-2.0 | <https://github.com/ansys/pyfluent-mcp> | Fluent | 20 tools: session, settings tree, run/validate, mesh quality, reports | stdio / HTTP |
| PyAnsys Common MCP | 0.3.6 | Apache-2.0 | <https://github.com/ansys/pyansys-common-mcp> | MCP framework | base classes for product MCP servers | stdio / HTTP |
| PrePoMax MCP | 3.0.0 | GPL-3.0 | <https://github.com/PrePoMax/PrePoMax> | CalculiX pre/post | Python API + MCP server (verify tool surface per release) | local |
| CAE-Agent-Hub | — | see repo | <https://github.com/Cai-aa/CAE-Agent-Hub> | reference agents | CalculiX `.inp` generation, ccx run, modal extraction | MCP reference |

> `freecad-ai` and `freecad-mcp` both drive `App::Document` on the GUI main thread. Do not attach both to the same document concurrently; serialize by document id.

---

## 11. Closed-source simulation and pre/post

| Tool | Vendor | Source | Function | Automation |
|---|---|---|---|---|
| ANSYS Workbench / Mechanical | Synopsys | <https://www.ansys.com/products/ansys-workbench> | Structural, thermal, modal, coupled | PyAnsys, JScript, MCP |
| ANSYS Fluent | Synopsys | <https://www.ansys.com/products/fluids/ansys-fluent> | CFD | PyFluent, Scheme |
| Abaqus/CAE | Dassault SIMULIA | <https://www.3ds.com/products/simulia/abaqus> | Nonlinear FEA, explicit | Python |
| COMSOL Multiphysics | COMSOL | <https://www.comsol.com> | Coupled multiphysics | Java API, `mph` |
| Simcenter 3D | Siemens | <https://plm.sw.siemens.com/en-US/simcenter/mechanical-simulation/simcenter-3d/> | Structural dynamics, acoustics | Python |
| HyperMesh | Siemens | <https://www.siemens.com/en-us/products/simcenter/simulation-modeling-visualization/hypermesh/> | Pre-processing, meshing | Tcl/Python |
| ANSA | Cadence | <https://www.cadence.com/en_US/home/tools/engineering-simulation/ansa-preprocessor.html> | Pre-processing, batch meshing | Python |
| SimScale | SimScale | <https://www.simscale.com> | Cloud CFD/FEA/thermal | REST API |
| CAD Exchanger | CAD Exchanger | <https://cadexchanger.com> | 30+ CAD format conversion, batch | CLI/SDK |
| Datakit | Datakit | <https://www.datakit.com> | CAD format conversion | CLI/SDK |

---

## 12. Format notes

| Format | Role | Producer | Consumer | Risk |
|---|---|---|---|---|
| STEP AP242 | B-rep + PMI | CAD, OCCT | CAD, CAE, meshers | PMI semantics often dropped |
| BREP | OCCT native | OCCT, FreeCAD | OCCT | not portable across kernels |
| IGES | surface exchange | legacy CAD | CAE | gaps, trimming errors |
| Parasolid `x_t` / `x_b` | kernel-native | SolidWorks, NX, Solid Edge | Parasolid-based tools | no open-source reader on Linux without schema catalog |
| `.inp` | CalculiX/Abaqus deck | PrePoMax, scripts | CalculiX, Abaqus | keyword subset differs |
| `.frd` | CalculiX results | ccx | ccx2paraview, ParaView | binary/text variants |
| `.med` | Salome/Code_Aster mesh+fields | SMESH, Aster | Code_Aster, ParaView | version coupling |
| `.msh` | Gmsh mesh | Gmsh | CalculiX (via conversion), FEniCS, FreeFEM | MSH2 vs MSH4 schema |
| `.vtu` / `.vtk` | post-processing | ParaView, PyVista | ParaView, PyVista | cell/point data association |
| XBF | cadgen document | cadgen | cadgen viewer | vendor-specific |
