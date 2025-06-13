from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import health, upload, inference  # ✅ Must import these

app = FastAPI(title="Computational Lithography AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # ✅ restrict to frontend dev origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Include routers
app.include_router(health.router, prefix="/health", tags=["Health"])
app.include_router(upload.router, prefix="/upload", tags=["Upload"])
app.include_router(inference.router, prefix="/inference", tags=["Inference"])

@app.get("/")
def root():
    return {"message": "Welcome to Computational Lithography AI API"}
