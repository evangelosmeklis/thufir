import unittest
from unittest.mock import patch, MagicMock
from thufir.integrations.kubernetes import KubernetesIntegration

class TestKubernetesIntegration(unittest.TestCase):
    @patch("kubernetes.client.CoreV1Api.list_event_for_all_namespaces")
    @patch("kubernetes.config.load_kube_config")
    def test_fetch_events(self, mock_load_kube_config, mock_list_events):
        # Simulate Kubernetes API response
        mock_event = MagicMock()
        mock_event.message = "Pod crash detected"
        mock_event.type = "Warning"
        mock_list_events.return_value.items = [mock_event]

        kubernetes = KubernetesIntegration()
        events = kubernetes.fetch_events()

        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]["message"], "Pod crash detected")
        self.assertEqual(events[0]["severity"], "Warning")

if __name__ == "__main__":
    unittest.main()
