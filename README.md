# birdo
birdo is a server/client pair to send sample through protobuf stream.

## Client
Client script is in `client` directory. To use it, simple type:
```bash
python client.py
```
The CLI will prompt you to key in the file path and remote server url.

file path is necessary.
** Before launching client, there should be a server running to catch the requests.**

## Server

Server is put in `server` directory. First change directory into `server`.

### Prerequisite

#### Install dependencies
```bash
pip install -r requirements.txt
```
#### Postgresql server
This server use PostGIS function. So there are two things necessary:
1. Install PostGIS
2. Create PostGIS extension in PostgreSQL server

### Run the server
Then it could be simply run in dev mode by:
```bash
python manage.py runserver
```

It could be used with uwsgi
```bash
uwsgi --ini uwsgi.ini
```

## Use the Docker
In `server` directory
```bash
docker build . -t birdo:v1
```

## Kubernetes deployment

First deploy PostgreSQL with PostGIS
```bash
kubectl apply -f k8s/postgis.yaml
```

Then deploy birdo
```bash
kubectl apply -f k8s/birdo.yaml
```

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