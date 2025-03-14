import os
from pathlib import Path
from transformers import CLIPProcessor, CLIPModel

def download_or_load_clip_model():
    """
    Load the CLIP model and processor from local storage or download if not available.
    
    Args:
        model_name: The name of the CLIP model to use for generating embeddings.
                   If None, uses the MODEL_NAME from environment variables.
        
    Returns:
        A tuple of (model, processor)
    """
    # Get model name from environment variable
    model_name = os.getenv("MODEL_NAME", "openai/clip-vit-base-patch32")
    
    # Create models directory if it doesn't exist
    models_dir = os.getenv("MODELS_DIR", "models")
    model_path = Path(models_dir) / model_name.split("/")[-1]
    os.makedirs(model_path, exist_ok=True)
    
    # Check if model already exists locally
    model_exists = (model_path / "model.safetensors").exists()
    
    if model_exists:
        print(f"Loading model from local path: {model_path}")
        model = CLIPModel.from_pretrained(str(model_path))
        processor = CLIPProcessor.from_pretrained(str(model_path))
    else:
        print(f"Model not found locally. Downloading from Hugging Face: {model_name}")
        model = CLIPModel.from_pretrained(model_name)
        processor = CLIPProcessor.from_pretrained(model_name)
        
        # Save model and processor to disk for future use
        print(f"Saving model to disk: {model_path}")
        model.save_pretrained(model_path)
        processor.save_pretrained(model_path)
        print(f"Model saved to: {model_path}")
    
    return model, processor 