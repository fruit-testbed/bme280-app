FROM arm32v6/alpine
MAINTAINER Herry <herry13@gmail.com>

RUN apk --no-cache --no-progress upgrade
RUN apk --no-cache --no-progress add python py-pip
RUN pip install RPi.bme280

COPY bme280-http.py /

ENTRYPOINT ["/usr/bin/python", "/bme280-http.py"]
