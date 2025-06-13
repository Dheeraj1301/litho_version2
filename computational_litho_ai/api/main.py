from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import upload, inference, health
import os
from dotenv import load_dotenv

# ✅ Load environment variables
load_dotenv()

openai_key = os.getenv("OPENAI_API_KEY")
if openai_key:
    print("✅ OPENAI_API_KEY is set!")
else:
    print("❌ OPENAI_API_KEY is missing!")

# ✅ Initialize FastAPI app
app = FastAPI(title="Computational Lithography AI")

# ✅ Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # More secure than "*"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Include routers
app.include_router(upload.router, prefix="/upload", tags=["Upload"])
app.include_router(inference.router, prefix="/inference", tags=["Inference"])
app.include_router(health.router, prefix="/health", tags=["Health"])

# ✅ Root route
@app.get("/")
def root():
    return {"message": "Welcome to Computational Lithography AI API"}
