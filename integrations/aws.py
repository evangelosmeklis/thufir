import boto3

class AWSCloudWatchIntegration:
    def __init__(self, region_name="us-east-1"):
        self.client = boto3.client("cloudwatch", region_name=region_name)

    def fetch_alarms(self):
        """Fetch active CloudWatch alarms."""
        response = self.client.describe_alarms(StateValue="ALARM")
        alarms = response.get("MetricAlarms", [])
        return [
            {
                "source": "AWS CloudWatch",
                "message": alarm["AlarmName"],
                "severity": "High" if alarm["StateValue"] == "ALARM" else "Low",
            }
            for alarm in alarms
        ]
