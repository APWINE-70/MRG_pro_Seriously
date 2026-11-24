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

