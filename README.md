# attest

Know whether your pipeline outputs are healthy. Workers report what they produced; attset tracks each artifact as ok, violated, or missing.

## Architecture

1. Workers call `watch.report()` → observations table
2. Dashboard / SDK `verify()` → live evaluation
3. `cli.evaluate` cron → persists evaluations, ntfy on status transitions

## Setup

### API
#### 1. Configure environment variables

```
cp .env.example .env
# Edit .env with your credentials
```

#### 2. Install dependencies

```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

#### 3. Start API

```
python -m db.init_db
uvicorn api.main:app --reload
```

### Dashboard

```
cd frontend
cp .env.example .env.local
npm install
npm run dev
```

### Evaluator (cron)

```
python -m cli.evaluate
```

## Quickstart

Assume the project slug `demo`.

### 1. Register a contract

```
curl -X POST http://localhost:8000/api/v1/projects/demo/contracts \
    -H 'Content-Type: application/json' \
    -d '{"artifact_id":"bronze/artifact_1","min_row_count":1,"max_age_hours":26,"expected_reporter":"bronze-worker"}'
```

### 2. Create a reporter token

```
python -m cli.create_tokens --project demo --reporter bronze-worker
# paste printed token into .env as DEMO_BRONZE_TOKEN=...
```

### 3. Report an observation (or use SDK)

#### Option A: curl (no SDK; good for testing)

```
curl -X POST http://localhost:8000/api/v1/projects/demo/observations \
    -H "Authorization": Bearer $DEMO_BRONZE_TOKEN" \
    -H "Content-Type: application/json" \
    -d '{
        "artifact_id": "bronze/artifact_1",
        "reporter": "bronze-worker",
        "observed_at": "2026-06-25T12:00:00+00:00",
        "row_count": 42
    }'
```

`reporter` must match the token's reporter and `expected_reporter` on the contract.

#### Option B: SDK (what workers actually use)

```
cp attest.yaml.example attest.yaml
# make sure DEMO_BRONZE_TOKEN is in .env
```

From repo root with venv active, run:

```
python -c '
from sdk.watch import Watch
watch = Watch.from_config("attest.yaml")
watch.report("bronze/artifact_1", row_count=42)
'
```

### 4. Open dashboard

```
cd frontend
cp .env.example .env.local # VITE_PROJECT_SLUG=demo
npm run dev
# http://localhost:5173 - artifact should show ok
```

## NOTE: Security

v0 is built for local/trusted network use:

- Contract registration and dashboard reads are **unauthenticated** (as it stands)
- Observations and SDK `/status` require Bearer tokens

Do **NOT** expose this API to the public without hardening writes at the very least