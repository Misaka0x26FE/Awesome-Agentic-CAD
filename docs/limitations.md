# Limitations of current Agentic CAD

Each limitation is written as a failure mechanism: how it arises, how to observe it, what mitigation exists, and what residual risk remains after mitigation.

---

## L1. Validity is not fidelity

**Mechanism.** A solid can be watertight, manifold, and meshable while being dimensionally wrong, missing a feature, or built on the wrong datum. Validity checks operate on topology; design intent lives in dimensions, constraints, and mating conditions.

**Observable.** `BRepCheck_Analyzer` returns true; `Volume` differs by 0.5%; a boss is 2 mm off; a hole pattern has 5 holes instead of 6.

**Mitigation.** Gate on multiple independent measurements: volume, mass, bbox, centroid, face count, feature recognition, and mating-feature keep-in/keep-out volumes.

**Residual risk.** Measurement coverage is finite; a model can satisfy every measured scalar and still violate an unmeasured intent.

**Evidence.** Text2CAD domain model: IR 2%, CD 220, IoU 0.04. CADGenBench: 98.77% validity at 0.677 aggregate.

---

## L2. Global constraint consolidation

**Mechanism.** LLMs construct locally plausible geometry and fail to maintain global invariants: genus, shell count, connectivity, assembly graph isomorphism, tolerance chains.

**Observable.** Final partition has the wrong face count class; a bracket has a disconnected island; an assembly loses a mate after an upstream edit.

**Mitigation.** External graph checks (Betti numbers, connectivity, mate graph), not model self-report. Reject on any invariant violation.

**Residual risk.** Encoding every global constraint is equivalent to writing a formal spec; under-specified tasks remain unverifiable.

**Evidence.** SCBench: best 57.6%, dominant failure "Local-Only". MecEng: graph isomorphism is the stage where many otherwise valid models fail.

---

## L3. Physical semantics

**Mechanism.** Boundary conditions, material models, contact definitions, and step controls are under-specified in natural language and easy to mis-map to solver keywords. The solver may converge on a physically meaningless model.

**Observable.** Reaction force does not balance applied load; temperature equals a solver default; contact status shows no closed pairs; rigid-body modes appear in a static solve.

**Mitigation.** Require a model-setup manifest: units, material ids, BC surfaces, load totals, contact pairs, step type, solver controls. Verify sum of reactions and energy balance before accepting fields.

**Residual risk.** A model can be internally consistent and still wrong relative to the real structure (wrong idealization, wrong boundary stiffness).

**Evidence.** FEABench: 2/15 valid targets at 0.88 executability; the single strict pass matched a COMSOL default temperature.

---

## L4. Topological naming

**Mechanism.** Parametric features reference faces, edges, and vertices by identifiers derived from construction history. Rebuild after an upstream change can rename, split, merge, or delete the referenced entity.

**Observable.** `Invalid shape name ?Face3`; downstream feature rebuilds on the wrong face; assembly mate silently attaches to a different vertex.

**Mitigation.** Reference datums and named selections, not raw face indices. Snapshot before edits. Prefer non-parametric defeaturing for analysis models, where history stability matters less.

**Residual risk.** Datum discipline reduces but does not eliminate failures in boolean-heavy histories; kernel-level naming remains an open problem.

