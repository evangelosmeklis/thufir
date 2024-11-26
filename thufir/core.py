import json

class AlertAggregator:
    def __init__(self):
        self.alerts = []

    def add_alert(self, source, message, severity):
        self.alerts.append({"source": source, "message": message, "severity": severity})

    def export_alerts(self, output_file):
        with open(output_file, "w") as f:
            json.dump(self.alerts, f, indent=4)