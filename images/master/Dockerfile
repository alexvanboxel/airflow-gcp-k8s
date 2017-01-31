FROM b.gcr.io/airflow-gcp/airflow-base:1.8.0.alpha.400

RUN git fetch -vp && git checkout a50bfc915c66b5e44e1b30b1beae2458b61d1379 && python setup.py install
RUN pip install flask_bcrypt
RUN pip install flask_oauthlib
