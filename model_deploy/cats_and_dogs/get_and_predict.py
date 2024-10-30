from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from torchvision import models, transforms
from PIL import Image
import logging
import torch
import io

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Cats and Dogs Classifier")

# Load model
try:
    model_name = "resnet50"  # Using torchvision's ResNet-50
    logger.info(f"Loading model: {model_name}")
    model = models.resnet50(pretrained=True)
    model.eval()  # Set the model to evaluation mode
    logger.info("Model loaded successfully")
    
    # Define the classes we're interested in (cats and dogs from ImageNet)
    CAT_CLASSES = [281, 282, 283, 284, 285]  # ImageNet indices for cat breeds
    DOG_CLASSES = list(range(151, 269))  # ImageNet indices for dog breeds
    
    # Define the image transformations
    preprocess = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    
except Exception as e:
    logger.error(f"Error loading model: {str(e)}")
    raise

@app.get("/health")
async def health_check():
    return {"status": "healthy", "model": "loaded"}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        # Validate file type
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Read and process the image
        image_data = await file.read()
        image = Image.open(io.BytesIO(image_data)).convert('RGB')
        
        # Preprocess the image
        input_tensor = preprocess(image)
        input_batch = input_tensor.unsqueeze(0)  # Create a mini-batch as expected by the model
        
        # Make prediction
        with torch.no_grad():
            outputs = model(input_batch)
            predictions = torch.nn.functional.softmax(outputs[0], dim=0)
        
        # Get the predicted class
        predicted_class_idx = predictions.argmax().item()
        confidence = predictions[predicted_class_idx].item()
        
        # Determine if it's a cat or dog
        if predicted_class_idx in CAT_CLASSES:
            predicted_class = "cat"
        elif predicted_class_idx in DOG_CLASSES:
            predicted_class = "dog"
        else:
            predicted_class = "other"
        
        logger.info(f"Prediction made: {predicted_class} with confidence: {confidence}")
        
        return JSONResponse({
            "predicted_class": predicted_class,
            "confidence": float(confidence)
        })
    
    except Exception as e:
        logger.error(f"Error during prediction: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
