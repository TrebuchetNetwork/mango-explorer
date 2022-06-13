
0) Install docker 


1) Pull Image

docker pull influx:2.2 

2) Get default config 

docker run --rm influxdb:2.2 influxd print-config > config.yml


3) Start the default stuff (please change this for prod) 

docker run -p 8086:8086 \
      -v $PWD/config.yml:/etc/influxdb2/config.yml \
      -v $PWD/data:/var/lib/influxdb2 \
      -e DOCKER_INFLUXDB_INIT_MODE=setup \
      -e DOCKER_INFLUXDB_INIT_USERNAME=my-user \
      -e DOCKER_INFLUXDB_INIT_PASSWORD=my-password \
      -e DOCKER_INFLUXDB_INIT_ORG=my-org \
      -e DOCKER_INFLUXDB_INIT_BUCKET=my-bucket \
      -e DOCKER_INFLUXDB_INIT_RETENTION=1y \
      -e DOCKER_INFLUXDB_INIT_ADMIN_TOKEN=my-super-secret-auth-token \
      influxdb:2.2

4) Adjust the file for ingestion config 

5) Run Borrow list tokens -> get interest rates borrow lend  xx (5 sec) tag symbol

python trebuchet/interest-influx.py


6) Run Funding rate -> perp list 

python trebuchet/funding-influx.py


7) Import dashboard_template...json 
In the UI import dashboard