**Evidence.** FreeCAD TNP V2 is still a draft PR (#31040) as of 2026-11; 1.1.x includes mitigation, not a complete fix.

---

## L5. Error propagation

**Mechanism.** Geometry → mesh → solve → post is a multiplicative chain. A 0.1 mm geometry error can change mesh topology; a bad element can shift an eigenfrequency; a wrong unit scales everything.

**Observable.** Eigenfrequency shifts 3–8% between simplification levels; contact area changes 10%; mesh quality collapses locally.

**Mitigation.** Stage gates with numeric tolerances; checkpoint and rollback; sensitivity runs at two mesh densities.

**Residual risk.** Tolerance stacking across stages can pass each gate and still exceed the final engineering tolerance.

**Evidence.** MecEng: flexible multibody tasks fail when any single stage fails. Internal CAD work: 65/68 parts meshed, 2 contact pairs above 1% area change after simplification.

---

## L6. Benchmark non-comparability

**Mechanism.** Scores depend on harness, retries, prompt, model effort, tool availability, and submission validation. Leaderboards mix all of these.

**Observable.** The same CADGenBench appears at 0.44 and 0.68 in different trackers; "best model" changes with retry budget.

**Mitigation.** Report `(model, harness, retries, n, version)`; reproduce on your own fixtures; prefer deterministic verifiers over judge models.

**Residual risk.** Even a fully specified harness is not the deployment harness.

**Evidence.** CADGenBench submissions include validated and unvalidated entries; Text2CAD-Bench explicitly warns about survivorship bias.

---

## L7. Data scarcity and IP

**Mechanism.** High-quality assemblies, GD&T, material cards, and validation cases are proprietary. Public datasets are dominated by simple parts. Models trained on public data underperform on production geometry.

**Observable.** Strong benchmark scores, weak performance on the first real assembly; frequent hallucinated standard parts.

**Mitigation.** Build an internal regression set with 10–20 real parts and fixed acceptance metrics; fine-tune or retrieve on internal standards.

**Residual risk.** Internal data cannot be shared, so external validation of the agent remains limited.

---

## L8. Determinism and version drift

**Mechanism.** Model aliases update silently; kernel versions change fillet/boolean behavior; mesher versions change element counts; solver versions change contact defaults.

**Observable.** Same prompt, different STEP hash; same STEP, different mesh; same deck, different convergence path.

**Mitigation.** Pin model ids, tool versions, and container digests; record them in the artifact manifest; re-baseline on upgrade.

**Residual risk.** Hosted models can change without a version bump.

---

## L9. Cost and latency

**Mechanism.** Agent loops multiply calls: each repair iteration resends context, each verification emits JSON, each screenshot adds image tokens. CAD/CAE operations are seconds to hours.

**Observable.** A 10-iteration repair costs 10–30× a single shot; a modal solve blocks the loop.

**Mitigation.** Fixed-size observations, cached schemas, early exit on gate failure, asynchronous jobs with progress, local small models for classification.

**Residual risk.** Long-horizon tasks remain economically unattractive for high-value, low-volume engineering.

---

## L10. Security

**Mechanism.** `execute_code` tools provide arbitrary code execution. STEP metadata, drawing text, file names, and tool descriptions are untrusted input and can carry prompt injection. MCP servers may expose destructive tools without authentication.

**Observable.** Unexpected file writes; network calls; tool calls not present in the plan; instructions embedded in a drawing note.

**Mitigation.** Process isolation, read-only inputs, network deny, tool allowlist, per-call approval for destructive operations, artifact hashing, audit logs.

**Residual risk.** A compromised kernel or dependency executes with the agent's privileges.

---

## L11. Qualification and acceptance

**Mechanism.** Engineering deliverables are accepted against codes, standards, and documented verification. LLM-generated models have no qualification trail: no V&V report, no uncertainty quantification, no traceability to a validated method.

**Observable.** A regulator or customer asks for the verification matrix; the agent produced a model but not the evidence.

**Mitigation.** Treat the agent as a model builder, not a qualifier. Generate the V&V artifacts (mesh convergence, comparison to reference, sensitivity) as part of the pipeline.

**Residual risk.** The qualification boundary is organizational, not technical; it cannot be automated away.

---

## L12. Responsibility

**Mechanism.** The professional of record signs the design. An agent cannot hold a license, accept liability, or certify compliance.

**Observable.** No signature, no stamp, no accountable reviewer.

**Mitigation.** Human review at defined checkpoints; agent output marked as draft; decisions logged with rationale.

**Residual risk.** Automation bias: reviewers approve plausible outputs without re-deriving them.

---

## Cross-cutting: what would change the conclusion

| Assumption | Falsifier |
|---|---|
| Validity gates are insufficient | A benchmark showing validity + mass + topology predicts engineering acceptance |
| Global constraints need external checkers | A model that reliably enforces invariants without tools |
| Physical semantics are the bottleneck | FEA agents passing Gold with correct BCs and no defaults |
| Long chains remain fragile | Flexible multibody success approaching rigid-body rates |
| Harness dominates scores | Inter-harness variance below 2 points on the same benchmark |

Until one of these is demonstrated, the design rules in [`reference-architecture.md`](reference-architecture.md) hold.
