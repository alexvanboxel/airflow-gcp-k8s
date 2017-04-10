FROM b.gcr.io/airflow-gcp/airflow-base:1.8.0.rc.100

RUN pip uninstall airflow -y
RUN git fetch -vp && git checkout 8e7a5583610be370dd26d50df0b7b98d90dbd396   && python setup.py install
RUN pip install flask_bcrypt
RUN pip install flask_oauthlib
