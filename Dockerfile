FROM arm32v6/alpine

RUN apk update && apk upgrade
RUN apk add python py-pip
RUN pip install RPi.bme280

COPY bme280-http.py /

CMD ["python", "/bme280-http.py"]
