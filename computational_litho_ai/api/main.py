from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import all routes
from api.routes import health, upload, inference, autoencoder, assistant

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
app.include_router(upload.router, prefix="/upload", tags=["Upload"])
app.include_router(inference.router, prefix="/inference", tags=["Inference"])
app.include_router(autoencoder.router, prefix="/autoencoder", tags=["AutoEncoder"])
app.include_router(assistant.router, prefix="/assistant", tags=["Assistant"])

# Root route
@app.get("/")
def root():
    return {"message": "Welcome to Computational Lithography AI API 🚀"}
