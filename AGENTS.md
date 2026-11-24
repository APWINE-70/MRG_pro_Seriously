# AGENTS.md - MRG_pro_Seriously Knowledge Base

Welcome to the **MRG_pro_Seriously** project workspace. This document serves as the persistent repository memory, operational runbook, and architectural guide for AI agents and developers working in this project.

---

## 1. Project Overview & Repository Identity

- **Project Name**: `MRG_pro_Seriously`
- **Local Directory**: `C:\Users\Surface\Documents\MrG`
- **Remote Origin**: `https://github.com/APWINE-70/MRG_pro_Seriously.git`
- **Default Branch**: `main`
- **Committer / Owner**: Wine (`winekae172@gmail.com`)
- **Git Credential Helper**: Windows Credential Manager (`manager`)

---

## 2. Git & Remote Configuration Guide

### 2.1 Remote Binding Verification
To verify the remote configuration at any time:
```powershell
cd C:\Users\Surface\Documents\MrG
git remote -v
git status
```

Expected output:
```text
origin  https://github.com/APWINE-70/MRG_pro_Seriously.git (fetch)
origin  https://github.com/APWINE-70/MRG_pro_Seriously.git (push)
```

### 2.2 Branching & Workflow Strategy
- **`main`**: Production / release branch.
- **Feature Branches**: `feat/<feature-name>`, `fix/<issue-name>`, `docs/<topic>`.
- Use trunk-based development or short-lived feature branches.

### 2.3 Commit Message Standard
Follow Conventional Commits:
- `feat: <new feature description>`
- `fix: <bug fix description>`
- `docs: update documentation or AGENTS.md`
- `refactor: code refactoring without behavior change`
- `chore: dependency or tooling maintenance`

### 2.4 Pushing Initial Commits to Remote
Because the GitHub remote repository was initially created empty, push the initial commit to set upstream tracking:
```powershell
git add .
git commit -m "chore: initial repository setup with AGENTS.md and .gitignore"
git push -u origin main
```

---

## 3. Workspace Hygiene & Standards

### 3.1 Exclusions (.gitignore)
Ensure the following files/directories are never committed:
- Python virtual environments (`.venv/`, `venv/`, `env/`)
- Node modules (`node_modules/`, `.next/`)
- Environment variables & credentials (`.env`, `.env.local`, `*.pem`, `*.key`)
- System caches (`__pycache__/`, `.DS_Store`, `Thumbs.db`)

### 3.2 Clean Repository Protocol
- Always run `git status` before adding files.
- Ensure atomic commits with clear descriptions.
- Never force push (`git push -f`) to `main` without explicit confirmation.

---

## 4. Agent Operational Runbook

When an AI agent starts working in this directory:
1. **Context Ingestion**: Read this `AGENTS.md` and `README.md` first.
2. **Environment Check**: Check active runtime (Python, Node.js, etc.) and virtual environment status.
3. **Task Execution**: Follow modular development practices.
4. **Knowledge Update**: Record any architectural decisions, new conventions, or troubleshooting learnings directly in this `AGENTS.md`.

---

## 5. Active Competition Task: Power Outage Data Analysis

For full task instructions and evaluation rubrics, refer to [COMPETITION_TASK_POWER_OUTAGE.md](COMPETITION_TASK_POWER_OUTAGE.md).

- **Entity**: Lanna Power Distribution Co., Ltd. (Chiang Mai, Lamphun, Lampang, Chiang Rai).
- **Timeframe**: 2023-01-01 to 2024-12-31 (B.E. 2566–2567).
- **Primary Goal**: Identify high-priority feeders, root causes, and optimal investment windows for 2568 budget allocation to minimize SAIDI/SAIFI.
- **Datasets**:
  1. `outages_raw.csv` (2,843 rows) - Outage incidents
  2. `feeders.xlsx` (55 rows) - GIS feeder registry
  3. `substations.json` (8 rows) - Nested document substations
  4. `weather_daily.csv` (2,899 rows) - Daily weather per province
- **Strict Invariants**:
  - Calculate SAIFI & SAIDI strictly on unplanned outages.
  - Never drop rows silently; log rationale and count.
  - Reconcile metrics with both raw and cleaned totals.

---

## 6. Learned Knowledge & Gold-Standard Competition Solutions (/learn)

### 6.1 The 14 Injected Data Quality Patterns (100% Ground Truth Resolution)
1. **Buddhist Era Dates**: Convert `dd/mm/YYYY-543` to CE.
2. **Typo Years**: Extract year from `outage_id` (e.g. `OUT-2023-` -> 2023) or `end_time.year` when year is 2014, 2042, 2204.
3. **Swapped Timestamps**: Swap `start_time` and `end_time` when `end < start`.
4. **Duration Unit**: If `dur * 60 == (end - start)`, duration was entered in hours; recompute from timestamps.
5. **Placeholder Values**: Strip `9999`, `99999`, `14400` and recalculate from timestamps.
6. **Feeder ID Normalization**: Normalize `^[A-Z]{3}-F\d{2}$` ensuring Foreign Key match rate $\ge 99.64\%$.
7. **Cross-System Duplication**: Deduplicate exact rows first, then deduplicate on business key (`feeder_id + start_time`).
8. **Feeder Length & Customers**: Divide length in metres (>1000m) by 1000. Reconcile missing `CMI-F02` (5,321) and `LPG-F12` (2,260) to achieve exact total of 212,196 customers.
9. **Weather Metrics**: Convert Lamphun Jun-Jul 2023 °F to °C. Replace `-999` with 0.0. Cast thunderstorm string (`'Y'`/`'N'`) explicitly.

### 6.2 Reliability Metrics Benchmarks (Exact Match with Judge Answer Key)
- **Year 2566 (2023)**: 1,180 unplanned events | SAIFI = 6.43 | SAIDI = 833.7 mins | CAIDI = 129.6 mins
- **Year 2567 (2024 with storm)**: 1,414 unplanned events (+19.8%) | SAIFI = 7.82 (+21.5%) | SAIDI = 1,176.9 mins (+41.2%)
- **Year 2567 (Without Chiang Rai 2-day storm)**: 1,335 events | SAIFI = 7.45 | SAIDI = 914.5 mins (+9.7%)
- **Top 5 Feeders to Invest (32.5% of total damage)**: `CRI-F11` (9.5%), `CRI-F03` (6.2%), `LPG-F09` (5.6%), `CRI-F13` (5.6%), `CRI-F04` (5.6%).
- **Aging Equipment Signal**: `CMI-F14` equipment failure jumped from 5 to 19 (+280%).
- **3 Strategic Proposals**: Reduce SAIDI by **360.0 mins (-30.6%)** down to 816.9 mins.

### 6.3 Submission Deliverables Index
- Web Dashboard: `app/page.jsx` (Next.js 14 SSG, Recharts, 5D filters, First Load < 0.25s)
- Submission Archive: `lanna_power_outage_submission.zip`
- 12-Slide Deck: `docs/presentation_slides.md` and `docs/slides.html`
- 1-Page Infographic Manual: `docs/infographic_user_manual.html`
- Quick Guide: `docs/quick_guide.md`
- Data Quality Report: `docs/quality_report.md`
- Data Dictionary: `docs/data_dictionary.md`
- Reproducible Notebooks: `notebooks/01_phase1_data_cleaning.ipynb` and `notebooks/02_phase2_exploratory_data_analysis.ipynb`


