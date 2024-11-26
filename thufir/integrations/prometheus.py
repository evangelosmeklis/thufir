import requests

class PrometheusIntegration:
    def __init__(self, prometheus_url):
        self.prometheus_url = prometheus_url

    def fetch_alerts(self):
        response = requests.get(f"{self.prometheus_url}/api/v1/query", params={"query": "ALERTS"})
        if response.status_code == 200:
            data = response.json()
            return [
                {
                    "source": "Prometheus",
                    "message": alert["metric"]["alertname"],
                    "severity": alert["metric"].get("severity", "Unknown"),
                }
                for alert in data["data"]["result"]
            ]
        else:
            raise Exception(f"Failed to fetch alerts: {response.status_code}")
