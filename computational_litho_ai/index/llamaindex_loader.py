from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, ServiceContext
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Securely load OpenAI API key
openai_api_key = os.getenv("OPENAI_API_KEY")

# Check if API key exists
if not openai_api_key:
    raise ValueError("Missing OpenAI API key. Please set OPENAI_API_KEY in your .env file.")

# Set up LLM and embedding
llm = OpenAI(api_key=openai_api_key)
embed_model = OpenAIEmbedding(api_key=openai_api_key)

# Service context for LlamaIndex
service_context = ServiceContext.from_defaults(llm=llm, embed_model=embed_model)

# Directory containing knowledge base (PDFs, docs, txt)
DATA_DIR = "./data/processed"

def build_index():
    documents = SimpleDirectoryReader(DATA_DIR).load_data()
    index = VectorStoreIndex.from_documents(documents, service_context=service_context)
    return index

def query_index(index, question):
    query_engine = index.as_query_engine()
    return query_engine.query(question)

if __name__ == "__main__":
    index = build_index()
    response = query_index(index, "What is lithography optimization?")
    print(f"🔍 Answer: {response}")
