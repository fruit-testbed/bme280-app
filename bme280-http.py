#!/usr/bin/env python

'''
Dependency:
- Python2
- RPi.bme280 module (`pip install RPi.bme280`)
'''

import smbus2
import bme280
import json
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
import time

http_port = 80
i2c_port = 1
i2c_address = 0x76
i2c_bus = smbus2.SMBus(i2c_port)
calibration_params = bme280.load_calibration_params(i2c_bus, i2c_address)

class Handler(BaseHTTPRequestHandler):
	def do_GET(self):
		sample = bme280.sample(i2c_bus, i2c_address, calibration_params)
		data = {
			'id': str(sample.id),
			'timestamp': time.mktime(sample.timestamp.timetuple()),
			'temp': sample.temperature,
			'pressure': sample.pressure,
			'humidity': sample.humidity,
		}
		self.send_response(200)
		self.send_header('Content-Type', 'application/json')
		self.end_headers()
		self.wfile.write(json.dumps(data))

httpd = HTTPServer(('', http_port), Handler)
print 'Starting httpd at port', http_port, '...'
httpd.serve_forever()
