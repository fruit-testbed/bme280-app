Fruit Application for BME280
============================

This FruitOS application reads a BME280 environment sensor through I2C,
and publishes the sensor data via Syndicate.

Requirements
- Raspberry Pi 1, 2 or 3
- BME280 sensor, connected to Raspberry Pi's I2C GPIO
- [FruitOS](https://github.com/fruit-testbed/fruitos)
- (optional) [fruit-cli](https://github.com/fruit-testbed/fruit-cli)

You will also need to configure Syndicate on your node(s). This is not
yet automated.

To **run through console**:

```shell
docker run --device /dev/i2c-1 -ti leastfixedpoint/fruit-syndicate-bme280
```

The above assumes that the I2C device-tree and kernel module have been
loaded, and the BME280 sensor is connected to I2C port 1 (0x76). It
also assumes a Syndicate broker listening for WebSocket connections on
port 8000 on the node.


To **run through fruit-cli**:

```shell
fruit-cli container --filter /monitor/os/hostname = '"MYNODEHOSTNAME"' run \
  --kernel-module i2c-dev \
  --device-tree i2c_arm=on \
  --device /dev/i2c-1 \
  --name bme280-syndicate \
  leastfixedpoint/fruit-syndicate-bme280
```

To deploy the container, _fruit-cli_ is using [fruit-agent](https://github.com/fruit-testbed/fruit-agent),
which ensures that the I2C device-tree (`i2c_arm`) and kernel module (`i2c-dev`)
have been loaded before starting the container.
This works under condition that the BME280 sensor is connected to I2C port 1 (0x76).

See [LICENSE](LICENSE.txt).
