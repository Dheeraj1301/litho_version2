# agents/assistant.py

import os
from dotenv import load_dotenv
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain_huggingface import HuggingFaceEndpoint

# Load Hugging Face token from .env
load_dotenv()
hf_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")
if not hf_token:
    raise ValueError("HUGGINGFACEHUB_API_TOKEN not found in .env file")

# Step 1: Load your document
loader = TextLoader('./data/processed/sample.txt', encoding='utf-8')
documents = loader.load()

# Step 2: Split text into chunks
text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
docs = text_splitter.split_documents(documents)

# Step 3: Create embeddings
embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Step 4: Create FAISS vector store
vectorstore = FAISS.from_documents(docs, embedding)

# Step 5: Initialize HuggingFaceEndpoint LLM
llm = HuggingFaceEndpoint(
    repo_id="google/flan-t5-base",
    task="text2text-generation",
    temperature=0.7,
    huggingfacehub_api_token=hf_token
)

# Step 6: Set up RetrievalQA chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vectorstore.as_retriever(),
    return_source_documents=True
)

# Step 7: Ask a question
query = "What is lithography optimization?"
result = qa_chain.invoke({"query": query})

# Step 8: Print the result
print("Answer:", result["result"])
print("Source Documents:")
for doc in result["source_documents"]:
    print(f"- {doc.metadata.get('source', 'N/A')}")
