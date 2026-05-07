from importlib import import_module
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response

# Import all routes
from .routes import health

logger = logging.getLogger(__name__)


def optional_route(module_name: str):
    """Import an optional route module without disabling unrelated routes."""
    try:
        return import_module(f".routes.{module_name}", package=__package__)
    except Exception as exc:  # pragma: no cover - optional dependencies may be missing
        logger.warning("Skipping %s route: %s", module_name, exc)
        return None


upload = optional_route("upload")
inference = optional_route("inference")
autoencoder = optional_route("autoencoder")
assistant = optional_route("assistant")

app = FastAPI(title="Computational Lithography AI")

# CORS settings (adjust as per frontend port/domain)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Route registrations
app.include_router(health.router, prefix="/health", tags=["Health"])
if upload:
    app.include_router(upload.router, prefix="/upload", tags=["Upload"])
if inference:
    app.include_router(inference.router, prefix="/inference", tags=["Inference"])
if autoencoder:
    app.include_router(autoencoder.router, prefix="/autoencoder", tags=["AutoEncoder"])
if assistant:
    app.include_router(assistant.router, prefix="/assistant", tags=["Assistant"])


@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    return Response(status_code=204)


# Root route
@app.get("/")
def root():
    return {"message": "Welcome to Computational Lithography AI API 🚀"}
