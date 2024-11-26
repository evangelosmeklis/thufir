import unittest
from unittest.mock import patch
from thufir.integrations.prometheus import PrometheusIntegration

class TestPrometheusIntegration(unittest.TestCase):
    @patch("requests.get")
    def test_fetch_alerts(self, mock_get):
        mock_response = {
            "status": "success",
            "data": {
                "result": [
                    {
                        "metric": {"alertname": "HighCPU", "severity": "Critical"},
                        "value": [1690815000.0, "1"]
                    }
                ]
            }
        }
        mock_get.return_value.json.return_value = mock_response
        mock_get.return_value.status_code = 200

        prometheus = PrometheusIntegration("http://localhost:9090")
        alerts = prometheus.fetch_alerts()

        self.assertEqual(len(alerts), 1)
        self.assertEqual(alerts[0]["source"], "Prometheus")
        self.assertEqual(alerts[0]["message"], "HighCPU")
        self.assertEqual(alerts[0]["severity"], "Critical")

if __name__ == "__main__":
    unittest.main()
