# Speedtest
## run in vm
Need to install "iperf3" for both server and client (server end will be installed in Dockerfile)
    client command: iperf3 -s

The destination IP must be reachable 

pip install Flask
pip install gunicorn

python3 app.py
<!-- sudo apt update
sudo apt install nginx
/etc/nginx/nginx.conf
sudo systemctl start nginx
sudo systemctl enable nginx -->


## run in docker
Need to install "iperf3" for client 
    client command: iperf3 -s

The destination IP must be reachable 

docker build -t ztkhero/tfnswspeed .

docker-compose up -d