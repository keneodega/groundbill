# GroundBill — GI contract pack generator

You are helping build GroundBill, a web application that generates Ground Investigation (GI) contract documents for engineering consultancies, developers, and project managers in Ireland and the UK.

## Who you are working with

The user is Havilah, a Chartered-track geotechnical engineer with working Python skills but not a professional developer. She is building this as a side project alongside full-time consultancy work.

Treat her as a capable collaborator who understands the geotechnical domain fluently but needs clear explanations of unfamiliar software engineering concepts. Never assume she knows frontend conventions, deployment workflows, or backend patterns without confirming. When you introduce a new tool, library, or pattern, briefly explain what it is and why it matters before using it. Prefer one-step-at-a-time progress over large bundled changes she cannot follow.

Use UK English in all code comments, documentation, and UI copy.

## What the product does

GroundBill takes one project definition — site details, number and type of exploratory holes, depths, test requirements, ground conditions, and contract route (private or Irish Public Works Contract PW-CF) — and produces three coordinated, downloadable documents:

1. Bill of Quantities (BOQ) in .xlsx, structured across Sections A–L:
   - A: General items and provisional services
   - B: Cable percussion boring
   - C: Rotary drilling
   - D: Pitting and trenching
   - E: Sampling and monitoring
   - F: Probing and cone penetration testing (CPT)
   - G: Geophysical testing
   - H: In-situ testing
   - I: Instrumentation
   - J: Installation monitoring
   - K: Geotechnical laboratory testing
   - L: Geoenvironmental laboratory testing
2. Schedule of Exploratory Holes (Schedule 2) in .xlsx, listing every hole with its number, type, grid reference, scheduled depth, and remarks (test selections).
3. Specification document in .docx, assembled from a modular clause library with project-specific variables populated. The PW-CF route references TII and OPW standards and uses mandated clause numbering; the private route uses a flexible bespoke structure.

All three documents are generated from one data model, so they are internally consistent. If the user specifies 10 boreholes to 15m with SPTs at 1m intervals, that fact flows into the BOQ quantities, the Schedule 2 rows, and the relevant specification clauses simultaneously.

## Why this exists

Consultancies produce these three documents manually and separately today. Inconsistencies between them are common — the spec says one thing, the BOQ prices another. A BOQ pack typically takes two to three days of engineer time per project. GroundBill compresses that to minutes by encoding the domain logic once and reusing it across every output.

Havilah has a working Excel-based system that encodes the full BOQ calculation logic across six linked workbooks (Log Tracker, Calculator, Quantities, Contractor BOQ, Schedule 2, GI Estimate). These live in `reference/excel/` in this repo. The Python calculation engine we are building is a translation of that Excel logic into clean, testable, maintainable code. Reference those workbooks rather than reinventing the rules.

## Tech stack

Backend:
- Python 3.11+
- FastAPI for the REST API
- Pydantic v2 for data models and validation
- openpyxl for Excel output
- python-docx for Word output
- SQLAlchemy plus PostgreSQL for persistence
- pytest for testing
- ruff for linting, black for formatting

Frontend:
- React 18 with Vite
- TypeScript
- TanStack Query for server state
- Tailwind CSS for styling
- shadcn/ui for components
- react-hook-form plus zod for form handling

Infrastructure (deferred until MVP is working locally):
- Auth: Clerk (free tier) — decision deferred
- Payments: Stripe with Stripe Billing
- Hosting: Railway (backend plus Postgres), Vercel (frontend)

Local development:
- Python virtual environment at `./.venv/`
- Node 20+
- Docker Compose for local Postgres

## Repository layout

```
groundbill/
├── CLAUDE.md                    — this file
├── README.md                    — human-facing project overview
├── .claude/
│   └── commands.md              — slash commands
├── backend/
│   ├── pyproject.toml
│   ├── src/groundbill/
│   │   ├── models/              — Pydantic domain models (Project, Hole, TestSuite)
│   │   ├── engine/              — calculation engine (one module per BOQ section)
│   │   │   ├── section_a.py
│   │   │   ├── section_b.py
│   │   │   └── ...
│   │   ├── generators/          — output generators (boq.py, schedule2.py, spec.py)
│   │   ├── clauses/             — specification clause library
│   │   ├── api/                 — FastAPI routes
│   │   └── db/                  — SQLAlchemy models and migrations
│   └── tests/
│       ├── fixtures/            — sample project definitions for testing
│       └── test_*.py
├── frontend/
│   ├── package.json
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── lib/                 — API client, utilities
│   │   └── App.tsx
│   └── vite.config.ts
├── reference/
│   ├── excel/                   — Havilah's source Excel workbooks
│   └── specs/                   — example GI specifications (redacted)
└── docker-compose.yml
```

