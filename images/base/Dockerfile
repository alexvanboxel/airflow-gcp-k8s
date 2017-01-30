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
RUN pip install python-daemon
RUN pip install oauth2client==3.0.0
RUN pip install google-api-python-client
#RUN pip install flask
#RUN pip install flask_bcrypt
#RUN pip install flask_oauthlib
RUN pip install cryptography
RUN pip install MySQL-python
RUN pip install cython
RUN pip install pyyaml
RUN git clone https://github.com/alexvanboxel/airflow
RUN cd airflow && python setup.py install 
RUN pip install celery[redis]

# Set the application directory
WORKDIR /airflow

COPY init_airflow.sh /var/local/

