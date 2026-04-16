# GroundBill slash commands

These are the recurring workflows for this project. When Havilah types one of these commands in Claude Code, follow the linked procedure.

## /status

Report the current state of the project:
1. Which step of the build order are we on?
2. What was the last thing worked on (check git log and recent file modifications)?
3. Are there any failing tests? Run `pytest -q` in `backend/` if it exists.
4. What is the next logical step?

Keep the report short — a paragraph or a short list. End with "Next up: …" and wait for confirmation before starting work.

## /translate-section

Translate a BOQ section from Excel to Python. Ask which section (A–L) if not specified.

Procedure:
1. Open the relevant sheet in `reference/excel/2_BOQ_Calculator_Rev_A.xlsx` using openpyxl.
2. List every formula in that sheet with its cell address.
3. For each formula, explain in plain English what rule it encodes and which Log Tracker columns it reads.
4. Present this as a translation plan for Havilah to review before any Python is written.
5. Once approved, implement each rule as a pure function in `backend/src/groundbill/engine/section_<letter>.py`, with the source formula quoted in a comment above each function.
6. Write a test for each rule in `backend/tests/test_section_<letter>.py` using a known-input/known-output fixture.
7. Run the tests. Do not mark the section done until all tests pass.

## /new-fixture

Create a new test fixture — a sample `Project` with known expected BOQ quantities.

Procedure:
1. Ask Havilah for a short description of the site (e.g. "5 boreholes to 10m with SPTs, 3 trial pits with DCP").
2. Build the `Project` object in `backend/tests/fixtures/<name>.py`.
3. Compute the expected quantities by loading Havilah's Excel system with the same inputs and reading the Contractor BOQ output.
4. Record those expected values in `backend/tests/fixtures/<name>_expected.json`.
5. Write a test that runs the Python engine against the fixture and compares to the expected values.

## /verify-excel

Verify that the Python engine output matches the Excel reference output for a given fixture.

Procedure:
1. Load the named fixture.
2. Run the engine to produce BOQ line items.
3. Load the Excel-generated Contractor BOQ for the same inputs (from `reference/excel/fixtures/<name>.xlsx`).
4. Compare every line item. Report any mismatches with section, item code, Python value, and Excel value.
5. If mismatches are found, stop and ask Havilah which is correct before proceeding.

## /explain

Havilah encountered a concept she wants explained. Give a short, plain-English explanation in the context of this project.

Procedure:
1. Read the surrounding code or context.
2. Explain the concept in two to three paragraphs maximum.
3. Show a concrete example from this codebase if one exists.
4. Offer to go deeper if she wants more detail.

## /commit

Prepare a commit.

Procedure:
1. Run `git status` and `git diff --stat` to see what changed.
2. Run `ruff check backend/` and `black --check backend/` — fix any issues.
3. Run `pytest -q backend/` — do not commit if tests fail.
4. Draft a conventional commit message (e.g. `feat(engine): add section B cable percussion rules`).
5. Show Havilah the message and ask for approval before running `git commit`.

## /deploy-check

Before deploying, verify the app is ready.

Procedure:
1. All tests pass.
2. No secrets in any committed file (grep for common patterns: `API_KEY`, `SECRET`, `.env`).
3. `requirements.txt` or `pyproject.toml` lockfile is up to date.
4. Frontend builds cleanly (`npm run build`).
5. A `.env.example` exists documenting every required environment variable.
6. Report the results. Do not deploy automatically — Havilah runs the deploy command herself.
