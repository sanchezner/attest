from fastapi import FastAPI
from api.routes import observations, contracts, status, dashboard

app = FastAPI(title='attest', version='0.1.0')
app.include_router(observations.router)
app.include_router(contracts.router)
app.include_router(status.router)
app.include_router(dashboard.router)


@app.get('/health')
def health():
    return {'status': 'ok'}