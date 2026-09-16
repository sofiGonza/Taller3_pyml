import joblib
from pathlib import Path
import numpy as np
from sklearn.linear_model import LinearRegression

# Predecir precios de viviendas según la superficie en M2

# Datos de entrenamiento (x) y etiquetas (y)
x = np.array([[40], [50], [60], [85], [100], [150]])

y = np.array([
    100000000,
    120000000,
    150000000,
    200000000,
    250000000,
    300000000
])

# Entrenar el modelo de regresión lineal
model = LinearRegression()
model.fit(x, y)

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "models/linear_model.joblib"

# Guardar el modelo entrenado
joblib.dump(model, MODEL_PATH)