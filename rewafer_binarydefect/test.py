import argparse

import timm
import torch
from datasets import BASIC_TRANSFORMS
from opts import opts
from PIL import Image


def main(opt: argparse.Namespace, image: Image.Image) -> float:
    """
    Test the model and return the prediction.

    Args:
        opt (argparse.Namespace): Command-line options.
        image (Image.Image): Input image.

    Returns:
        logits (float): Prediction result (probability between 0 and 1).
    """
    source = BASIC_TRANSFORMS()(image)  # Apply basic transformations

    model = timm.create_model(
        opt.model_name, pretrained=False, num_classes=1
    )  # Create model
    model.load_state_dict(torch.load(opt.load_model_path))  # Load model weights
    model = model.to(opt.device)  # Move model to device

    model.eval()  # Set model to evaluation mode
    with torch.no_grad():  # Disable gradient computation
        # Add batch dimension and move to device
        source = source.unsqueeze(0).to(opt.device)
        logits = model(source).squeeze()  # Get model output
    print("logits:", logits)
    probability = torch.sigmoid(logits).item()  # Apply sigmoid to get probability
    return probability


if __name__ == "__main__":
    """
    Test mode must be enabled, and model weight and image paths must be specified.
    """
    opt = opts().parse(
        [
            "--test",
            "--model_name",
            "convnext_tiny.fb_in22k",
            "--load_model_path",
            "runs/.../best_model.pt",
            "--image_path",
            ".../xxx.png",
        ]
    )
    # Load image
    with open(opt.image_path, "rb") as f:
        image = Image.open(opt.image_path).convert("RGB")
    probability = main(opt, image)  # Make prediction
    print("probability:", probability)
