import re

import requests
from django.conf import settings
from django.shortcuts import render


_DECIMAL_RE = re.compile(r'^\d+(?:[.,]\d+)?$')


def parse_area(value):
    """Convert a Spanish/English decimal input to a positive float."""
    normalized = value.strip().replace(' ', '').replace(',', '.')
    if not normalized or not _DECIMAL_RE.fullmatch(normalized):
        raise ValueError

    area_m2 = float(normalized)
    if area_m2 <= 0:
        raise ValueError
    return area_m2


def tasador(request):
    contexto = {}

    if request.method == 'POST':
        area_raw = request.POST.get('area_m2', '')
        contexto['area_ingresada'] = area_raw.strip()

        try:
            area_m2 = parse_area(area_raw)
            respuesta = requests.post(
                f'{settings.API_URL.rstrip("/")}/predict',
                json={'area_m2': area_m2},
                timeout=5,
            )
            respuesta.raise_for_status()
            data = respuesta.json()

            contexto['exito'] = True
            contexto['area_m2'] = data.get('area_m2')
            contexto['precio_estimado'] = data.get('predicted_price')

        except ValueError:
            contexto['error'] = 'Ingresa un número válido (ej: 85,5 o 85.5).'
        except requests.exceptions.ConnectionError:
            contexto['error'] = 'No fue posible conectar con la API de predicción.'
        except requests.exceptions.RequestException:
            contexto['error'] = 'Ocurrió un error al calcular el precio. Inténtalo de nuevo.'

    return render(request, 'app_predicc/index.html', contexto)
