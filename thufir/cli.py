import click
from thufir.core import AlertAggregator
from integrations.prometheus import PrometheusIntegration, AWSCloudWatchIntegration, KubernetesIntegration

@click.group()
def cli():
    """Thufir: A lightweight tool for incident management."""
    pass

@cli.command()
@click.option("--prometheus-url", help="URL of the Prometheus server", required=True)
@click.option("--output", default="alerts.json", help="File to save the alerts")
def collect_alerts(prometheus_url, output):
    """Collect alerts from Prometheus and save to a file."""
    aggregator = AlertAggregator()
    prom = PrometheusIntegration(prometheus_url)
    alerts = prom.fetch_alerts()
    for alert in alerts:
        aggregator.add_alert(alert["source"], alert["message"], alert["severity"])
    aggregator.export_alerts(output)
    click.echo(f"Alerts collected and saved to {output}")

@click.command()
@click.option("--aws-region", default="us-east-1", help="AWS region for CloudWatch")
@click.option("--output", default="aws_alerts.json", help="File to save the alerts")
def collect_aws_alerts(aws_region, output):
    """Collect alerts from AWS CloudWatch and save to a file."""
    from thufir.core import AlertAggregator
    aggregator = AlertAggregator()
    aws = AWSCloudWatchIntegration(region_name=aws_region)
    alarms = aws.fetch_alarms()
    for alarm in alarms:
        aggregator.add_alert(alarm["source"], alarm["message"], alarm["severity"])
    aggregator.export_alerts(output)
    click.echo(f"AWS alerts collected and saved to {output}")


@click.command()
@click.option("--output", default="k8s_alerts.json", help="File to save the alerts")
def collect_k8s_alerts(output):
    """Collect alerts from Kubernetes and save to a file."""
    from thufir.core import AlertAggregator
    aggregator = AlertAggregator()
    k8s = KubernetesIntegration()
    events = k8s.fetch_events()
    for event in events:
        aggregator.add_alert(event["source"], event["message"], event["severity"])
    aggregator.export_alerts(output)
    click.echo(f"Kubernetes alerts collected and saved to {output}")

if __name__ == "__main__":
    cli()
