FROM python:3.7.3

RUN groupadd user && useradd --create-home --home-dir /home/user -g user user

COPY . /usr/src/app/birdo
WORKDIR /usr/src/app/birdo

RUN apt-get update \
    && apt-get install -y gdal-bin sudo \
    && sudo apt-get install -y curl ca-certificates \
    && sudo sh -c echo 'deb http://apt.postgresql.org/pub/repos/apt/ stretch-pgdg main' >  /etc/apt/sources.list.d/pgdg.list \
    && wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add - \
    && sudo apt-get update \
    && sudo apt-get install -y postgresql-client-9.6 \
    && pip install --upgrade pip \
    && pip install -r requirements.txt

EXPOSE 8000
CMD ["/bin/bash", "run.sh"]
