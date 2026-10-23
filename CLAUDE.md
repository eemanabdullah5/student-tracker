# CLAUDE.md: Student Assignment & Progress Tracker

Context for Claude Code sessions. **Read this first, and update the "Progress" and "Next step" sections after every completed step.**

## How the user wants to work (important)

- **Very small steps.** One step per turn. Never write large chunks of code or several features at once.
- **Explain before adding.** Before writing lines, explain what is being added and why. After writing, walk through it line by line (a table works well).
- **Options before decisions.** For every design or tooling choice, present 2–4 options with trade-offs and a recommendation, then **wait for the user to choose**.
- **Plain language.** If the user says they don't understand, re-explain simply, with a small concrete code example and an analogy.
- Verify each step (run it or test it), then make one small commit.
- The user is on a **Windows work laptop** using PowerShell in VS Code.
  - The **GitHub CLI (`gh`) is blocked.** Never suggest it. Claude commits locally; **the user runs `git push`** and opens and merges PRs on the GitHub website. Claude supplies a ready-to-paste PR title and description.
  - VS Code's interpreter is not pointed at the venv, so it shows "package not installed" hints. That's harmless; ignore it.

## The brief (condensed)

Full-stack app: **React.js + FastAPI + SQLite**. Teachers manage assignments and grades; students submit work and track progress.

1. **React:** login, student dashboard, teacher dashboard. Teachers create assignments, review submissions, grade. Students browse assignments, submit, view their own results. React Router, reusable components, hooks, a shared API client. Form validation, loading indicators, empty states, clear errors. Routes protected by login and role (the backend still enforces everything). Handle expired sessions and logout. Progress shown with summary cards and a simple chart.
2. **Auth/security:** JWT login with expiry, hashed passwords, signing secret from env. Student and teacher roles; **public registration never grants teacher**. Students can't see other students' submissions or grades. CORS for React. Document how tokens are stored.
3. **Database/backend:** normalized tables for users, courses, enrollments, assignments, submissions. PKs, FKs, uniqueness, validation constraints. APIs for enrollment, assignments, submissions, grading, progress. Routes, schemas, logic and database access kept separate. Classes, exception handling, logging. **Never log passwords or tokens.**
4. **DSA:** course topics as a **tree** (displayed in React). Topic prerequisites as a **directed graph** (retrieve prerequisites, reject cycles). **Stack-based undo** of a teacher's latest grade change, with an Undo button. Explain time and space complexity, and whether undo history survives a restart.
5. **Maths/SQL:** weighted score from score and weight vectors; average, min, max and **population variance** of grades; historical pass proportion of graded submissions. SQL joins and aggregation for submission counts, missing submissions and student progress. Define how ungraded work and empty results are handled. Show these in the dashboards.
6. **Testing/Git:** backend tests (auth, permissions, data isolation, validation, algorithms, calculations); frontend tests (login errors, form validation, role views, loading and error states); a full teacher-to-student workflow test. Feature branches, meaningful commits, PRs.

**Deliverables:** repo with separate `frontend/` and `backend/`; README (setup, demo accounts, example env vars without real secrets); database relationship diagram and design explanation; automated tests and their results; a working demo.

## Repo and environment

