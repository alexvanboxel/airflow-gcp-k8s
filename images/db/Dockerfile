FROM alpine:3.4

RUN apk add --update ca-certificates
RUN wget http://dl.google.com/cloudsql/cloud_sql_proxy.linux.amd64 && mv cloud_sql_proxy.linux.amd64 /cloud_sql_proxy && chmod +x /cloud_sql_proxy

EXPOSE 3306