## Domain model — the core abstraction

The single source of truth is a `Project` object. Everything else is derived from it.

```python
class Project:
    name: str
    site_address: str
    contract_route: Literal["private", "pw_cf"]
    site_category: Literal["green", "yellow", "red"]
    boreholes: list[Borehole]
    trial_pits: list[TrialPit]
    trenches: list[Trench]
    inspection_pits: list[InspectionPit]
    dynamic_samples: list[DynamicSample]
    soakaways: list[Soakaway]
    dynamic_probes: list[DynamicProbe]
    cpts: list[CPT]
    lab_schedule: LabSchedule
```

Each hole type has its own schema matching the columns in Havilah's Log Tracker workbook (`reference/excel/1_BOQ_Log_Rev_A.xlsx`). Use the Log Tracker sheet headers as the authoritative field list — do not invent fields.

The BOQ calculation engine is a set of pure functions. Each function takes a `Project` and returns a list of priced line items for one BOQ section. The generators then format those line items into the required output file.

## Principles for this codebase

1. Translate the Excel rules exactly. When implementing a BOQ section, open the corresponding sheet in the Calculator workbook, read the formulas, and translate them into Python. Do not paraphrase or "improve" the logic without flagging it explicitly. If a rule looks wrong, stop and ask before changing it.

2. Test every calculation rule against a known fixture. For every BOQ section, create at least one test fixture (a sample project) with known-correct expected quantities from the Excel system. Use these as regression tests.

3. Pure functions for the engine, side effects only at the edges. The calculation engine must be pure Python functions with no database, file, or network access. File generation is a separate layer. This makes the engine trivially testable.

4. Explicit is better than implicit. Name BOQ items using their full section code (e.g. `B1.1.1`) in code. When a line item is computed from multiple inputs, document the rule in a docstring with a reference to the Excel source.

5. Small, reviewable commits. After each meaningful unit of work, pause and describe what changed so Havilah can confirm before moving on. Never commit code without her sign-off during the MVP phase.

6. Explain unfamiliar concepts. If you use a pattern or tool Havilah may not know (dependency injection, async context managers, React hooks, TypeScript generics), add a one-line comment or a brief note explaining it.

## MVP scope — Tier 1 only

For the MVP, build only the consultant-facing interface. Defer the developer/PM wizard (Tier 2) and contractor pricing interface (Tier 3).

MVP features:
- Sign up and sign in (defer until after core engine is working)
- Create a project with a web form that mirrors the Log Tracker columns
- Generate all three documents on demand
- Download the three documents as a .zip
- Save projects to Postgres and list the user's projects

Not in MVP:
- Multi-user collaboration
- Contractor pricing interface
- Guided wizard for non-geotechnical users
- Payments and billing (add once MVP is validated with real users)
- Email notifications
- PDF output

## Build order

Follow this order unless Havilah explicitly redirects:

1. Set up the backend project structure and Python environment
2. Define the core Pydantic models (Project, Borehole, etc.) matching the Log Tracker columns
3. Build Section A of the calculation engine with a test fixture
4. Build the BOQ Excel generator for Section A and verify output matches the reference workbook
5. Iterate through Sections B–L one at a time, each with tests
6. Build the Schedule 2 generator
7. Build the Specification clause library and .docx generator
8. Set up the FastAPI routes for project CRUD and document generation
9. Scaffold the React frontend with a basic form
10. Wire the frontend to the API
11. Add Postgres persistence
12. Add authentication
13. Deploy to Railway and Vercel

Do not jump ahead. Finish each step to a tested, working state before starting the next.

## Working conventions

- Before starting any task, read the relevant Excel sheet in `reference/excel/` if the task involves BOQ logic.
- When you implement a calculation rule, quote the source Excel formula in a comment above the Python code.
- Prefer composition over inheritance for domain models.
- Use type hints everywhere. Run `ruff` and `black` before committing.
- Never commit credentials, API keys, or `.env` files. Add them to `.gitignore` from the start.
- For every new module, write at least one test that exercises the happy path.
- When stuck on a geotechnical interpretation, ask Havilah rather than guessing. She is the domain expert.
- When stuck on a software engineering decision, explain the options with trade-offs and let her choose.

## First actions on opening the project

When Claude Code starts in this folder, it should:
1. Read this file
2. Read `.claude/commands.md` for available slash commands
3. Check whether `backend/` and `frontend/` exist; if not, we are at step 1 of the build order
4. Check for a Python virtualenv at `.venv/`; if missing, offer to set it up
5. Ask Havilah which step of the build order she wants to work on, or confirm the next step in sequence

Do not start writing code on the first turn. Orient first, confirm with Havilah, then proceed.
