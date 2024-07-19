## mp423

### Architecture

![Architecture](https://s2.loli.net/2024/07/19/9QWsKxoXaiSB51g.png)

### NOTE

> This project need to create two queue first, one name is "video" and the other is "mp3", you can use the ingress service: ["Rabbit Management"](http://rabbitmq-manager.com)

### Create a Environment

```bash
python3 -m venv .venv
source ./venv/bin/activate.fish
```

### Generate Requirements

```bash
pip3 freeze > requirements.txt
```

### Delete K8S Server

```bash
kubectl delete -f auth/manifests
kubectl delete -f converter/manifests
kubectl delete -f notification/manifests
kubectl delete -f gateway/manifests
kubectl delete -f mongo/manifests
kubectl delete -f rabbit/manifests
```

### Start K8S Server

```bash
kubectl apply -f mongo/manifests
kubectl apply -f auth/manifests
kubectl apply -f converter/manifests
kubectl apply -f notification/manifests
kubectl apply -f gateway/manifests
kubectl apply -f rabbit/manifests
```

### Management Address

[RabbitMQ](http://rabbitmq-manager.com)
[MongoDB](http://mongo-express.com)

### Change Host File

```bash
##
# Host Database
#
# localhost is used to configure the loopback interface
# when the system is booting.  Do not change this entry.
##
127.0.0.1 localhost
255.255.255.255 broadcasthost
::1             localhost
# Added by Docker Desktop
# To allow the same kube context to work on the host and the container:
127.0.0.1 kubernetes.docker.internal
192.168.49.2 mongo.express.com
# End of section
127.0.0.1 mp3converter.com
127.0.0.1 rabbitmq-manager.com
127.0.0.1 host.minikube.internal
127.0.0.1 mongo-express.com

```

### Login In

```bash
 curl -X POST -u maloong2022@gmail.com:Admin123 http://mp3converter.com/login
```

get the jwt token

```bash
 eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Im1hbG9vbmcyMDIyQGdtYWlsLmNvbSIsImV4cCI6MTcxOTY0NjcxNCwiaWF0IjoxNzE5NTYwMzE0LCJhZG1pbiI6dHJ1ZX0.epdabvk0kqv1ys6n4sTvRHucjtPbcSz6mFPrs2noJDE
```

### Put the MP4 file

```bash
 curl -X POST -F 'file=@./1.mp4' -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Im1hbG9vbmcyMDIyQGdtYWlsLmNvbSIsImV4cCI6MTcxOTY0NjcxNCwiaWF0IjoxNzE5NTYwMzE0LCJhZG1pbiI6dHJ1ZX0.epdabvk0kqv1ys6n4sTvRHucjtPbcSz6mFPrs2noJDE' http://mp3converter.com/upload
```

### Get file ID from the email

```bash
667e8c7e9e07558d49740a8d
```

### Get the MP3 file

```bash
 curl --output some.mp3 -X GET -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Im1hbG9vbmcyMDIyQGdtYWlsLmNvbSIsImV4cCI6MTcxOTY0NjcxNCwiaWF0IjoxNzE5NTYwMzE0LCJhZG1pbiI6dHJ1ZX0.epdabvk0kqv1ys6n4sTvRHucjtPbcSz6mFPrs2noJDE' "http://mp3converter.com/download?fid=667e8c7e9e07558d49740a8d"
```
