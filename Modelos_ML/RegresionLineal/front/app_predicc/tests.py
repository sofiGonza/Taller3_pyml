from unittest.mock import patch

from django.test import TestCase

from .views import parse_area


class AreaParserTests(TestCase):
    def test_accepts_comma_decimal(self):
        self.assertEqual(parse_area('85,5'), 85.5)

    def test_accepts_dot_decimal_and_spaces(self):
        self.assertEqual(parse_area(' 85.5 '), 85.5)

    def test_rejects_invalid_or_non_positive_values(self):
        for value in ('', 'abc', '85,5.2', '0', '-10'):
            with self.assertRaises(ValueError):
                parse_area(value)


class TasadorViewTests(TestCase):
    @patch('app_predicc.views.requests.post')
    def test_submits_normalized_area_to_api(self, mock_post):
        mock_post.return_value.raise_for_status.return_value = None
        mock_post.return_value.json.return_value = {
            'area_m2': 85.5,
            'predicted_price': 250000000,
        }

        response = self.client.post('/', {'area_m2': '85,5'}, secure=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '250.000.000')
        mock_post.assert_called_once()
        self.assertEqual(mock_post.call_args.kwargs['json'], {'area_m2': 85.5})

    @patch('app_predicc.views.requests.post')
    def test_valid_area_reports_api_connection_error_separately(self, mock_post):
        mock_post.side_effect = __import__('requests').exceptions.ConnectionError

        response = self.client.post('/', {'area_m2': '85.5'}, secure=True)

        self.assertContains(response, 'No se pudo conectar con la API')
        self.assertNotContains(response, 'Ingresa un número válido')
