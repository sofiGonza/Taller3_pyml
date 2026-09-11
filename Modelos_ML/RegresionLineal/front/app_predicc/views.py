import re

import requests
from django.conf import settings
from django.shortcuts import render


_DECIMAL_RE = re.compile(r'^\d+(?:[.,]\d+)?$')


def parse_area(value):
    """Convert a Spanish/English decimal input to a positive float."""
    normalized = value.strip().replace(' ', '').replace(',', '.')
    if not normalized or not _DECIMAL_RE.fullmatch(normalized):
        raise ValueError('Formato de área no válido')

    area_m2 = float(normalized)
    if area_m2 <= 0:
        raise ValueError('El área debe ser mayor que cero')
    return area_m2


def tasador(request):
    contexto = {}

    if request.method == 'POST':
        area_raw = request.POST.get('area_m2', '')
        contexto['area_ingresada'] = area_raw.strip()

        try:
            area_m2 = parse_area(area_raw)
        except ValueError:
            contexto['error'] = 'Ingresa un número válido mayor que cero (ej: 85,5 o 85.5).'
        else:
            try:
                respuesta = requests.post(
                    f'{settings.API_URL.rstrip("/")}/predict',
                    json={'area_m2': area_m2},
                    timeout=10,
                )
                respuesta.raise_for_status()
                data = respuesta.json()

                if 'predicted_price' not in data:
                    raise ValueError('La API no devolvió predicted_price')

                contexto['exito'] = True
                contexto['area_m2'] = data.get('area_m2', area_m2)
                contexto['precio_estimado'] = data['predicted_price']

            except requests.exceptions.ConnectionError:
                contexto['error'] = 'No se pudo conectar con la API. Revisa la variable API_URL en Railway.'
            except requests.exceptions.Timeout:
                contexto['error'] = 'La API tardó demasiado en responder.'
            except requests.exceptions.HTTPError as error:
                contexto['error'] = f'La API respondió con un error HTTP ({error.response.status_code}).'
            except (requests.exceptions.RequestException, ValueError):
                contexto['error'] = 'La API respondió con un formato inesperado.'

    return render(request, 'app_predicc/index.html', contexto)
