# Getting started with GroundBill

These instructions cover both **Windows** (PowerShell or Git Bash) and **macOS** (Terminal / zsh). Pick the OS block at each step.

## Prerequisites

- **Git** — [git-scm.com/downloads](https://git-scm.com/downloads)
- **Python 3.11 or newer** — [python.org/downloads](https://www.python.org/downloads/) (tick "Add Python to PATH" on the Windows installer)
- **Node.js 20 or newer** — [nodejs.org](https://nodejs.org/) (needed later for the frontend, not for day one)
- **VS Code** — [code.visualstudio.com](https://code.visualstudio.com/)
- **Claude Code** — follow the install steps at [docs.claude.com/claude-code](https://docs.claude.com/en/docs/claude-code/overview)

## First-time setup (5 minutes)

### 1. Choose a project folder

This repo is expected to live in a dedicated folder called `groundbill` (or whatever name you prefer — the folder name is not referenced by any code).

**Windows (PowerShell):**

```powershell
mkdir $HOME\groundbill
cd $HOME\groundbill
```

**Windows (Git Bash):**

```bash
mkdir -p ~/groundbill
cd ~/groundbill
```

**macOS:**

```bash
mkdir -p ~/groundbill
cd ~/groundbill
```

### 2. Copy the briefing and slash commands

Place `CLAUDE.md` at the folder root, and `commands.md` inside a `.claude/` sub-folder.

**Windows (PowerShell):**

```powershell
mkdir .claude -Force
Copy-Item <path-to>\CLAUDE.md .
Copy-Item <path-to>\commands.md .claude\commands.md
```

**Windows (Git Bash) / macOS:**

```bash
mkdir -p .claude
cp <path-to>/CLAUDE.md .
cp <path-to>/commands.md .claude/commands.md
```

### 3. Copy the reference Excel workbooks

The six authoritative Rev A workbooks go directly in `reference/excel/`. Rail-sector, legacy 2019, and supporting workbooks go in sub-folders — see [reference/excel/](reference/excel/) for the layout.

**Windows (PowerShell):**

```powershell
mkdir reference\excel\rail, reference\excel\legacy_2019, reference\excel\supporting -Force
# then copy each .xlsx / .xltm into the matching sub-folder
```

**Windows (Git Bash) / macOS:**

```bash
mkdir -p reference/excel/rail reference/excel/legacy_2019 reference/excel/supporting
# then copy each .xlsx / .xltm into the matching sub-folder
```

Expected structure:

```
reference/excel/
├── 1_BOQ_Log_Rev_A.xlsx
├── 2_BOQ_Calculator_Rev_A.xlsx
├── 3_BOQ_Quantities_Rev_A.xlsx
├── 4_BOQ_Contractor_Rev_A.xlsx
├── 5_Schedule_2_Rev_A.xlsx
├── 6_BOQ_GI_Estimate_Rev_A.xlsx
├── rail/
├── legacy_2019/
└── supporting/
```

### 4. Initialise git

**Windows (PowerShell):**

```powershell
git init
@(".venv/", ".env", "node_modules/", "__pycache__/", "*.pyc", ".DS_Store", "Thumbs.db") | Out-File -Encoding utf8 .gitignore
git add CLAUDE.md .claude/ .gitignore
git commit -m "initial: project brief and slash commands"
```

**Windows (Git Bash) / macOS:**

```bash
git init
cat > .gitignore <<'EOF'
.venv/
.env
node_modules/
__pycache__/
*.pyc
.DS_Store
Thumbs.db
EOF
git add CLAUDE.md .claude/ .gitignore
git commit -m "initial: project brief and slash commands"
```

> `.DS_Store` is a macOS Finder metadata file; `Thumbs.db` is its Windows equivalent. Both are safe to ignore.

### 5. Open the folder in VS Code

**Windows (PowerShell):**

```powershell
code $HOME\groundbill
```

**Windows (Git Bash) / macOS:**

```bash
code ~/groundbill
```

## Starting Claude Code

Open a terminal inside VS Code (**View → Terminal**, or `` Ctrl+` `` on Windows / `` Cmd+` `` on macOS), then run:

```
claude
```

Claude Code will read `CLAUDE.md` automatically and orient itself to the project. Its first response should tell you where the project stands and ask which step you want to work on.

## Your opening message

The first thing to say is:

> Read CLAUDE.md and .claude/commands.md, then run /status.

That triggers the status command, which will report where you are and suggest the next step. From there, follow the build order one step at a time.

## Moving between Windows and Mac

Because all day-to-day paths in this project are **relative** (e.g. `reference/excel/1_BOQ_Log_Rev_A.xlsx`), the repo works identically on both operating systems once git is set up. To move between machines, push to a private remote (GitHub / GitLab) from one and `git clone` on the other — do not rely on OneDrive or iCloud for the working copy, as in-flight syncs can corrupt the Python virtualenv.

Per-OS differences to be aware of:

- **Line endings:** run `git config --global core.autocrlf input` on Windows and `core.autocrlf input` on macOS to keep text files as LF in the repo.
- **Virtualenv:** `.venv/` is listed in `.gitignore`, so recreate it on each machine with `python -m venv .venv` rather than syncing it.
- **Macro-enabled templates** (`.xltm`) in `reference/excel/legacy_2019/` open on both OSes but Excel for Mac has limited VBA support — treat those templates as read-only reference material on Mac.
