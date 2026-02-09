import joblib
import numpy as np
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime

# --- CONFIGURING THE FLIGHT RECORDER (LOGGING) ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("api_usage.log"), # Saves to file
        logging.StreamHandler()               # Prints to terminal
    ]
)
logger = logging.getLogger(__name__)

app = FastAPI(title="EcoRoute Production API")

# Load Model Bundle
try:
    bundle = joblib.load("production_model.pkl")
    model = bundle["model"]
    scaler = bundle["scaler"]
    logger.info("✅ ML Model and Scaler loaded successfully.")
except Exception as e:
    logger.error(f"❌ CRITICAL ERROR: Model file not found or corrupted: {e}")
    model = None

class VehicleFeatures(BaseModel):
    cylinders: int
    displacement: float
    horsepower: float
    weight: float
    acceleration: float
    model_year: int
    origin: int

@app.get("/")
def health_check():
    return {"status": "online", "model_loaded": model is not None}

@app.post("/predict")
async def predict(data: VehicleFeatures):
    if not model:
        logger.error("Prediction attempt failed: Model not loaded.")
        raise HTTPException(status_code=503, detail="Model unavailable")

    logger.info(f"Inbound Request: {data.dict()}")
    
    try:
        # Convert to numpy and Scale
        input_data = np.array([[data.cylinders, data.displacement, data.horsepower, 
                                data.weight, data.acceleration, data.model_year, data.origin]])
        
        scaled_input = scaler.transform(input_data)
        prediction = float(model.predict(scaled_input)[0])
        
        logger.info(f"Successful Prediction: {prediction:.2f} MPG")
        
        return {
            "prediction": round(prediction, 2),
            "units": "miles_per_gallon",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Prediction logic failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Inference processing error")