from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import all routes
from .routes import health

# Optional imports for heavier routes. These may require third-party
# libraries that aren't always installed in lightweight test
# environments. Wrap them in a try/except block so the application can
# still start without them.
try:
    from .routes import upload, inference, autoencoder, assistant
except Exception:  # pragma: no cover - optional dependencies may be missing
    upload = inference = autoencoder = assistant = None

app = FastAPI(title="Computational Lithography AI")

# CORS settings (adjust as per frontend port/domain)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
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

# Root route
@app.get("/")
def root():
    return {"message": "Welcome to Computational Lithography AI API 🚀"}
