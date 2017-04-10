FROM b.gcr.io/airflow-gcp/airflow-base:1.8.0.rc.100

# A few problems with compiling Java from source:
#  1. Oracle.  Licensing prevents us from redistributing the official JDK.
#  2. Compiling OpenJDK also requires the JDK to be installed, and it gets
#       really hairy.

#RUN apt-get update && apt-get install -y --no-install-recommends \
#		bzip2 \
#		unzip \
#		xz-utils \
#	&& rm -rf /var/lib/apt/lists/*
#
#RUN echo 'deb http://httpredir.debian.org/debian jessie-backports main' > /etc/apt/sources.list.d/jessie-backports.list
#
## Default to UTF-8 file.encoding
#ENV LANG C.UTF-8
#
## add a simple script that can auto-detect the appropriate JAVA_HOME value
## based on whether the JDK or only the JRE is installed
#RUN { \
#		echo '#!/bin/sh'; \
#		echo 'set -e'; \
#		echo; \
#		echo 'dirname "$(dirname "$(readlink -f "$(which javac || which java)")")"'; \
#	} > /usr/local/bin/docker-java-home \
#	&& chmod +x /usr/local/bin/docker-java-home
#
#ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64
#
#ENV JAVA_VERSION 8u121
#ENV JAVA_DEBIAN_VERSION 8u121-b13-1~bpo8+1
#
#
## see https://bugs.debian.org/775775
## and https://github.com/docker-library/java/issues/19#issuecomment-70546872
#ENV CA_CERTIFICATES_JAVA_VERSION 20140324
#
#RUN set -x \
#	&& apt-get update \
#	&& apt-get install -y \
#        openjdk-8-jre="$JAVA_DEBIAN_VERSION" \
#        openjdk-8-jdk-headless="$JAVA_DEBIAN_VERSION"
#
#RUN set -x \
#	&& apt-get install -y \
#		openjdk-8-jdk="$JAVA_DEBIAN_VERSION" \
#		ca-certificates-java="$CA_CERTIFICATES_JAVA_VERSION" \
#	&& rm -rf /var/lib/apt/lists/* \
#	&& [ "$JAVA_HOME" = "$(docker-java-home)" ]
#
## see CA_CERTIFICATES_JAVA_VERSION notes above
#RUN /var/lib/dpkg/info/ca-certificates-java.postinst configure

RUN pip uninstall airflow -y
RUN git fetch -vp && git checkout 8e7a5583610be370dd26d50df0b7b98d90dbd396   && python setup.py install
RUN pip install flask_bcrypt
RUN pip install flask_oauthlib


RUN apt-get update && apt-get install -y --no-install-recommends \
		bzip2 \
		unzip \
		xz-utils \
	&& rm -rf /var/lib/apt/lists/*

RUN echo 'deb http://deb.debian.org/debian jessie-backports main' > /etc/apt/sources.list.d/jessie-backports.list

# Default to UTF-8 file.encoding
ENV LANG C.UTF-8

# add a simple script that can auto-detect the appropriate JAVA_HOME value
# based on whether the JDK or only the JRE is installed
RUN { \
		echo '#!/bin/sh'; \
		echo 'set -e'; \
		echo; \
		echo 'dirname "$(dirname "$(readlink -f "$(which javac || which java)")")"'; \
	} > /usr/local/bin/docker-java-home \
	&& chmod +x /usr/local/bin/docker-java-home

ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64

ENV JAVA_VERSION 8u121
ENV JAVA_DEBIAN_VERSION 8u121-b13-1~bpo8+1

# see https://bugs.debian.org/775775
# and https://github.com/docker-library/java/issues/19#issuecomment-70546872
ENV CA_CERTIFICATES_JAVA_VERSION 20161107~bpo8+1

RUN set -x \
	&& apt-get update \
	&& apt-get install -y \
		openjdk-8-jdk="$JAVA_DEBIAN_VERSION" \
		ca-certificates-java="$CA_CERTIFICATES_JAVA_VERSION" \
	&& rm -rf /var/lib/apt/lists/* \
	&& [ "$JAVA_HOME" = "$(docker-java-home)" ]

# see CA_CERTIFICATES_JAVA_VERSION notes above
RUN /var/lib/dpkg/info/ca-certificates-java.postinst configure
