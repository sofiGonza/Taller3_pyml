# Taller 3 — Python y Machine Learning

Repositorio académico con ejemplos de carga y preparación de datos, modelos de machine learning y aplicaciones web para consultar predicciones y procesar imágenes.

Modelo_ML: link de predecir Enfermedad desplegado
https://taller3pyml-prucdkadnovapj4swm38nv.streamlit.app

Regresion Lineal desplegado
front: https://frontend-production-4471.up.railway.app
back: https://backend-production-b18e.up.railway.app

Py_img desplegado
https://pyimagenes.vercel.app


## Contenido

- [Descripción general](#descripción-general)
- [Aplicaciones](#aplicaciones)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Requisitos](#requisitos)
- [Instalación básica](#instalación-básica)
- [Cómo ejecutar cada aplicación](#cómo-ejecutar-cada-aplicación)
- [Flujo recomendado](#flujo-recomendado)
- [Tecnologías](#tecnologías)
- [Notas importantes](#notas-importantes)
- [Contribución](#contribución)
- [Licencia](#licencia)

## Descripción general

Este proyecto reúne ejercicios y aplicaciones prácticas desarrolladas con Python para explorar un flujo completo de trabajo de machine learning:

1. Cargar datos desde archivos, APIs y técnicas de web scraping.
2. Explorar y preparar datasets.
3. Entrenar modelos de regresión y clasificación.
4. Guardar modelos entrenados para reutilizarlos.
5. Exponer predicciones y resultados mediante interfaces web.
6. Aplicar visión artificial para detectar rostros en imágenes o video.

## Aplicaciones

### 1. `Carga-datos`

Incluye notebooks para practicar diferentes formas de obtener datos:

- `1.csv_carga_datos.ipynb`: lectura y exploración de datos en formato CSV.
- `2.excel_carga_datos.ipynb`: lectura de información desde archivos Excel.
- `3-api_carga_datos.ipynb`: consumo de datos desde una API.
- `4.webscraping_carga_datos.ipynb`: extracción de información desde páginas web.
- `dataset_ventas.csv` y `dataset_ventas.xlsx`: archivos de ejemplo para los ejercicios.

Esta carpeta es el punto de partida recomendado para entender la carga, revisión y preparación de los datos.

### 2. `Modelos_ML/RandomForest`

Aplicación de clasificación con Random Forest para estimar una posible enfermedad a partir de un dataset médico.

- `1.Crear_dataset.py`: crea o prepara el dataset médico ampliado.
- `2.Entrenar_modelo.py`: entrena el modelo y guarda el resultado.
- `3.Predecir_enfermedad.py`: carga el modelo guardado y realiza una predicción.
- `data/dataset_medico_ampliado.csv`: datos utilizados por el modelo.
- `models/modelo_random_forest_ampliado.pkl`: modelo entrenado serializado.

El modelo es demostrativo y no debe utilizarse para diagnósticos médicos reales.

### 3. `Modelos_ML/RegresionLineal`

Sistema de regresión lineal para estimar el precio de una vivienda a partir de su área en metros cuadrados.

- `back/`: backend auxiliar con scripts de entrenamiento y predicción.
- `back/train.py`: entrenamiento del modelo.
- `back/main.py`: servicio de predicción.
- `back/models/linear_model.joblib`: modelo entrenado.
- `front/`: aplicación web Django que recibe el área y muestra el precio estimado.
- `front/app_predicc/`: aplicación Django encargada del formulario y la respuesta.

La estimación es educativa y depende de los datos con los que se entrenó el modelo.

### 4. `Modelos_ML/py_img-main`

Aplicación web de visión artificial para detectar rostros usando OpenCV.

Permite:

- subir una imagen mediante selector o drag and drop;
- utilizar la cámara web en tiempo real;
- cambiar entre cámara frontal y trasera cuando el dispositivo lo permite;
- visualizar la imagen original y el resultado anotado;
- consultar la cantidad de rostros detectados.

El backend está construido con Flask y expone `POST /api/detect`. El clasificador Haar de OpenCV dibuja recuadros sobre los rostros encontrados.



## Estructura del proyecto

```text
.
├── Carga-datos/
│   ├── 1.csv_carga_datos.ipynb
│   ├── 2.excel_carga_datos.ipynb
│   ├── 3-api_carga_datos.ipynb
│   ├── 4.webscraping_carga_datos.ipynb
│   └── datasets de ejemplo
├── Modelos_ML/
│   ├── RandomForest/
│   ├── RegresionLineal/
│   └── py_img-main/
│       └── py_img-main/
├── README.md
└── venv/                  # entorno local
```

## Requisitos

- Python 3.10 o superior recomendado.
- `pip`.
- Jupyter Notebook o JupyterLab para ejecutar los notebooks.
- Navegador moderno para las aplicaciones web.
- Permiso de cámara para el modo webcam de `py_img-main`.

Cada aplicación puede tener dependencias específicas en su propio `requirements.txt`. Se recomienda instalar las dependencias dentro de un entorno virtual.

## Instalación básica

Desde la raíz del proyecto:

```bash
python -m venv venv
```

Activación en Windows:

```bash
venv\Scripts\activate
```

Activación en macOS o Linux:

```bash
source venv/bin/activate
```

Después, instala las dependencias de la aplicación que quieras ejecutar. Por ejemplo, para visión artificial:

```bash
cd Modelos_ML/py_img-main/py_img-main
pip install -r requirements.txt
```

## Cómo ejecutar cada aplicación

### Notebooks de carga de datos

```bash
jupyter notebook
```

Abre uno de los notebooks dentro de `Carga-datos/` y ejecuta sus celdas en orden.

### Random Forest

Desde `Modelos_ML/RandomForest/`:

```bash
pip install -r requirements.txt
python 1.Crear_dataset.py
python 2.Entrenar_modelo.py
python 3.Predecir_enfermedad.py
```

Los nombres exactos de entradas pueden variar según la implementación y los datos disponibles; revisa los comentarios de cada script antes de ejecutarlo.

### Regresión lineal

Frontend Django, desde `Modelos_ML/RegresionLineal/front/`:

```bash
pip install -r requirements.txt
python manage.py check
python manage.py runserver
```

Luego visita `http://127.0.0.1:8000/`.

El backend auxiliar ubicado en `back/` tiene sus propias dependencias y puede ejecutarse según las instrucciones de sus scripts o su `Dockerfile`.

### `py_img-main`

Desde `Modelos_ML/py_img-main/py_img-main/`:

```bash
pip install -r requirements.txt
python api/index.py
```

Abre `http://127.0.0.1:5000/`. Para usar la webcam, acepta el permiso solicitado por el navegador.

#### API de detección

`POST /api/detect`

- Campo multipart requerido: `image`.
- Respuesta exitosa: JSON con `success`, `faces_detected` e `image` en formato Data URL.
- Error `400`: falta la imagen o el formato no es válido.
- Error `500`: ocurrió un problema durante el procesamiento del servidor.

## Flujo recomendado

1. Explorar y preparar los datos en `Carga-datos/`.
2. Entrenar el modelo elegido.
3. Verificar que el archivo del modelo se genere en la carpeta `models/` correspondiente.
4. Ejecutar el script de predicción o la aplicación web.
5. Probar con datos de ejemplo antes de interpretar resultados.

## Tecnologías

- Python
- Jupyter Notebook
- pandas y NumPy
- scikit-learn
- Flask
- Django
- OpenCV
- HTML, CSS, JavaScript y Bootstrap
- Vercel para la configuración de despliegue de `py_img-main`

## Notas importantes

- `venv/` es un entorno virtual local y no debería incluirse en commits.
- Los archivos `.pkl` y `.joblib` contienen modelos ya entrenados; si se cambia el dataset o el código de entrenamiento, conviene regenerarlos.
- La detección facial y las predicciones son demostraciones académicas, no herramientas médicas ni sistemas de identificación.
- La cámara solo funciona en contextos permitidos por el navegador, normalmente `localhost` o una conexión HTTPS.
- Revisa los `requirements.txt` de cada aplicación para evitar mezclar dependencias innecesariamente.

## Contribución

1. Crea una rama para tu cambio.
2. Describe qué problema resuelve.
3. Mantén separadas las mejoras de código, documentación y diseño cuando sea posible.
4. Ejecuta las comprobaciones locales antes de proponer el cambio.
5. Incluye instrucciones de ejecución si agregas una nueva aplicación.

## Licencia

Este repositorio no declara actualmente una licencia formal en su raíz. Antes de distribuirlo, añade un archivo `LICENSE` con la licencia elegida y actualiza esta sección.
