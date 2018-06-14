Fruit Application for BME280
============================

This FruitOS application reads a BME280 environment sensor through I2C,
and returns the sensor data in JSON as a response of HTTP GET request.

Requirements
- Raspberry Pi 1, 2 or 3
- BME280 sensor, connected to Raspberry Pi's I2C GPIO
- [FruitOS](https://github.com/fruit-testbed/fruitos)
- (optional) [fruit-cli](https://github.com/fruit-testbed/fruit-cli)


To **run through console**:

```shell
docker run --device /dev/i2c-1 -p 8000:80 -ti herry13/fruit-bme280
```

The above assumes that the I2C device-tree and kernel module have been loaded,
and the BME280 sensor is connected to I2C port 1 (0x76).


To **run through fruit-cli**:

```shell
fruit-cli run-container --node mynode -p 8000:80 \
    -k i2c-dev -d i2c_arm=on --device /dev/i2c-1 \
    bme280 \
    herry13/fruit-bme280
```

To deploy the container, _fruit-cli_ is using [fruit-agent](https://github.com/fruit-testbed/fruit-agent),
which ensures that the I2C device-tree (`i2c_arm`) and kernel module (`i2c-dev`)
have been loaded before starting the container.
This works under condition that the BME280 sensor is connected to I2C port 1 (0x76).

See [LICENSE](LICENSE.txt).
