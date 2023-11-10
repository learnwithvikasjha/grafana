# node_exporter overview
node_exporter is a Prometheus exporter for collecting and exposing various metrics related to a Linux or UNIX system. It is part of the Prometheus monitoring and alerting ecosystem and serves as a fundamental component in gathering system-level metrics.

Here's a brief overview of what node_exporter does:

System Metrics:

Collects general system-level metrics such as CPU usage, memory usage, disk I/O, and network activity.
Provides information about the overall health and performance of the system.

# Download and extract Node Exporter
- You can download node exporter from this link.
[Download Node Exporter](https://prometheus.io/download/#node_exporter)
- Extract Node Explorer
```
tar -xzvf node_exporter*.gz
```
- Create a user which we will use to run node_exporter service
Username: nodeusr
```
sudo useradd -rs /bin/false nodeusr
```


# Configuring Node Exporter to run as a service
create a file
```
touch /etc/systemd/system/node_exporter.service
```

write below content in the file.

```
[Unit]
Description=Node Exporter
After=network.target

[Service]
User=nodeusr
Group=nodeusr
Type=simple
ExecStart=/usr/local/bin/node_exporter --web.listen-address=:9105

[Install]
WantedBy=multi-user.target
```

# Start node_exporter service
```
sudo systemctl daemon-reload
sudo systemctl start node_exporter
sudo systemctl enable node_exporter
sudo systemctl status node_exporter
```
