# backend/routes/assistant.py

from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
import os
import numpy as np

from langchain.chains import RetrievalQA
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_huggingface import HuggingFaceEndpoint

router = APIRouter()

class Query(BaseModel):
    query: str

class TensorRequest(BaseModel):
    session_id: str

# ✅ Embedding model and text splitter
embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)

# ✅ In-memory vector store and retriever
VECTOR_DB_PATH = "./data/vector_store"
if not os.path.exists(VECTOR_DB_PATH):
    os.makedirs(VECTOR_DB_PATH)

vectorstore = None  # Will hold the FAISS store
retriever = None

# ✅ Load PDF and create vectorstore
def load_vector_store_from_pdf(file_path: str):
    loader = PyPDFLoader(file_path)
    docs = loader.load_and_split()
    split_docs = text_splitter.split_documents(docs)
    return FAISS.from_documents(split_docs, embedding)

# ✅ Ask from PDF
@router.post("/doc")
async def ask_from_doc(query: Query):
    global vectorstore, retriever
    if not vectorstore:
        return {"response": "Please upload a PDF first."}
    
    llm = HuggingFaceEndpoint(
        repo_id="google/flan-t5-base",
        task="text2text-generation",
        temperature=0.7
    )
    
    qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
    response = qa.run(query.query)
    return {"response": response}

# ✅ Upload and process PDF
@router.post("/upload_pdf")
async def upload_pdf(file: UploadFile = File(...)):
    global vectorstore, retriever

    file_path = f"./data/processed/{file.filename}"
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    vectorstore = load_vector_store_from_pdf(file_path)
    retriever = vectorstore.as_retriever()
    return {"message": f"Uploaded and processed {file.filename} successfully."}

# ✅ Tool-based simple QA
@router.post("/tool")
async def ask_tool(query: Query):
    tools_qa = {
        "lithography": "Lithography is a process used in semiconductor manufacturing.",
        "optimization": "Optimization in lithography involves improving print quality and yield."
    }
    for keyword, answer in tools_qa.items():
        if keyword in query.query.lower():
            return {"response": answer}
    return {"response": "Sorry, I don’t have an answer using tools right now."}

# ✅ Analyze tensor.txt from a session
@router.post("/analyze_tensor")
async def analyze_tensor(request: TensorRequest):
    session_id = request.session_id
    tensor_path = f"/ml/logs/{session_id}/tensor.txt"

    if not os.path.exists(tensor_path):
        raise HTTPException(status_code=404, detail=f"tensor.txt not found in {session_id}.")

    try:
        with open(tensor_path, "r") as f:
            lines = f.readlines()
            data = [float(x.strip()) for x in lines if x.strip()]
            tensor = np.array(data)

        result = {
            "shape": tensor.shape,
            "mean": float(np.mean(tensor)),
            "std": float(np.std(tensor)),
            "min": float(np.min(tensor)),
            "max": float(np.max(tensor)),
        }

        return {"session_id": session_id, "analysis": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading tensor.txt: {str(e)}")

# ✅ List available session folders under .ml/logs/
@router.get("/sessions")
async def list_sessions():
    logs_path = "./.ml/logs"
    try:
        sessions = [name for name in os.listdir(logs_path)
                    if os.path.isdir(os.path.join(logs_path, name))]
        return {"sessions": sessions}
    except Exception as e:
        return {"error": str(e)}
