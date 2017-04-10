# Using official python runtime base image
FROM python:2.7.13

# MySQL Client for CloudSQL setup
RUN apt-get update && apt-get install -y --no-install-recommends \
		bzip2 \
		unzip \
		xz-utils \
	&& rm -rf /var/lib/apt/lists/*
RUN echo 'deb http://httpredir.debian.org/debian jessie-backports main' > /etc/apt/sources.list.d/jessie-backports.list
RUN set -x \
	&& apt-get update \
	&& apt-get install -y \
		mysql-client \
	&& rm -rf /var/lib/apt/lists/*

# Python dependencies
RUN pip install python-daemon \
    && pip install oauth2client==3.0.0 \
    && pip install google-api-python-client \
    && pip install cryptography \
    && pip install MySQL-python \
    && pip install cython \
    && pip install pyyaml
#RUN pip install flask
#RUN pip install flask_bcrypt
#RUN pip install flask_oauthlib
RUN git clone https://github.com/alexvanboxel/airflow \
    && cd airflow \
    && git checkout c64832718bd1cf3ca772b7bb9c61b51a2e27a12b \
    && python setup.py install
RUN pip install celery[redis]

# Set the application directory
WORKDIR /airflow

COPY init_airflow.sh /var/local/

