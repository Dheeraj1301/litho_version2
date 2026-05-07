# backend/routes/assistant.py

import csv
import logging
import os
from pathlib import Path

import numpy as np
from fastapi import APIRouter, File, HTTPException, UploadFile
from pydantic import BaseModel

router = APIRouter()

# Basic file logger for assistant interactions
logger = logging.getLogger(__name__)
if not logger.handlers:
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler("assistant.log")
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)


class Query(BaseModel):
    query: str


class TensorRequest(BaseModel):
    session_id: str


DATA_DIRECTORIES = [Path("data/raw"), Path("data/processed")]
SUPPORTED_TEXT_SUFFIXES = {".txt", ".csv", ".md", ".json", ".yaml", ".yml"}
knowledge_cache = []


def read_text_file(path: Path) -> str:
    if path.suffix.lower() == ".csv":
        with path.open(newline="", encoding="utf-8", errors="ignore") as csv_file:
            reader = csv.reader(csv_file)
            rows = [", ".join(row) for _, row in zip(range(25), reader)]
        return "\n".join(rows)

    return path.read_text(encoding="utf-8", errors="ignore")[:8000]


def extract_pdf_text(path: Path) -> str:
    """Best-effort PDF extraction without requiring LangChain at import time."""
    try:
        from langchain_community.document_loaders import PyPDFLoader

        loader = PyPDFLoader(str(path))
        pages = loader.load_and_split()
        return "\n".join(page.page_content for page in pages)[:12000]
    except Exception as exc:  # pragma: no cover - depends on optional PDF stack
        logger.warning("PDF text extraction failed for %s: %s", path, exc)
        return f"PDF uploaded: {path.name}. Text extraction is unavailable in this environment."


def load_document(path: Path):
    suffix = path.suffix.lower()
    if suffix in SUPPORTED_TEXT_SUFFIXES:
        content = read_text_file(path)
    elif suffix == ".pdf":
        content = extract_pdf_text(path)
    else:
        return None

    return {"source": path.name, "path": str(path), "content": content}


def refresh_knowledge_cache():
    global knowledge_cache
    documents = []
    for directory in DATA_DIRECTORIES:
        if not directory.exists():
            continue
        for path in sorted(directory.iterdir()):
            if path.is_file():
                document = load_document(path)
                if document and document["content"].strip():
                    documents.append(document)
    knowledge_cache = documents
    return documents


def score_document(query: str, document: dict) -> int:
    words = [word for word in query.lower().split() if len(word) > 2]
    content = document["content"].lower()
    return sum(content.count(word) for word in words)


def answer_from_documents(query: str) -> str:
    documents = refresh_knowledge_cache()
    if not documents:
        return "No uploaded or sample data is available yet. Upload a PDF or add CSV/TXT data first."

    ranked = sorted(
        documents,
        key=lambda document: score_document(query, document),
        reverse=True,
    )
    best = ranked[0]
    content = best["content"].strip()
    lines = [line.strip() for line in content.splitlines() if line.strip()]
    query_words = [word for word in query.lower().split() if len(word) > 2]
    matching_lines = [
        line for line in lines if any(word in line.lower() for word in query_words)
    ]
    selected_lines = matching_lines[:4] or lines[:4]
    snippet = " ".join(selected_lines)[:900]
    return f"Based on {best['source']}: {snippet}"


@router.post("/doc")
async def ask_from_doc(query: Query):
    response = answer_from_documents(query.query)
    logger.info("DOC_QUERY: %s | RESPONSE: %s", query.query, response)
    return {"response": response}


@router.post("/upload_pdf")
async def upload_pdf(file: UploadFile = File(...)):
    processed_dir = Path("data/processed")
    processed_dir.mkdir(parents=True, exist_ok=True)
    file_path = processed_dir / file.filename

    with file_path.open("wb") as buffer:
        buffer.write(await file.read())

    refresh_knowledge_cache()
    logger.info("PDF_UPLOADED: %s", file.filename)
    return {"message": f"Uploaded {file.filename} and added it to the assistant knowledge base."}


@router.post("/tool")
async def ask_tool(query: Query):
    normalized_query = query.query.lower()
    tools_qa = {
        "lithography": "Lithography is a semiconductor manufacturing process that transfers circuit patterns onto a wafer.",
        "optimization": "Lithography optimization improves print quality, process windows, and predicted yield.",
        "yield": "Yield prediction estimates how many manufactured patterns or wafers are expected to pass quality targets.",
        "autoencoder": "The autoencoder reconstructs image inputs and stores tensor sessions that can be analyzed later.",
        "csv": "Use the CSV inference section to upload process data and receive predicted yield values.",
    }
    for keyword, answer in tools_qa.items():
        if keyword in normalized_query:
            logger.info("TOOL_QUERY: %s | RESPONSE: %s", query.query, answer)
            return {"response": answer}

    response = answer_from_documents(query.query)
    logger.info("TOOL_QUERY: %s | RESPONSE: %s", query.query, response)
    return {"response": response}


@router.post("/analyze_tensor")
async def analyze_tensor(request: TensorRequest):
    session_id = request.session_id
    tensor_path = os.path.join("ml", "logs", session_id, "tensor.txt")

    if not os.path.exists(tensor_path):
        raise HTTPException(status_code=404, detail=f"tensor.txt not found in {session_id}.")

    try:
        with open(tensor_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            values = []
            for line in lines:
                values.extend([float(v) for v in line.split() if v])
            tensor = np.array(values)

        result = {
            "shape": tensor.shape,
            "mean": float(np.mean(tensor)),
            "std": float(np.std(tensor)),
            "min": float(np.min(tensor)),
            "max": float(np.max(tensor)),
        }

        logger.info("TENSOR_ANALYSIS: %s | shape=%s", session_id, result["shape"])
        return {"session_id": session_id, "analysis": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading tensor.txt: {str(e)}")


@router.get("/sessions")
async def list_sessions():
    logs_path = os.path.join("ml", "logs")
    try:
        sessions = [
            name
            for name in os.listdir(logs_path)
            if os.path.isdir(os.path.join(logs_path, name))
        ]
        return {"sessions": sessions}
    except Exception as e:
        return {"error": str(e), "sessions": []}
