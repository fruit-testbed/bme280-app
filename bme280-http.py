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

BME280 = S.Record.makeConstructor('BME280', 'host timestamp temperature pressure humidity')
OverlayNode = S.Record.makeConstructor('OverlayNode', 'id')

i2c_port = 1
i2c_address = 0x76
i2c_bus = smbus2.SMBus(i2c_port)
calibration_params = bme280.load_calibration_params(i2c_bus, i2c_address)

argv = sys.argv
loop = asyncio.get_event_loop()

local_conn = S.Connection.from_url('ws://172.17.0.1:8000/#local')
federated_conn = S.Connection.from_url('ws://172.17.0.1:8000/#test')

def discover_hostname(conn):
    with conn.turn() as t:
        a = conn.actor()
        with a.react(t) as facet:
            print('Waiting to discover node ID...')
            def on_discovery(t, node_id):
                print('Discovered node ID', repr(node_id))
                sample_and_publish(federated_conn, node_id)
                a.stop(t)
            facet.add(S.Observe(OverlayNode(S.CAPTURE)), on_add=on_discovery)

def sample_and_publish(conn, hostname):
    with conn.turn() as t:
        with conn.actor().react(t) as facet:
            def sample(facet):
                data = bme280.sample(i2c_bus, i2c_address, calibration_params)
                item = BME280(hostname,
                              time.mktime(data.timestamp.timetuple()),
                              data.temperature,
                              data.pressure,
                              data.humidity)
                print(item)
                facet.add(item)
            facet.on_start(lambda turn: poller(turn, facet, 5, sample, loop))

discover_hostname(local_conn)

loop.create_task(local_conn.reconnecting_main(loop))
loop.create_task(federated_conn.reconnecting_main(loop))
loop.run_forever()
# loop.run_until_complete(federated_conn.reconnecting_main(loop))
