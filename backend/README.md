# GroundBill backend

FastAPI + Pydantic service that generates the three coordinated GI contract documents (BOQ, Schedule 2, Specification) from a single `Project` definition.

## Layout

```
backend/
├── pyproject.toml
├── src/groundbill/
│   ├── models/       — Pydantic domain models
│   ├── engine/       — pure-function BOQ calculation engine (one module per section A–L)
│   ├── generators/   — output generators (BOQ .xlsx, Schedule 2 .xlsx, Spec .docx)
│   ├── clauses/      — specification clause library
│   ├── api/          — FastAPI routes
│   └── db/           — SQLAlchemy models and Alembic migrations
└── tests/
    ├── fixtures/     — sample Project definitions with known expected outputs
    └── test_*.py
```

## Local development

From the **project root** (not `backend/`):

### Create and activate the virtual environment

**Windows (PowerShell):**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Windows (Git Bash):**

```bash
python -m venv .venv
source .venv/Scripts/activate
```

**macOS:**

```bash
python -m venv .venv
source .venv/bin/activate
```

### Install the backend in editable mode with dev extras

```bash
pip install -e "./backend[dev]"
```

Editable install (`-e`) means changes to the source code are picked up immediately without reinstalling.

### Run the test suite

```bash
pytest backend/
```

### Lint and format

```bash
ruff check backend/
black backend/
```

## Adding a dependency

1. Add the package name + version spec to `backend/pyproject.toml` under `dependencies` (runtime) or `optional-dependencies.dev` (tooling / tests only).
2. Re-run `pip install -e "./backend[dev]"` to pull it in.
