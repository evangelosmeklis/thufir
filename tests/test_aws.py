import unittest
from unittest.mock import patch
from thufir.integrations.aws import AWSCloudWatchIntegration

class TestAWSCloudWatchIntegration(unittest.TestCase):
    @patch("boto3.client")
    def test_fetch_alarms(self, mock_boto_client):
        mock_client = mock_boto_client.return_value
        mock_client.describe_alarms.return_value = {
            "MetricAlarms": [
                {"AlarmName": "HighCPUAlarm", "StateValue": "ALARM"}
            ]
        }

        aws = AWSCloudWatchIntegration(region_name="us-east-1")
        alarms = aws.fetch_alarms()

        self.assertEqual(len(alarms), 1)
        self.assertEqual(alarms[0]["source"], "AWS CloudWatch")
        self.assertEqual(alarms[0]["message"], "HighCPUAlarm")
        self.assertEqual(alarms[0]["severity"], "High")

if __name__ == "__main__":
    unittest.main()