- GitHub: https://github.com/eemanabdullah5/student-tracker (`origin`, default branch `main`)
- Commit style: Conventional Commits (`feat:`, `fix:`, `refactor:`, `chore:`, `test:`, `docs:`)
- Tools: Python 3.14, Node 24, npm 11, Git 2.56
- Backend venv: `backend\.venv`. Activate with `cd backend; .\.venv\Scripts\Activate.ps1`. On a new laptop, run `python -m venv .venv` then `pip install -r requirements.txt`.
- `backend/.env` holds the real `JWT_SECRET` and is git-ignored. On a new laptop, copy `.env.example` to `.env` and generate a secret with `python -c "import secrets; print(secrets.token_urlsafe(48))"`.
- Run the server from inside `backend\`: `uvicorn app.main:app --reload` (`.env` is read from the current folder)

## Decisions made (do not reopen unless the user asks)

| Area | Decision |
|---|---|
| Python environment | `venv` + `pip` + `requirements.txt`, **exact pins for direct dependencies only**, each with a comment |
| Packages | `fastapi`, `uvicorn[standard]` (not `fastapi[standard]`); add each package in the step that needs it |
| Backend layout | **By layer:** `app/routes/`, `app/schemas/`, `app/services/`, `app/repositories/`, `app/models/`, `app/core/`, `app/db/`. Create folders only when the first file goes in. `main.py` only builds the app (logging, routers, later CORS) |
| Settings | `pydantic-settings` in `app/core/config.py`. `JWT_SECRET` required, min 32 chars, `hide_input_in_errors=True`. HS256. 60-minute token expiry (access token only, no refresh tokens) |
| Logging | Built-in `logging`, `app/core/logging.py`, with a `RedactingFormatter` that masks Bearer tokens, JWTs, and password/token/secret values (including tracebacks) |
| Roles | `role` column on `users` (student or teacher) |
| Course ownership | `courses.teacher_id`: one teacher per course |
| Submissions | One per student per assignment (`UNIQUE(assignment_id, student_id)`); resubmitting replaces it **until graded** |
| Grades | Columns on `submissions`: `score` (NULL = ungraded), `feedback`, `graded_at`, `graded_by` |
| Database access | **SQLAlchemy 2.x ORM, sync** (not async, not SQLModel). Reports may use explicit joins/aggregation, or `text()` SQL |
| Migrations | `Base.metadata.create_all()`; reset the dev database via the seed script. Mention Alembic in the README only |

### Planned database schema (topics and prerequisites come in Phase 3)

- **users:** id PK, email UNIQUE, password_hash, full_name, role, created_at
- **courses:** id PK, title, teacher_id FK→users
- **enrollments:** id PK, student_id FK→users, course_id FK→courses, enrolled_at, UNIQUE(student_id, course_id)
- **assignments:** id PK, course_id FK→courses, title, description, due_at, max_score CHECK > 0, weight CHECK > 0
- **submissions:** id PK, assignment_id FK, student_id FK→users, content, submitted_at, score NULL, feedback, graded_at, graded_by FK→users, UNIQUE(assignment_id, student_id)
- `0 <= score <= max_score` is checked in the service layer (SQLite can't compare against another table's column in a CHECK)
- Foreign keys are switched on for every connection (`PRAGMA foreign_keys = ON`)

## Roadmap

- **Phase 0, foundations:** ✅ done (PR #1 merged)
- **Phase 1 (Milestone 1):** 1.1 DB design ✅ · 1.2 SQLAlchemy setup and models ⏳ · 1.3 password hashing · 1.4 registration (always student) · 1.5 JWT login · 1.6 current-user and role dependencies · 1.7 CORS · 1.8 seed script with demo accounts · 1.9 React app setup · 1.10 shared API client (401 handling) · 1.11 auth context, token storage, logout · 1.12 router, protected routes, dashboard shells · 1.13 first auth tests (backend and frontend)
- **Phase 2 (Milestone 2):** courses and enrollment · assignments · submissions (own only) · grading · React pages with validation, loading, empty and error states · data-isolation tests
- **Phase 3 (Milestone 3):** topic tree · prerequisite graph with cycle rejection · stack-based grade undo (decide in-memory vs persisted) · weighted score · stats (mean, min, max, population variance, pass rate) · SQL reports · rules for ungraded work and empty data · dashboard cards and chart · complexity write-up
- **Phase 4 (Milestone 4):** remaining backend and frontend tests · full teacher-to-student workflow test · README, ER diagram and design notes · final demo

## Progress (what exists now)

```
.gitignore                 .venv, node_modules, .env (except .env.example), *.db, caches
CLAUDE.md                  this file
backend/
  requirements.txt         fastapi==0.159.1, uvicorn[standard]==0.54.0,
                           pydantic-settings==2.16.1, sqlalchemy==2.1.6
  .env.example             blank JWT_SECRET + defaults
  app/main.py              setup_logging(), FastAPI app, include health router
  app/routes/health.py     GET /health -> {"status": "ok"}
  app/core/config.py       Settings + `settings` singleton
  app/core/logging.py      redact(), RedactingFormatter, setup_logging()
  app/db/database.py       engine, foreign-key PRAGMA hook, SessionLocal, Base, get_db()
  app/models/__init__.py   imports every model (so create_all sees all tables)
  app/models/user.py       Role(StrEnum student/teacher) + User model
  app/models/course.py     Course: title, teacher_id FK ON DELETE RESTRICT, UNIQUE(teacher_id, title)
```

Current branch: **`feature/database-models`** (not yet pushed or merged).

User model decisions: `Role` is a `StrEnum` mapped with SQLAlchemy `Enum(..., values_callable, create_constraint=True, validate_strings=True)`, which generates `CHECK (role IN ('student','teacher'))` and defaults to STUDENT. Email is lowercased in the **service layer** (Step 1.4, not done yet), with `UNIQUE` on the column. Verified in an in-memory DB: duplicate email and `role='admin'` are both rejected by SQLite.

## Next step (waiting for the user)

Course decisions: `ON DELETE RESTRICT` (never cascade-delete grades) and `UNIQUE(teacher_id, title)`. The FK can't check that the owner is a teacher; the service layer must (Phase 2). No `relationship()`s added yet; add them when a query needs them.

**Step 1.2e, the `Enrollment` model** (`app/models/enrollment.py`): id, student_id FK, course_id FK, enrolled_at, UNIQUE(student_id, course_id). Open decisions to present first: the ON DELETE behaviour of each FK, and whether to keep a surrogate `id` or use the composite primary key (student_id, course_id).

After that: the Assignment and Submission models (one per step), `create_all` at startup, then a PR for `feature/database-models`.
