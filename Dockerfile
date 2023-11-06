FROM tiangolo/uwsgi-nginx:python3.11

RUN apt-get -y clean \
    && apt-get -y update \
    && apt-get -y upgrade

RUN apt-get -y install \
    openssl \
    htop

COPY ./app /app
RUN chmod -R 777 /app
RUN chown -R 777 /root
WORKDIR /app

RUN pip3 install -r /app/requirements.txt

EXPOSE 5000
ENV TZ Europe/Paris

COPY nginx.conf /etc/nginx