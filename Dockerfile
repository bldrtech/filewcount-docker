FROM debian:stretch-slim

RUN apt-get update \
	&& apt-get install -y --no-install-recommends \
	    build-essential \
	    curl \
	    libcurl4-openssl-dev \
	    pkg-config \
		python3-dev \
		python3-pip \
		python3-setuptools \
        nginx

COPY / /staging/

RUN pip3 install wheel==0.30.0
RUN pip3 install -r /staging/requirements.txt
RUN pip3 install uwsgi==2.0.16

RUN mkdir -p /usr/share/uwsgi/conf/ \
    && mkdir -p /etc/uwsgi/apps-enabled/ \
    && mkdir -p /var/log/uwsgi/app/ \
    && mkdir -p /etc/uwsgi/apps-enabled/ \
    && mkdir -p /run/uwsgi/upload/ \
    && mkdir -p /opt/upload/root \
    && mkdir -p /opt/upload/uploads \
    && chown www-data:www-data /opt/upload/uploads \
    && cp -r /staging/root /opt/upload/ \
    && cp /staging/configs/upload.ini /etc/uwsgi/apps-enabled/upload.ini \
    && cp /staging/configs/nginx.conf /etc/nginx/nginx.conf \
    && cp /staging/configs/upload.conf /etc/nginx/sites-enabled/upload.conf \
    && cp /staging/startup.sh /bin/startup.sh \
    && rm /etc/nginx/sites-enabled/default \
    && rm /etc/nginx/sites-available/default

RUN rm -rf /staging

EXPOSE 80 443

STOPSIGNAL SIGQUIT

CMD ["/bin/startup.sh"]