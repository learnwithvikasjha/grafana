# Install Prometheus on centos using package manager

- Create a repository file called `prometheus.repo`
```
sudo touch /etc/yum.repos.d/prometheus.repo
```

- Write below in repository file.
```
[prometheus]
name=Prometheus repository
baseurl=https://packagecloud.io/prometheus-rpm/release/el/7/$basearch
gpgcheck=0
enabled=1
```
- Install Prometheus
```
sudo yum install -y prometheus
```
# Managing Prometheus Service
Use below commands to check status, start or stop Prometheus service.
```
sudo systemctl status prometheus
```
```
sudo systemctl start prometheus
```
```
sudo systemctl stop prometheus
```
# Prometheus Configuration File Location
Prometheus YML file is located at following `/etc/prometheus/prometheus.yml`
Here is what a default configuration file will look like.

```
# my global config
global:
  scrape_interval:     15s # Set the scrape interval to every 15 seconds. Default is every 1 minute.
  evaluation_interval: 15s # Evaluate rules every 15 seconds. The default is every 1 minute.
  # scrape_timeout is set to the global default (10s).

  # Attach these labels to any time series or alerts when communicating with
  # external systems (federation, remote storage, Alertmanager).
  external_labels:
      monitor: 'codelab-monitor'

# Load rules once and periodically evaluate them according to the global 'evaluation_interval'.
rule_files:
  # - "first.rules"
  # - "second.rules"

# A scrape configuration containing exactly one endpoint to scrape:
# Here it's Prometheus itself.
scrape_configs:
  # The job name is added as a label `job=<job_name>` to any timeseries scraped from this config.
  - job_name: 'prometheus'

    # metrics_path defaults to '/metrics'
    # scheme defaults to 'http'.

    static_configs:
      - targets: ['localhost:9090']
```
