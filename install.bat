docker stop soe.test
docker rm soe.test
docker rmi soe.test
docker build -t soe.test .
docker run -ti --sysctl net.core.somaxconn=4096 -d -p 5000:80 --name=soe.test --restart unless-stopped soe.test