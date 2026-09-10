import joblib
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


app = FastAPI(title="API de Predicción de Precios de Ventas", description="API para predecir precios de viviendas según la superficie", version="1.0.0")

try:
    # Cargar el modelo entrenado
    model = joblib.load('Modelos_ML/RegresionLineal/models/linear_model.joblib')

except Exception:
    model = None
    
class housem2(BaseModel):
    area_m2: float = Field(..., example=82.5, description="Superficie de la vivienda en metros cuadrados")   
    
@app.get("/")
def health_check():
    return {"status": "OK", "message": "API de Predicción de Precios de Ventas está funcionando correctamente.", "model_loaded": model is not None}

@app.post("/predict")
def predict_price(data: housem2):
    if not model:
        raise HTTPException(status_code=500, detail="Modelo no cargado. Por favor, asegúrese de que el modelo esté disponible.")
    prediction = model.predict([[data.area_m2]])
    
    return {
        "area_m2": data.area_m2,
        "predicted_price": round(prediction, 2)
    }
        
     