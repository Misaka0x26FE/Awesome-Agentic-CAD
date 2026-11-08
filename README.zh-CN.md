<a id="top" name="top"></a>

<div align="center">
  <img src="assets/banner.svg" alt="Awesome Agentic CAD — 面向 LLM 驱动 CAD/CAE 的工具、接口、评测与失效模式" width="100%">
</div>

<div align="center">

[English](README.md) · **简体中文**

[![Awesome](https://img.shields.io/badge/awesome-agentic--cad-0ea5e9?style=flat-square)](#)
[![License: MIT](https://img.shields.io/github/license/Misaka0x26FE/Awesome-Agentic-CAD?style=flat-square&color=22c55e)](LICENSE)
[![Last commit](https://img.shields.io/github/last-commit/Misaka0x26FE/Awesome-Agentic-CAD?style=flat-square&color=8b5cf6)](https://github.com/Misaka0x26FE/Awesome-Agentic-CAD/commits/main)
[![Stars](https://img.shields.io/github/stars/Misaka0x26FE/Awesome-Agentic-CAD?style=flat-square&color=f59e0b)](https://github.com/Misaka0x26FE/Awesome-Agentic-CAD)
[![PRs welcome](https://img.shields.io/badge/PRs-welcome-22c55e?style=flat-square)](CONTRIBUTING.md)

</div>

> **面向 LLM 驱动 CAD/CAE 的技术索引：开源与闭源工具、agent 接口、评测证据、失效模式。**
>
> 范围：参数化 B-rep 建模、几何准备、网格、结构/热/多物理求解、后处理、拓扑优化，以及把它们绑定成闭环的 agent 接口层。
>
> 状态：持续维护。每条记录给出源码、许可证、agent 接口、无头能力；结论标注证据等级。

<table>
  <tr>
    <td align="center"><b>36</b><br/><sub>agent 项目</sub></td>
    <td align="center"><b>9</b><br/><sub>benchmark</sub></td>
    <td align="center"><b>12</b><br/><sub>失效机制</sub></td>
    <td align="center"><b>6</b><br/><sub>篇指南</sub></td>
    <td align="center"><b>169</b><br/><sub>条链接已检查</sub></td>
  </tr>
</table>

> **适合谁读**：正在构建一个必须交付可制造 STEP、收敛求解与可审计证据链的 agent，而不是一张截图。

## 目录

- [定义](#1-定义)
- [分层模型](#2-分层模型)
- [能力包络](#3-能力包络基于公开证据)
- [Agent 接口模式](#4-agent-接口模式)
- [参考架构](#5-参考架构)
- [工具目录](#6-工具目录)
- [Agent 生态](#61-agent-生态)
- [评测证据](#7-评测证据)
- [局限](#8-局限)
- [仓库结构](#9-仓库结构)
- [贡献](#10-贡献)
- [许可证](#11-许可证)
- [参考](#12-参考)

---

## 1. 定义

**Agentic CAD 是几何状态上的闭环控制**，不是 CAD GUI 的自然语言外壳。

```
s_t = (B_t, G_t, M_t, P_t, R_t)
a_t ~ π(· | s_t, h_t)
s_{t+1} = T(s_t, a_t)
V(s_{t+1}) -> {accept, reject, rollback}
```

| 符号 | 含义 | 机器可读形式 |
|---|---|---|
| `B` | B-rep 实体/装配 | STEP AP242、BREP、XBF |
| `G` | 装配图：实例、配合、接触对 | JSON：`{instance, definition, transform, interfaces[]}` |
| `M` | 体/面网格与质量场 | `.msh`、`.inp`、`.med`、`.vtk` |
| `P` | 求解模型：材料、边界、载荷、步控制 | `.inp`、`.comm`、`.sif`、JSON |
| `R` | 结果与收敛元数据 | `.frd`、`.dat`、`.vtu`、JSON |
| `V` | 确定性校验器 | Python/CLI，退出码 + JSON 报告 |

只有 **`V` 可执行、且其结论门控下一步动作**，系统才算 agentic。没有 `V` 的系统只是带聊天界面的代码生成器。

### 1.1 不变量

任意状态迁移必须保持任务相关的不变量集合 `I`：

- `watertight(B) = true`、`is_valid(B) = true`、`n_solids ≥ 1`；
- `|ΔV| / V_0 ≤ ε_v`、`|Δm| / m_0 ≤ ε_m`；
- 接触集合 `C` 保持：`C_new ⊇ C_required`，`|C_new \ C_0| = 0`（除非显式声明）；
- 网格门：`minSICN ≥ q_min`、`n_bad ≤ n_bad,0`；
- 求解门：`converged = true`、`residual ≤ tol`、`n_iter < n_max`；
- 单位与基准一致：`unit_system`、`datum_frame`、`tolerance_stack`。

算不出 `I` 的 agent，不具备执行 `T` 的资格。

---

## 2. 分层模型

| 层 | 职责 | 开源参考实现 | 闭源参考实现 |
|---|---|---|---|
| L0 几何内核 | B-rep 求值、布尔、圆角、去特征 | OCCT / OCP | Parasolid、ACIS、CGM、ShapeManager |
| L1 建模 | 特征、草图、装配、工程图 | FreeCAD、build123d、CadQuery | SolidWorks、NX、Creo、CATIA、Inventor、Solid Edge、Fusion、Onshape |
| L2 几何准备 | 愈合、简化、特征识别 | OCCT、Analysis Situs、Salome GEOM | SpaceClaim、DesignModeler、ANSA、CADdoctor |
| L3 网格 | 四面体/六面体/边界层、质量指标 | Gmsh、Netgen、TetGen、MMG | ANSYS Meshing、HyperMesh、ANSA、STAR-CCM+ |
| L4 求解 | 结构、热、模态、显式、CFD、多体 | CalculiX、Code_Aster、Elmer、FEniCSx、MOOSE、FreeFEM、OpenFOAM、MBDyn、Chrono | ANSYS Mechanical/Fluent、Abaqus、Nastran、COMSOL、Simcenter、LS-DYNA |
| L5 后处理 | 场可视化、提取、报告 | ParaView、PyVista、meshio、ccx2paraview | CFD-Post、Tecplot、EnSight、HyperView |
| L6 Agent 接口 | 工具暴露、状态、校验、回滚 | freecad-mcp、build123d-mcp、agentcad、cadgen、PyAnsys MCP、PrePoMax MCP | 厂商 copilot / 专有 API |

层边界尽量落在**进程边界**上：GPL 工具（Gmsh、CalculiX、Code_Aster、OpenFOAM）以子进程调用；宽松许可库（build123d、CadQuery、meshio、PyVista）可进程内 import。

---

## 3. 能力包络（基于公开证据）

可靠性分档来自公开 benchmark；指标定义、样本量与口径见 [`docs/benchmarks.md`](docs/benchmarks.md)。

| 任务 | 当前档位 | 主导失效 | 证据 |
|---|---|---|---|
| 文本→参数化零件（简单图元） | **高**：有效率 > 90%，CD ≈ 44–53，IoU ≈ 0.54–0.59 | 尺寸漂移、漏特征 | Text2CAD-Bench L1 |
| 含扫掠/放样/抽壳的零件 | **低**：无效率 68–93% | 内核操作误用、退化截面 | Text2CAD-Bench L3 |
| 已有 B-rep 编辑 | **中**：编辑分 0.62–0.71 | 引用漂移、特征重排 | CADGenBench 编辑集 |
| 草图约束推断 | **中高**：PF1 0.979、CF1 0.484 | 约束冲突、过约束 | CAD-Assistant / SketchGraphs |
| FEA 模型端到端 | **低**：可执行率 0.88 时仅 2/15 有效目标 | 边界/材料/接触语义 | FEABench Gold |
| FEM 内核代码 | **线性高、非线性低** | 几何刚度、屈曲、有限转动 | FEM-Bench 2025 |
| 文本→刚体多体 | **高**：成功率 86–91% | 参数选择、关节限位 | MecEng L1–L2 |
| 文本→柔性多体 | **低**：几何→四面体网格→降阶的长链 | 任一阶段出错即中止 | MecEng L3 |
| 工程图问答 | **分化**：标题栏 ≈ 97%，装配 ≈ 46% | 投影规则、GD&T 语义 | MechVQA |
| GD&T 抽取 | **低**：召回 25–37%，返回项 41–56% 错 | 符号词表、基准参照 | A*STAR 400 图研究 |
| 长程 agent 工作流 | **中**：单问题闭源 96–97%、开源 55–78%；跨域 20–53% | 工具编排、检索、HPC 状态 | EngiAI |

---

## 4. Agent 接口模式

按确定性与影响面排序，共四种。

| 模式 | 传输 | 状态 | 典型工具 | 风险 |
|---|---|---|---|---|
| **MCP / JSON-RPC** | stdio 或 Streamable HTTP | 服务端会话 | freecad-mcp、build123d-mcp、PyMechanical-MCP | 工具白名单、鉴权、prompt injection |
| **进程内 Python API** | 函数调用 | 进程内存 | build123d、OCP、gmsh、PyVista | 内核崩溃会带走 agent 进程 |
| **CLI + 产物契约** | fork/exec | 文件系统 | FreeCADCmd、gmsh、ccx、FreeFEM、ParaView | 退出码歧义、部分产物 |
| **文件交换** | 共享卷 | 无 | STEP、BREP、`.inp`、`.frd`、`.med`、`.vtu` | schema 漂移、单位丢失、静默愈合 |

### 4.1 MCP 配置（stdio）

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

对 CAD 有实际影响的 MCP 语义：

- `tools/list` 是能力契约；缓存并哈希，作为可复现性的一部分；
- `tools/call` 必须返回**结构化内容**（JSON）+ 可选图像内容，而不是散文；
- 长操作需要 progress notification 与 cancellation；
- 会话状态必须显式：document id、active body、selection set、undo depth。

### 4.2 CLI 契约

每个 CLI 包装器应在 stdout 输出单个 JSON 对象，并约定退出码：

| 退出码 | 含义 | Agent 动作 |
|---|---|---|
| 0 | 成功，产物已写 | 校验产物 |
| 2 | 输入/ schema 错误 | 修复参数 |
| 3 | 几何失败（非流形、布尔失败） | 回滚，调整参数 |
| 4 | 网格失败/质量门 | 重划或简化 |
| 5 | 求解不收敛 | 调整控制，不接收结果 |
| 6 | 外部依赖缺失 | 停止，报告环境 |

### 4.3 校验循环

```python
state = load_step("part.step")
report = audit(state)                      # 质量属性、有效性、拓扑
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

**校验器才是产品，模型是可替换件。**

---

## 5. 参考架构

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

设计规则：

1. **单写者**：FreeCAD `App::Document` 与多数内核不是并发安全的。
2. **改前检查点**：保存 `(STEP, JSON state, hash)` 三元组；回滚是文件恢复，不是 undo。
3. **数值与视觉双通道**：截图能发现刚体位移，质量属性会发现尺度错误；单通道都不够。
4. **版本钉死**：内核、网格器、求解器、模型版本都进入可复现性哈希。
5. **GPL 进程隔离**：不把 GPL 求解器链接进分发二进制；用 `subprocess` + 产物契约。

---

## 6. 工具目录

完整表格（源码、许可证、功能、agent 接口）：[`docs/tool-catalog.md`](docs/tool-catalog.md)。

要点：

- **几何**：FreeCAD 1.1.x、build123d 0.13、CadQuery 2.8、OCCT/OCP 8.0。
- **网格**：Gmsh 4.15.2、Netgen/NGSolve 6.2、TetGen、MMG。
- **求解**：CalculiX 2.23、Code_Aster 17.4 / Salome-Meca 2025.1、Elmer、FEniCSx、MOOSE 5.0、FreeFEM 4.17、OpenFOAM、MBDyn、Chrono。
- **后处理**：ParaView 5.11、PyVista、meshio、ccx2paraview。
- **Agent 接口**：freecad-ai（64 工具）、freecad-mcp（17 工具）、build123d-mcp（38 工具）、agentcad、cadgen、PyAnsys MCP（Mechanical 28 工具、MAPDL、Fluent 20 工具）、PrePoMax 3.0 MCP。
- **闭源**：SolidWorks、NX、Creo、CATIA、Inventor、Solid Edge、Fusion、Onshape、SpaceClaim、ANSYS、Abaqus、COMSOL、Simcenter、HyperMesh、ANSA、SimScale、CAD Exchanger、Datakit。

### 6.1 Agent 生态

MCP server 与 agent-native CAD 项目的独立目录（按 star 与维护状态筛选）：[`docs/agent-ecosystem.md`](docs/agent-ecosystem.md)。

| 方向 | 代表 | Stars | 接口 |
|---|---|---:|---|
| FreeCAD | `neka-nat/freecad-mcp` | 3,254 | stdio MCP + XML-RPC |
| SolidWorks | `wzyn20051216/solidworks-automation-skill` | 1,867 | MCP + skill |
| Text-to-CAD | `earthtojake/text-to-cad` | 25,810 | CLI + MCP |
| Abaqus | `Cai-aa/abaqus-mcp` | 326 | MCP + plugin |
| COMSOL | `wjc9011/COMSOL_Multiphysics_MCP` | 944 | MCP |
| CAE 编排 | `Cai-aa/CAE-Agent-Hub` | 1,297 | MCP + skills |

阈值：热门方向（FreeCAD、SolidWorks、text-to-CAD、通用 CAD MCP）≥ 200 stars；冷门方向（CATIA、NX、Onshape、Fusion、code-CAD、CAE 求解器）≥ 100 stars。

---

## 7. 评测证据

指标定义与口径：[`docs/benchmarks.md`](docs/benchmarks.md)。

| Benchmark | 规模 | 公开最好结果 | 测什么 |
|---|---|---|---|
| Text2CAD-Bench | 600 CAD / 1,200 prompt | L1 CD 44.31、IR 11.1%、IoU 0.59；L3 IR 68–93% | 文本 → CadQuery 代码 |
| CADGenBench | 81 fixtures | 综合 0.677、有效率 98.77% | 有效性门控的生成 + 编辑 |
| CAD-Assistant | 1,700 测试件 | 2D 0.791、3D 0.857、CF1 0.484 | FreeCAD 上的工具增强 VLLM |
| FEABench | 15 Gold + 200 Large | 可执行率 0.88、2/15 有效目标 | COMSOL API 端到端 |
| FEM-Bench 2025 | 33 题 | 30/33 至少一次、26/33 五次全对 | FEM 代码 + 测试 |
| MecEng | 84 题、34 个 LLM | 刚体 91.4%；柔性显著更低 | 多体模型合成 |
| SCBench | 285 子任务 | 57.6% | 空间约束满足 |
| MechVQA | 3,281 图 / 21K 题 | 领域微调 84.85%；通用 77.28% | 工程图理解 |
| EngiAI | 2 个设计问题 | 闭源 96–97%、开源 55–78% | 工具连接的工作流 |

**不要跨 harness 横比。** 引用时同时给出 `(model, harness, retries, n_samples, benchmark_version)`。

---

## 8. 局限

完整分析：[`docs/limitations.md`](docs/limitations.md)。

1. **有效性 ≠ 保真**：水密实体也可能尺寸错误。
2. **全局约束整合失败**：局部几何合理，全局不变量不成立。
3. **物理语义缺失**：边界、材料、接触常被低估或写错。
4. **拓扑命名**：面/边的持久引用在参数化重建后失效。
5. **误差传播**：几何 → 网格 → 求解是乘性的，任一阶段失败即中止。
6. **评测口径不可比**：同一 benchmark，不同分数。
7. **数据稀缺与知识产权**：真实装配、标准、验证算例不公开。
8. **确定性与版本漂移**：模型、内核、工具版本都会改变输出。
9. **成本与延迟**：迭代循环放大 token 与算力开销。
10. **安全**：`execute_code` 是任意代码执行；图纸与 STEP 元数据是不可信输入。
11. **资质**：没有公开证据表明 LLM 生成的模型满足规范/法规验收。
12. **责任**：人仍是持证人与签署人。

---

## 9. 仓库结构

| 路径 | 内容 |
|---|---|
| [`README.md`](README.md) · [`README.zh-CN.md`](README.zh-CN.md) | 范围、分层模型、能力包络、接口模式、参考架构 |
| [`docs/tool-catalog.md`](docs/tool-catalog.md) | 开源/闭源工具：版本、许可证、源码、功能、agent 接口、无头能力 |
| [`docs/agent-ecosystem.md`](docs/agent-ecosystem.md) | 36 个 MCP server 与 agent-native CAD 项目，按 star 与维护状态筛选 |
| [`docs/agent-interfaces.md`](docs/agent-interfaces.md) | MCP/CLI/Python/文件契约、错误码、校验门、沙箱 |
| [`docs/benchmarks.md`](docs/benchmarks.md) | 指标定义、benchmark 结果、效度威胁、证据分级 |
| [`docs/limitations.md`](docs/limitations.md) | 12 个失效机制：观测、缓解、残余风险 |
| [`docs/reference-architecture.md`](docs/reference-architecture.md) | 状态机、JSON schema、回滚、确定性、反模式 |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | 收录标准、star 阈值、证据格式、PR checklist |
| [`scripts/check_links.py`](scripts/check_links.py) | 链接检查器；404/410 为硬失败，反爬为警告 |

---

## 10. 贡献

收录标准、证据要求与 PR 格式：[`CONTRIBUTING.md`](CONTRIBUTING.md)。

简版：

- 开源工具必须有公开源码仓库与 OSI 许可证；
- 闭源工具必须有公开产品页与可文档化的自动化接口；
- 每条记录必须给出 `source`、`license`、`function`、`agent surface`、`headless`；
- benchmark 结论必须给出 `benchmark`、`version`、`n`、`metric`、`harness`；
- 链接由 `scripts/check_links.py` 检查。

---

## 11. 许可证

MIT，见 [`LICENSE`](LICENSE)。

---

## 12. 参考

- Text2CAD-Bench：<https://arxiv.org/html/2605.18430>
- CADGenBench 指标：<https://github.com/huggingface/cadgenbench/blob/main/docs/metrics.md>
- CAD-Assistant：<https://cadassistant.github.io/>
- FEABench：<https://arxiv.org/abs/2504.06260>
- FEM-Bench：<https://doi.org/10.1007/s00366-026-02397-z>
- MecEng：<https://arxiv.org/abs/2608.14615>
- SCBench：<https://arxiv.org/html/2604.09594v1>
- MechVQA：<https://arxiv.org/html/2605.30794v2>
- EngiBench：<https://aclanthology.org/2026.findings-acl.1810/>
- EngiAI：<https://arxiv.org/html/2605.19743v3>
- Autodesk AI Pulse 2026：<https://www.autodesk.com/design-make/articles/2026-ai-pulse>
- McKinsey State of AI 2026：<https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai>

---

## Star history

<a href="https://star-history.com/#Misaka0x26FE/Awesome-Agentic-CAD&Date">
  <img src="https://api.star-history.com/svg?repos=Misaka0x26FE/Awesome-Agentic-CAD&type=Date" alt="Star history chart">
</a>

---

<div align="center">
<sub>为需要证据、而不是演示的工程师而建。· <a href="#top">回到顶部</a></sub>
</div>
