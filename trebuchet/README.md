# Trebuchet.Network ML full node setup 
* trebuchet.network ML lab with decision trees train/inference example for funding rates with variable time horizon
* mango.markets funding rate connector for all available perpetuals 
* mango.markets interest rate connector for all vault tokens 

#### [optional] Run train/inference with or without GPU support (Nvidia Cuda)
Requirements:
* For GPU option - CUDA 11 GPU support 


## Setup

1) Pull influx-db image

```sudo docker pull influxdb:2.3 ```

2) Get default config 

`sudo docker run --rm influxdb:2.3 influxdb print-config > config.yml`



3) Adjust the file for ingestion config + install dependencies for venv + branch

```git checkout trebuchet```

4) Run the setup 

```make setup```

5) Start the default stuff (change this for prod) 
```
sudo docker run -p 8086:8086 \
      -v $PWD/config.yml:/etc/influxdb2/config.yml \
      -v $PWD/data:/var/lib/influxdb2 \
      -e DOCKER_INFLUXDB_INIT_MODE=setup \
      -e DOCKER_INFLUXDB_INIT_USERNAME=my-user \
      -e DOCKER_INFLUXDB_INIT_PASSWORD=my-password \
      -e DOCKER_INFLUXDB_INIT_ORG=my-org \
      -e DOCKER_INFLUXDB_INIT_BUCKET=my-bucket \
      -e DOCKER_INFLUXDB_INIT_RETENTION=102w \
      -e DOCKER_INFLUXDB_INIT_ADMIN_TOKEN=my-super-secret-auth-token \
      influxdb:2.3
```


6) Run the connectors for mango.markets

```python trebuchet/interest-influx.py```

```python trebuchet/funding-influx.py```


7) Import dashboard_template...json 
In the UI import dashboard on localhost:8086


8) Run the Jupter lab docker file in a new window
```
insert docker code with GPU support and without GPU support 
```

9) Example code can be found in 
/trebuchet/train

10) Access the LAB on ... .

Enjoy!