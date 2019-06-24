FROM alpine:latest
MAINTAINER Tony Garnock-Jones <tonyg@leastfixedpoint.com>

RUN \
    apk --no-cache --no-progress upgrade && \
    apk --no-cache --no-progress add python3 py3-pip && \
    pip3 install RPi.bme280 mini-syndicate

COPY *.py /

ENTRYPOINT ["/usr/bin/python3", "/bme280-http.py"]
