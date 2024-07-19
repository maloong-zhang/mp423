kubectl delete -f auth/manifests
kubectl delete -f converter/manifests
kubectl delete -f notification/manifests
kubectl delete -f gateway/manifests



kubectl delete -f mongo/manifests
kubectl apply -f mongo/manifests


kubectl apply -f auth/manifests
kubectl apply -f converter/manifests
kubectl apply -f notification/manifests
kubectl apply -f gateway/manifests

kubectl delete -f rabbit/manifests
kubectl apply -f rabbit/manifests


 curl -X POST -u maloong2022@gmail.com:Admin123 http://mp3converter.com/login

 eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Im1hbG9vbmcyMDIyQGdtYWlsLmNvbSIsImV4cCI6MTcxOTY0NjcxNCwiaWF0IjoxNzE5NTYwMzE0LCJhZG1pbiI6dHJ1ZX0.epdabvk0kqv1ys6n4sTvRHucjtPbcSz6mFPrs2noJDE

 curl -X POST -F 'file=@./1.mp4' -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Im1hbG9vbmcyMDIyQGdtYWlsLmNvbSIsImV4cCI6MTcxOTY0NjcxNCwiaWF0IjoxNzE5NTYwMzE0LCJhZG1pbiI6dHJ1ZX0.epdabvk0kqv1ys6n4sTvRHucjtPbcSz6mFPrs2noJDE' http://mp3converter.com/upload

 curl --output some.mp3 -X GET -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6Im1hbG9vbmcyMDIyQGdtYWlsLmNvbSIsImV4cCI6MTcxOTY0NjcxNCwiaWF0IjoxNzE5NTYwMzE0LCJhZG1pbiI6dHJ1ZX0.epdabvk0kqv1ys6n4sTvRHucjtPbcSz6mFPrs2noJDE' "http://mp3converter.com/download?fid=667e8c7e9e07558d49740a8d"
