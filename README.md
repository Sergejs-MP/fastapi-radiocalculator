# Radiocalc – README Collection

Below are **two self‑contained README files** you can copy into each sub‑project:

---

## backend/README.md

````markdown
# Radiocalc – FastAPI Backend

Small FastAPI service that computes radiobiological metrics (BED, EQD2, TCP/NTCP) and helper endpoints for gap compensation and OAR dose‑limits.

---
## Table of Contents
1. [Quick start](#quick-start)
2. [Project layout](#project-layout)
3. [Running in development](#running-in-development)
4. [Environment variables](#environment-variables)
5. [API reference](#api-reference)
6. [Tests](#tests)
7. [Deployment](#deployment)

---
### Quick start
```bash
# clone & create venv
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# run locally
uvicorn app.main:app --reload  # default http://localhost:8000
````

### Project layout

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI instance + CORS + routes
│   ├── models.py        # Pydantic request / response models
│   ├── calculations.py  # core LQ maths helpers
│   ├── routes.py        # /oar_max_dose, etc.
│   └── tests/           # pytest unit tests
├── requirements.txt
└── README.md            # you are here
```

### Running in development

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

- Docs: [http://localhost:8000/docs](http://localhost:8000/docs)
- Re‑loads on code changes.

### Environment variables

| Variable       | Purpose                              | Default        |
| -------------- | ------------------------------------ | -------------- |
| `LOG_LEVEL`    | uvicorn log level                    | `info`         |
| `CORS_ORIGINS` | comma‑separated list allowed by CORS | `*` (dev only) |

Put overrides in `.env`; [python‑dotenv] is already loaded.

### API reference (high‑level)

| Method | Path                | Req.Model                      | Resp.Model          | Notes                       |
| ------ | ------------------- | ------------------------------ | ------------------- | --------------------------- |
| POST   | `/calculate`        | `CalcRequest`                  | `CalcResponse`      | Basic BED/EQD₂/LQ           |
| POST   | `/gap_compensation` | `GapRequest`                   | `GapResponse`       | Dose loss + extra fracs     |
| POST   | `/calculate_dual`   | `CalcRequest` + `oar_ab` query | `DualCalcResponse`  | tumour + one OAR            |
| POST   | `/calculate_multi`  | `MultiCalcRequest`             | `MultiCalcResponse` | tumour + array of OARs      |
| POST   | `/oar_max_dose`     | `LimitRequest`                 | `LimitResponse`     | Max safe EQD₂ at given NTCP |

See full schemas in `/docs`.

### Tests

```bash
pytest -q
```

### Deployment

- **Render.com**: free web‑service gunicorn buildpack works out‑of‑box.
- **Docker** example:
  ```dockerfile
  FROM python:3.11-slim
  WORKDIR /app
  COPY . .
  RUN pip install -r requirements.txt
  CMD ["uvicorn","app.main:app","--host","0.0.0.0","--port","80"]
  ```

````

---
## radiocalc-ui/README.md

```markdown
# Radiocalc UI – Vite + React + MUI

Frontend SPA that talks to the FastAPI backend and visualises survival, TCP/NTCP curves, QUANTEC limits, and OAR risk.

---
## Table of Contents
1. [Quick start](#quick-start)
2. [Project layout](#project-layout)
3. [Running in development](#running-in-development)
4. [Environment variables](#environment-variables)
5. [Build & deploy](#build--deploy)

### Quick start
```bash
# inside radiocalc-ui/
npm install
npm run dev           # default http://localhost:5173
````

### Project layout

```
radiocalc-ui/
├── src/
│   ├── App.tsx              # main component
│   ├── components/
│   │   ├── TcpNtcpPlot.tsx
│   │   └── TcpNtcpPlotMulti.tsx
│   ├── data/                # JSON presets & limits
│   └── index.tsx
├── public/
├── vite.config.ts
├── package.json
└── README.md                # you are here
```

### Running in development

- Backend must be running on another port (e.g. 8000).
- Create `.env`:
  ```env
  VITE_API=http://localhost:8000
  ```
- `npm run dev` – opens hmr server; auto‑reloads on save.

### Environment variables

| Variable   | Purpose                     |
| ---------- | --------------------------- |
| `VITE_API` | Base URL of FastAPI backend |

### Build & Deploy

```bash
npm run build           # generates dist/
```

#### Netlify

- Point site to **radiocalc-ui/**, build command `npm run build`, publish `dist/`.
- Add environment var `VITE_API` in Netlify dashboard.

#### GitHub Pages (static)

```bash
npm install -g serve
serve -s dist
```

---

### Feature flags & folders

| Folder                         | Purpose                      |
| ------------------------------ | ---------------------------- |
| `src/data/tumour_presets.json` | default tumour α/β, D50, γ₅₀ |
| `src/data/oar_limits.json`     | QUANTEC limits table         |
| `src/components/*Plot*.tsx`    | Plotly renderers             |

---

### Development notes

- Uses **Material‑UI v5** – theme overrides in `src/theme.ts` (optional).
- Plot colours follow MUI primary (`#2196f3`) and error (`#dc3545`).
- State management is kept in `App.tsx`; no Redux.
- For analytics, call `posthog.capture()` after each successful calc (optional).

```

---
Copy each block into the respective folder (`backend/README.md`, `radiocalc-ui/README.md`) or leave this single collection file at project root if you prefer.

```
