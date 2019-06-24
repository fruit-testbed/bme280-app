#!/usr/bin/env python3

'''
Dependency:
- Python2
- RPi.bme280 module (`pip install RPi.bme280`)
- mini-syndicate (`pip install mini-syndicate`)
'''

import sys
import smbus2
import bme280
import asyncio
import syndicate.mini.core as S
from syndicateutils import poller
import time

BME280 = S.Record.makeConstructor('BME280', 'id timestamp temperature pressure humidity')

i2c_port = 1
i2c_address = 0x76
i2c_bus = smbus2.SMBus(i2c_port)
calibration_params = bme280.load_calibration_params(i2c_bus, i2c_address)

def sample(facet):
    data = bme280.sample(i2c_bus, i2c_address, calibration_params)
    item = BME280(str(data.id),
                  time.mktime(data.timestamp.timetuple()),
                  data.temperature,
                  data.pressure,
                  data.humidity)
    print(item)
    facet.add(item)

argv = sys.argv
conn = S.Connection.from_url(argv[1] if len(argv) == 2 else 'ws://172.17.0.1:8000/#test')
loop = asyncio.get_event_loop()

with conn.turn() as t:
    with conn.actor().react(t) as facet:
        facet.on_start(lambda turn: poller(turn, facet, 5, sample, loop))

loop.run_until_complete(conn.reconnecting_main(loop))
