import argparse
import time
from config import Config
from os import path
from pathlib import Path
from home_server_api_client import HomeServerApiClient
from requests.exceptions import Timeout

import board
import adafruit_dht

default_config_path = path.join(str(Path.home()), ".homeserver_logger_config.json")


def load_config(config_file_path=None):
    if config_file_path is None:
        config_file_path = default_config_path

    if not path.exists(config_file_path):
        return None

    from json import load
    with open(config_file_path, "r") as f:
        raw_config = load(f)

        sensor_id = raw_config.get("sensorId", None)
        secret = raw_config.get("secret", None)
        endpoint = raw_config.get("serverEndpoint", None)
        time_between_reports_in_seconds = raw_config.get("reportTimeSeconds", 60)
        pin_number = raw_config.get("pin", None)

        if sensor_id is None and secret is None and endpoint is None and pin_number is None:
            return None

        return Config(endpoint, sensor_id, secret, time_between_reports_in_seconds, pin_number)


def run_logger(config):
    pin_number = board.__dict__.get("D" + str(config.pin_number), None)

    if pin_number is None:
        print("invalid pin number %d" % config.pin_number)
        return

    api_client = HomeServerApiClient(config.endpoint, config.sensor_id, config.secret)

    try:
        success = api_client.authenticate()

        if not success:
            print("invalid sensor credentials")
            return
    except Timeout:
        print("server took too long to respond")
        return

    dht_device = adafruit_dht.DHT11(pin_number)

    while True:
        # noinspection PyBroadException
        try:
            temperature_celsius = dht_device.temperature
            humidity = dht_device.humidity

            api_client.create_reading("Temperature", temperature_celsius)
            api_client.create_reading("Humidity", humidity)

            time.sleep(config.time_between_reports_in_seconds)
        except Exception:
            pass


def main():
    parser = argparse.ArgumentParser(description="Run DHT sensor logger to external API server")
    parser.add_argument("-s", "--sensor-id", help="sensor id to send requests as")
    parser.add_argument("-t", "--secret-token", help="secret for the sensor to verify as")
    parser.add_argument("-e", "--endpoint", help="endpoint to interface with")
    parser.add_argument("-r", "--report-frequency", help="time to wait between reports in seconds")
    parser.add_argument("-p", "--pin-number", help="pin number that DHT sensor is attached to")
    parser.add_argument("-c", "--config",
                        help="alternate config file to use instead of default location of ~/.home_server_logger.json")

    args = parser.parse_args()

    config_path = args.config

    sensor_id = args.sensor_id
    secret = args.secret_token
    endpoint = args.endpoint
    time_between_reports_in_seconds = args.report_frequency
    pin_number = args.pin_number

    if sensor_id is str and secret is str and endpoint is str and (
            time_between_reports_in_seconds is int or time_between_reports_in_seconds is float) and pin_number is int:
        config = Config(endpoint, sensor_id, secret, time_between_reports_in_seconds, pin_number)
    else:
        config = load_config(config_path)

    # no config file found at path, print error message and exit
    if config is None:
        print("invalid config file found, or config file doesn't exist")
        return

    # command line overrides take precedence over config file
    if sensor_id is str:
        config.sensor_id = sensor_id
    if secret is str:
        config.secret = secret
    if endpoint is str:
        config.endpoint = endpoint
    if time_between_reports_in_seconds is int or time_between_reports_in_seconds is float:
        config.time_between_reports_in_seconds = time_between_reports_in_seconds
    if pin_number is int:
        config.pin_number = pin_number

    run_logger(config)


if __name__ == '__main__':
    main()
