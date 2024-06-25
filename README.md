# Speedtest
## run in vm
The destination IP must be reachable 

pip install Flask
pip install gunicorn

python3 app.py
<!-- sudo apt update
sudo apt install nginx
/etc/nginx/nginx.conf
sudo systemctl start nginx
sudo systemctl enable nginx -->


## run in docker (recommand)
The destination IP must be reachable 

docker build -t ztkhero/tfnswspeed .

docker-compose up -d