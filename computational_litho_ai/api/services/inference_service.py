import random
import os
from ml.gated_cnn.gated_cnn_model import GatedCNN, predict_layout_class
from ml.qml_optimizer.qml_trainer import optimize_parameters
import torch

def run_inference(mask_id: str, model: str = "gated_cnn"):
    # Dummy input — replace with real layout tensor from mask_id
    dummy_input = torch.rand(1, 1, 64, 64)

    if model == "gated_cnn":
        model_instance = GatedCNN()
        pred = predict_layout_class(model_instance, dummy_input)
        return {"mask_id": mask_id, "layout_class": pred}

    elif model == "qml_opt":
        opt_params = optimize_parameters()
        return {"mask_id": mask_id, "optimized_qml_params": opt_params.tolist()}

    return {"mask_id": mask_id, "status": "model not found"}

