# Computational Lithography AI — Architecture

The repository contains a **React/Vite front end**, a **FastAPI back end** and several **local demonstration ML artifacts**. This is a prototype: components are built for research exploration rather than production fab operations.

## System diagram

```mermaid
flowchart TB
    U["Researcher"] --> R["React/Vite frontend"]
    R --> F["FastAPI application: api/main.py"]
    F --> Health["/health"]
    F --> Upload["/upload"]
    F --> Infer["/inference"]
    F --> Recon["/autoencoder"]
    F --> Assistant["/assistant"]
    Infer --> Yield["Saved yield-prediction model"]
    Infer --> Gated["Gated CNN / layout classification"]
    Infer --> AEmodel["Autoencoder reconstruction"]
    Recon --> AEmodel
    Recon --> Local[("ml/logs session outputs and ZIPs")]
    Assistant --> Doc[("data/raw + data/processed local docs")]
    Doc --> Search["Keyword-based document selection and snippets"]
    Search --> R
    Yield --> R
    Gated --> R
    AEmodel --> R
    Local --> R
```

## Example workflows

```mermaid
sequenceDiagram
    actor User
    participant Front as React
    participant API as FastAPI
    participant Model as Saved ML model
    participant Disk as Local artifacts
    User->>Front: Upload example CSV or image
    Front->>API: Request inference/reconstruction
    API->>Model: Preprocess input, run model
    Model-->>API: Predicted yield / class / reconstruction
    opt Autoencoder session
        API->>Disk: Write original, tensor, reconstructed image, ZIP
        Disk-->>API: Download URL
    end
    API-->>Front: JSON result or session URL
    Front-->>User: Display result
```

## Operational notes

- The backend mounts route modules **conditionally** via `optional_route`. When a module fails to import, unrelated routes remain available and logs record the omission.
- The startup working directory matters because inference loads checkpoints relative to `computational_litho_ai`.
- The local assistant uses document snippets and basic keyword scoring; support for PDF extraction depends on optional packages.
- `run_pipeline.py` is an example data/model demonstration, not a validated experimental benchmark. Reported performance requires independent held-out evaluation.
- The root contains lightweight compatibility stub directories, and many dependencies are unpinned; document the exact tested environment before external reproduction.

[Return to project README](../README.md).
