from kubernetes import client, config

class KubernetesIntegration:
    def __init__(self):
        config.load_kube_config()  # Assumes kubeconfig is set up
        self.core_api = client.CoreV1Api()

    def fetch_events(self):
        """Fetch Kubernetes events from the cluster."""
        events = self.core_api.list_event_for_all_namespaces().items
        return [
            {
                "source": "Kubernetes",
                "message": event.message,
                "severity": "Warning" if event.type == "Warning" else "Normal",
            }
            for event in events
        ]
