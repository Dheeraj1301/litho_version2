from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import upload, inference, health
import os
from dotenv import load_dotenv

load_dotenv()

openai_key = os.getenv("OPENAI_API_KEY")
if openai_key:
    print("✅ OPENAI_API_KEY is set!")
else:
    print("❌ OPENAI_API_KEY is missing!")


app = FastAPI(title="Computational Lithography AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with allowed domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(upload.router, prefix="/upload", tags=["Upload"])
app.include_router(inference.router, prefix="/inference", tags=["Inference"])
app.include_router(health.router, prefix="/health", tags=["Health"])

@app.get("/")
def root():
    return {"message": "Welcome to Computational Lithography AI API"}
