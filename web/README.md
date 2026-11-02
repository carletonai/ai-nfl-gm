# web

The public deliverable is a trade calculator and draft board on carletonai.com, a React page
backed by the FastAPI service in `src/ai_nfl_gm/api/` (`make api`, then http://127.0.0.1:8000/docs).

**Where the page lives is the Product workstream's first decision.** The site's source is the
club's [`cais-website`](https://github.com/carletonai/cais-website) repository, so the
simplest route is a page there that calls this API. If a standalone client is preferable (own
build, own deploy), scaffold it in this folder:

```bash
# from the repo root; when Vite says web/ is not empty, choose "Ignore files and continue"
npm create vite@latest web -- --template react-ts
```

and add a `web` job to `.github/workflows/ci.yml`. Either way, keep the request and response
shapes in sync with `src/ai_nfl_gm/api/schemas.py`; the API's OpenAPI document at
`http://127.0.0.1:8000/openapi.json` can generate the TypeScript types. The API sends no CORS
headers yet, so a page on another origin cannot call it from the browser until
`CORSMiddleware` is added in `src/ai_nfl_gm/api/main.py`.

Week-4 milestone: a page that prices any two WR-and-pick packages against each other.
