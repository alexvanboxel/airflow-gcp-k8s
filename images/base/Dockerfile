# Using official python runtime base image
FROM python:2.7.12

#RUN apt-get install python-mysqldb
#RUN apk add --update alpine-sdk
#RUN apk add --update py-numpy ca-certificates
#RUN pip install --index-url=http://pypi.python.org/simple/ --trusted-host pypi.python.org numpy
RUN pip install python-daemon
RUN pip install google-api-python-client 
RUN pip install flask
RUN pip install flask_bcrypt
RUN pip install flask_oauthlib
RUN pip install cryptography
RUN pip install MySQL-python
RUN pip install cython
RUN pip install slackclient
RUN pip install pyyaml
RUN git clone https://github.com/alexvanboxel/airflow
RUN cd airflow && python setup.py install 
RUN pip install celery[redis]
# Set the application directory

WORKDIR /airflow

# Install our requirements.txt
#ADD requirements.txt /app/requirements.txt
#RUN pip install -r requirements.txt

# Copy our code from the current folder to /app inside the container
#ADD airflow  /airflow

