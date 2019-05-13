FROM python:3.7.3

RUN groupadd user && useradd --create-home --home-dir /home/user -g user user

COPY . /usr/src/app/birdo
WORKDIR /usr/src/app/birdo

RUN apt-get update \
    && apt-get install -y gdal-bin \
    && pip install --upgrade pip \
    && pip install -r requirements.txt 

EXPOSE 8000
CMD ["/bin/bash", "run.sh"]