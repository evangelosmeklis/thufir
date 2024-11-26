import unittest
from unittest.mock import patch
from thufir.integrations.aws import AWSCloudWatchIntegration

class TestAWSCloudWatchIntegration(unittest.TestCase):
    @mock_cloudwatch
    def test_fetch_alarms(self):
        # Setup mocked AWS environment
        client = boto3.client("cloudwatch", region_name="us-east-1")
        client.put_metric_alarm(
            AlarmName="HighCPUAlarm",
            MetricName="CPUUtilization",
            Namespace="AWS/EC2",
            Statistic="Average",
            Period=60,
            EvaluationPeriods=1,
            Threshold=80.0,
            ComparisonOperator="GreaterThanThreshold",
            AlarmActions=[],
        )

        aws = AWSCloudWatchIntegration(region_name="us-east-1")
        alarms = aws.fetch_alarms()

        self.assertEqual(len(alarms), 1)
        self.assertEqual(alarms[0]["message"], "HighCPUAlarm")
        self.assertEqual(alarms[0]["severity"], "High")

if __name__ == "__main__":
    unittest.main()
