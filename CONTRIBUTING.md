# Contributing

This repository is a technical index, not a link dump. Every entry must be verifiable and every claim must carry its measurement context.

---

## 1. What we accept

### Tools

- **Open source**: public repository, OSI-approved license, build/install instructions, documented automation surface.
- **Closed source**: public product page, documented API/CLI/automation surface, and a statement of platform and licensing model.
- **Agent surfaces**: MCP server, agent skill, or agent-native SDK with a stated transport and tool inventory.

### Evidence

- benchmark results with `benchmark`, `version`, `n`, `metric`, `harness`;
- failure analyses with reproduction steps;
- negative results are welcome if they are reproducible.

### Rejected

- prompt collections without an executable component;
- repositories with no license and no license statement (may be listed only in a clearly marked "unlicensed" note);
- abandoned projects (no push for 12 months) unless historically important, marked `historical`;
- marketing claims without a public artifact.

---

## 2. Star thresholds

| Direction class | Threshold |
|---|---|
| Popular (FreeCAD, SolidWorks, text-to-CAD, general CAD MCP) | ≥ 200 stars |
| Niche (CATIA, NX, Onshape, Fusion, code-CAD, CAE solvers) | ≥ 100 stars |

Stars are a discovery filter, not a quality score. A project below threshold may be mentioned as a gap or a historical note, but not as a catalog entry.

---

## 3. Entry format

For tool catalog entries:

```markdown
| Tool | Version | License | Source | Function | Agent surface | Headless |
```

For ecosystem entries:

```markdown
| Repo | Stars | License | Last push | What it is | Interface |
```

Rules:

- link the canonical repository, not a mirror or a fork;
- use the SPDX identifier; write `no license` when none is declared;
- state the transport (`stdio`, `HTTP`, `CLI`, `Python`, `REST`);
- state prerequisites (Windows-only, licensed host, GUI session);
- do not copy marketing copy; describe the mechanism.

---

## 4. Benchmark claims

Every number must be accompanied by:

```
benchmark: <name and version>
model: <exact id and effort>
harness: <tool set, retries, prompt>
n: <samples>
metrics: <metric=value>
validity: <rate>
```

Numbers without this block are removed.

---

## 5. Pull request checklist

- [ ] links resolve (`python scripts/check_links.py`);
- [ ] no duplicated entries;
- [ ] license and stars verified on the day of submission;
- [ ] benchmark claims include harness and sample size;
- [ ] text is technical, no superlatives without measurement;
- [ ] tables render (no unescaped `|` inside cells).

---

## 6. Link check

```bash
python scripts/check_links.py
```

The script extracts `http(s)` URLs from Markdown, performs a HEAD request with a GET fallback, and prints a status table. Exit code 1 indicates at least one 4xx/5xx.

Network access is required. Some hosts block automated requests; failures are reported, not silently ignored.

---

## 7. Style

- English is the primary language; `README.zh-CN.md` mirrors the top-level document.
- Units: SI, with explicit unit strings.
- Identifiers: backticks for code, file names, and tool names.
- No emoji in technical tables.
- Prefer measured statements: "17.1% of tasks produced executable but physically wrong models" over "often wrong".
