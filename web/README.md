# web

The public deliverable is a trade calculator and draft board on carletonai.com, a React page
backed by the FastAPI service in `src/ai_nfl_gm/api/`.

**Where the page lives is the Product workstream's first decision.** The site's source is the
club's `cais-website` repository, so the simplest route is a page there that calls this API.
If a standalone client is preferable (own build, own deploy), scaffold it in this folder:

```bash
npm create vite@latest web -- --template react-ts
```

and add a `web` job to `.github/workflows/ci.yml`. Either way, keep the request and response
shapes in sync with `src/ai_nfl_gm/api/schemas.py`; the API's OpenAPI document at
`http://127.0.0.1:8000/openapi.json` can generate the TypeScript types.

Week-4 milestone: a page that prices any two WR-and-pick packages against each other.
