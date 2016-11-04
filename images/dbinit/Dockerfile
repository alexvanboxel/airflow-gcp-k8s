FROM b.gcr.io/airflow-gcp/airflow-base:1.8.0.alpha.6

# A few problems with compiling Java from source:
#  1. Oracle.  Licensing prevents us from redistributing the official JDK.
#  2. Compiling OpenJDK also requires the JDK to be installed, and it gets
#       really hairy.

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

RUN git fetch -vp && git checkout 8ea382079b36c789500623ed8e1f0dc61dcab2c2 && python setup.py install


