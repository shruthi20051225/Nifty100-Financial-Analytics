import time

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from src.api.routers import (
    health,
    companies,
    screener,
    sectors,
    peers,
    valuation,
    portfolio,
    documents,
)

app = FastAPI(
    title="Nifty100 Financial Analytics API",
    version="1.0.0",
    description="REST API for Nifty100 Financial Analytics Platform",
)

# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# Request Logging Middleware
# ============================================================


@app.middleware("http")
async def log_requests(request: Request, call_next):

    start = time.time()

    response = await call_next(request)

    duration = round(time.time() - start, 4)

    print(f"{request.method} | {request.url.path} | {duration} sec")

    return response


# ============================================================
# Routers
# ============================================================

app.include_router(health.router, prefix="/api/v1", tags=["Health"])

app.include_router(companies.router, prefix="/api/v1", tags=["Companies"])

app.include_router(screener.router, prefix="/api/v1", tags=["Screener"])

app.include_router(sectors.router, prefix="/api/v1", tags=["Sectors"])

app.include_router(peers.router, prefix="/api/v1", tags=["Peers"])

app.include_router(valuation.router, prefix="/api/v1", tags=["Valuation"])

app.include_router(portfolio.router, prefix="/api/v1", tags=["Portfolio"])

app.include_router(documents.router, prefix="/api/v1", tags=["Documents"])

# ============================================================
# Root Endpoint
# ============================================================


@app.get("/")
def root():

    return {"message": "Nifty100 Financial Analytics API", "version": "1.0.0"}
