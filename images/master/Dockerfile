FROM b.gcr.io/airflow-gcp/airflow-base:1.8.0.alpha.400

RUN git fetch -vp && git checkout 5f395306385a21c05e50b86ce096a036a4cf1f13 && python setup.py install
RUN pip install flask_bcrypt
RUN pip install flask_oauthlib
