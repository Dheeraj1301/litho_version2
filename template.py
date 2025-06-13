import os

project_structure = {
    "api/routes": [],
    "api/services": [],
    "api/models": [],
    "api": ["main.py"],
    
    "frontend/public": [],
    "frontend/src/components": [],
    "frontend/src/pages": [],
    "frontend/src": ["App.jsx"],
    "frontend": ["tailwind.config.js"],
    
    "ml/autoencoder": [],
    "ml/gated_cnn": [],
    "ml/yield_prediction": [],
    "ml/qml_optimizer": [],
    
    "agents/tools": [],
    "agents": ["assistant.py"],
    
    "index": ["llamaindex_loader.py"],
    
    "data/raw": [],
    "data/processed": [],
    
    "tests/api": [],
    "tests/ml": [],
    "tests/utils": [],
    
    "configs": ["model_config.yaml"],
    
    "docker": [
        "backend.Dockerfile", 
        "frontend.Dockerfile", 
        "docker-compose.yml"
    ],
    
    "": [
        ".env",
        "requirements.txt",
        "README.md",
        "run_pipeline.py"
    ]
}

def create_project_structure(base_path="computational_litho_ai"):
    print(f"\n🚧 Creating project structure under: `{base_path}/`\n")
    
    for folder, files in project_structure.items():
        dir_path = os.path.join(base_path, folder)
        os.makedirs(dir_path, exist_ok=True)
        for file in files:
            file_path = os.path.join(dir_path, file)
            with open(file_path, "w") as f:
                pass
            print(f"📄 Created: {file_path}")
    
    print("\n✅ Project structure successfully initialized.")

if __name__ == "__main__":
    create_project_structure()
