from datetime import datetime
import json

class AlertAggregator:
    def __init__(self):
        self.alerts = []

    def add_alert(self, source, message, severity="Low"):
        alert = {
            "timestamp": datetime.now().isoformat(),
            "source": source,
            "message": message,
            "severity": severity,
        }
        self.alerts.append(alert)

    def export_alerts(self, filename):
        with open(filename, "w") as f:
            json.dump(self.alerts, f, indent=4)