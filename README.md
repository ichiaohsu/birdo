# birdo
birdo is a server/client pair to send sample through protobuf stream.

## Client

### Prerequisite

Before using the client script, dependencies must be installed. There is a `requirements.txt` in the `client` folder:
```bash
pip install -r requirements.txt
```

### Usage

Client script is in `client` directory. To use it, simply use:
```bash
python client.py
```
The CLI will prompt you to key in the file path and remote server url. File path is necessary. Then it will upload the content of the file.

** Before launching client, there should be a server running to catch the requests.**

## Server

Server is in `server` directory. First change directory into `server`.

### Run on MacOS

1. PostGIS database
This server use PostGIS function. So there are two things necessary:
- Install PostGIS
```bash
brew install postgis
```
- Create PostGIS extension in PostgreSQL server
Then in postgres CLI type to create extension:
```postgres
CREATE EXTENSION postgis;
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Run the server
Then it could be simply run in dev mode by:
```bash
python manage.py runserver
```

It could be used with uwsgi as well
```bash
uwsgi --ini uwsgi.ini
```

### Run on Kubernetes

1. First deploy PostgreSQL with PostGIS
If you have helm enabled in your kubernetes cluster:
```bash
helm install --name postgis --set postgresqlPassword=postgres,postgresqlDataDir="/bitnami/postgresql/data",persistence.storageClass=standard,persistence.size=5Gi,livenessProbe.initialDelaySeconds=120,postgresqlDatabase=birdo,image.registry=registry.weave.nl,image.repository=docker/postgres-postgis,image.tag=latest --set fullnameOverride=postgis stable/postgresql
```

If you don't, simply use the template in `server/k8s`:
```bash
kubectl apply -f k8s/postgis.yaml
```
2. Deploy birdo server
```bash
kubectl apply -f k8s/birdo.yaml
```

This will create an exposed ip address. You could see the address using:
```bash
kubectl get svc
```
Use `http://{server-address}:8000` in the client prompt.

## Questions
- Explain your database choice 

If there is no frequent demand on changing database schema, I will intend to select relational database, SQL instead of NoSQL. SQL are very reliable, high performance, and easy to establish the connection between different table. It is convenient considering future filter demands, and the nature of the data.

There are location data in this challenges. In my previous work experience, PostgreSQL supports abundant plugins, including PostGIS, which is a GeoData library. It could handle GPS data beautifully. Also, PostgreSQL has better statement optimizer, so it might have better efficiency.

And, it is the spatial database I am familiar with.

- How would you modify the system if the number of samples becomes really big?

Currently the server accept samples one-by-one. So each time it will only insert one piece of sample into the database and therefore create a lot of database session and connect overhead. To reduce the insert session, I think it could implement bulk insert, and insert multiple samples at once.

For really big amount of data, I will make the sample sent to a Pub/Sub or message queue, therefore the samples could be keep in the queue and be inserted later. From the insertion of the queue, there could be throttling mechanism implemented.

- How would you monitor the running services?

I will choose Prometheus to monitor the services. Since there are three components in this service: uwsgi, Django, PostgreSQL, I will work on these parts to monitor. 

In uwsgi, I will enable the monitoring modules in it, and create a new endpoint for Prometheus to scrape.

For PostgreSQL, I will use a side-car exporter to get the metrics.

For the Django, I will set the metrics, like current request, and response time in the `view` parts. These will help us to get the RPS and latency information.