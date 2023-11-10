# node_exporter overview
node_exporter is a Prometheus exporter for collecting and exposing various metrics related to a Linux or UNIX system. It is part of the Prometheus monitoring and alerting ecosystem and serves as a fundamental component in gathering system-level metrics.

Here's a brief overview of what node_exporter does:

System Metrics:

Collects general system-level metrics such as CPU usage, memory usage, disk I/O, and network activity.
Provides information about the overall health and performance of the system.

# Install node_exporter
Create a file 
```
touch /etc/yum.repos.d/prometheus-node-exporter.repo
```
Write following content in the file
```
[prometheus-node-exporter]
name=prometheus-node-exporter
baseurl=https://packagecloud.io/prometheus-rpm/node_exporter/el/7/\$basearch
gpgcheck=1
enabled=1
gpgkey=https://packagecloud.io/prometheus-rpm/node_exporter/gpgkey
sslverify=1
```
