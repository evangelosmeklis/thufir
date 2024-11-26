import unittest
from thufir.core import AlertAggregator

class TestAlertAggregator(unittest.TestCase):
    def test_add_alert(self):
        aggregator = AlertAggregator()
        aggregator.add_alert("TestSource", "Test Message", "Low")
        self.assertEqual(len(aggregator.alerts), 1)
        self.assertEqual(aggregator.alerts[0]["source"], "TestSource")

if __name__ == "__main__":
    unittest.main()
