BME280 Application
==================

This FruitOS application reads reads a BME280 environment sensor through I2C,
and then returns the sensor data in JSON as a response of HTTP GET request.

Requirements
- Raspberry Pi 1, 2 or 3
- BME280 sensor, connected to Raspberry Pi's I2C GPIO
- [FruitOS](https://github.com/fruit-testbed/fruitos)
- (optional) [fruit-cli](https://github.com/fruit-testbed/fruit-cli)


To **run through console**:

```shell
docker run --device /dev/i2c-1 -p 8000:80 -ti herry13/bme280:fruit
```


To **run through fruit-cli**:

```shell
fruit-cli run-container --node mynode -p 8000:80 \
    -k i2c-dev -d i2c_arm=on --device /dev/i2c-1 \
    bme280 \
    herry13/bme280:fruit
```


See [LICENSE](LICENSE.txt).
