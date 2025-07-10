# Computational Lithography AI

This repository contains a prototype platform for running machine-learning experiments in computational lithography. It provides a FastAPI backend, a React frontend, and several small ML models used for demonstration purposes. Most third-party packages are stubbed to keep the project lightweight, so the code is primarily illustrative.

## Project layout

```
backend/                   Entrypoint for the FastAPI app
computational_litho_ai/    Main Python package with API routes, ML code and utilities
└── api/                   FastAPI routes and service logic
└── agents/                Example LangChain tools and QA scripts
└── frontend/              Vite/React interface
└── ml/                    Simple PyTorch and scikit‑learn models
└── utils/                 Data loaders and synthetic data generation
httpx/, multipart/, pandas/ Minimal stubs used for testing without real dependencies
```

## Features

- **API** – Endpoints for health checks, CSV inference, image classification, autoencoder reconstruction and a basic assistant for QA over PDFs.
- **ML models** – Includes training scripts and lightweight implementations of a gated CNN, autoencoder and yield predictor. Pretrained weights are stored under `ml/scripts/models`.
- **Frontend** – React components to upload data, run inferences, and interact with the assistant.
- **Utilities** – Helpers for generating synthetic data and normalizing values.
- **Tests** – Basic pytest suite covering API routes, utilities and model loading.

## Getting started

1. Install the required dependencies (FastAPI, PyTorch, scikit‑learn, etc.).
2. Launch the backend:
   ```bash
   uvicorn backend.main:app --reload
   ```
3. Start the frontend development server inside `computational_litho_ai/frontend`:
   ```bash
   npm install
   npm run dev
   ```
4. Run the tests (requires all optional dependencies):
   ```bash
   pytest
   ```

Because many packages are stubbed, the API can start in minimal environments. However, the ML features require PyTorch and other scientific libraries when executed for real.

## License

This project is released under the MIT License.
