#FROM python:3.6.4-alpine3.7
FROM python:2.7.14-alpine3.7

RUN apk add --no-cache bash \
      && apk add --update openssl \
      && apk add ca-certificates \
      && apk add --update make \
      && apk add --update alpine-sdk \
      && echo http://dl-2.alpinelinux.org/alpine/edge/community/ >> /etc/apk/repositories \
      && apk --no-cache add shadow \
      && mkdir -p /secrets/ssl/cert \
      && /usr/bin/openssl req -x509 -newkey rsa:2048 -nodes -keyout /secrets/ssl/cert/private_key.pem -out /secrets/ssl/cert/certificate.pem -days 365 -subj "/C=US/ST=Texas/L=Austin/O=Cisco/OU=longhorn/CN=python"

ENV CERTFILE /secrets/ssl/cert/certificate.pem
ENV PKEYFILE /secrets/ssl/cert/private_key.pem
ENV CAFILE /secrets/ssl/ca/ca_certificate.pem

COPY dist/template_adapter-1.0-py2.py3-none-any.whl /root/
RUN pip install /root/template_adapter-1.0-py2.py3-none-any.whl \
      && rm -f /root/*.whl && chmod +x /usr/local/bin/activities-worker

ENV JAIL_GROUPNAME script_executer
ENV JAIL_USERNAME script_executer
ENV JAIL_DIR /jail

COPY Makefile .
RUN make jail


EXPOSE 8082

ENTRYPOINT ["/usr/local/bin/activities-worker"]
