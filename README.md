
# Thufir

**Thufir** is a lightweight, open-source command-line tool designed to simplify incident detection, analysis, and resolution. It integrates seamlessly with popular monitoring tools like Prometheus and AWS to streamline operations and automate routine tasks, making system reliability easier to manage.

## Features

- **Alert Aggregation**: Collect alerts from multiple sources into a unified view.
- **Incident Detection**: Identify critical issues using predefined rules.
- **Log Analysis**: Parse logs for common patterns to suggest root causes.
- **Automated Actions**: Perform tasks like restarting services, scaling resources, or executing custom scripts.
- **Reporting**: Generate clear, actionable incident reports.
- **Notifications**: Notify teams through integrations like Slack.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/evangelosmeklis/thufir.git
   cd thufir
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -e .
   ```

## Usage

### Command-Line Interface (CLI)

Run the tool to collect alerts and generate a report:

```bash
thufir-cli --collect-alerts --output alerts.json
```

### Library Usage

Use the library in your Python projects:

```python
from thufir.core import AlertAggregator

aggregator = AlertAggregator()
aggregator.add_alert("Prometheus", "High CPU Usage", "Critical")
aggregator.export_alerts("alerts.json")
```

## Roadmap

- Add support for more integrations (e.g., Datadog, Splunk).
- Expand automated actions (e.g., rollback deployments).
- Improve logging and error handling.
- Add a plugin system for extensibility.

## Contributing

Contributions are welcome! Please fork this repository, make your changes, and submit a pull request.

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

---

Start building reliable and automated incident handling with **Thufir** today!