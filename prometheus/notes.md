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
