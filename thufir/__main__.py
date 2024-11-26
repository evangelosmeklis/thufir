import argparse
from thufir.core import AlertAggregator

def main():
    parser = argparse.ArgumentParser(description="Incident detection and resolution tool.")
    parser.add_argument("--collect-alerts", help="Collect alerts from sources", action="store_true")
    parser.add_argument("--output", help="Output file for alerts", type=str)
    args = parser.parse_args()

    if args.collect_alerts:
        aggregator = AlertAggregator()
        aggregator.add_alert("Prometheus", "High CPU Usage", "Critical")
        aggregator.add_alert("AWS", "Instance Unreachable", "High")
        aggregator.export_alerts(args.output)
        print(f"Alerts saved to {args.output}")

if __name__ == "__main__":
    main()
