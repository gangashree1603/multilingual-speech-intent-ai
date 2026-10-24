# AI Project Builder

Describe a project (text or PDF/DOCX/TXT) → an AI provider generates a full codebase → preview it, download a ZIP, or publish it to GitHub via OAuth.

**Stack:** React 18 + Vite (frontend) · FastAPI (backend) · GitHub REST/Git Data API.

## Setup
Requires Python 3.11+ and Node 18+.

```bash
# backend
cd backend
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env     # then fill it in (see below)
uvicorn main:app --reload --port 8000

# frontend (second terminal)
cd frontend
npm install
npm run dev              # http://localhost:5173 (proxies /api to :8000)
```
Open http://localhost:5173 (use this origin, not :8000, so session cookies work).

## Credentials you must provide
1. **AI**: `AI_API_KEY`, `AI_MODEL`, and `AI_PROVIDER` (`anthropic` or `openai`-compatible; optional `AI_BASE_URL`).
2. **GitHub OAuth App** (github.com → Settings → Developer settings → OAuth Apps): callback URL `http://localhost:5173/api/github/callback`; put the client id/secret in `.env`. Default scope is `repo` (needed for private repos); set `GITHUB_SCOPE=public_repo` for public-only.
3. `SESSION_SECRET`: a long random string.

## Test
```bash
cd backend && pytest        # path-traversal / secret-filter tests
```
Manual check: generate → download ZIP and inspect it → connect GitHub → publish to a new private repo → confirm the URL shows the commit.

## API
`POST /api/projects/analyze` · `POST /api/projects/generate` · `GET /api/projects/{id}/files` · `GET /api/projects/{id}/download` · `GET /api/github/login` · `GET /api/github/callback` · `GET /api/github/repositories` · `POST /api/github/publish` · plus `GET /api/session`, `POST /api/github/logout`.

## Security notes
- AI key, OAuth secret and GitHub tokens live only on the server; the browser holds a signed session cookie with a random id.
- OAuth `state` is validated; projects are bound to the session that created them.
- Generated paths are sanitized (no `..`, absolute paths, `.env*` except `.env.example`, key files, `node_modules`, build/cache dirs); files that look like they contain secrets are dropped; uploads limited to 5 MB.
- Publishing requires explicit confirmation, refuses to overwrite existing files unless allowed, never force-pushes, and reports success only after GitHub accepts the ref update.

## Known limitations
- Project/session state is in memory (lost on restart, single process). Use Redis/DB for production.
- Image uploads are rejected (no OCR configured); paste the text instead.
- Generation is one non-streaming AI call limited to ~16k output tokens, so very large projects may be truncated.
- Publishing to an empty (zero-commit) existing repo is not supported; initialize it with a README first.
- No per-user rate limiting; add it (e.g. slowapi) before exposing publicly.
