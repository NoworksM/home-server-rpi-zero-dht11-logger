import requests


class HomeServerApiClient:
    def __init__(self, endpoint, sensor_id, secret):
        self._endpoint = endpoint
        self._token = None
        self._sensor_id = sensor_id
        self._secret = secret

    def authenticate(self):
        self._token = None
        r = requests.post(self._endpoint + "/auth/sensor", {"sensorId": self._sensor_id, "secret": self._secret},
                          timeout=30)
        if r.status_code == 200:
            token = r.json().get("token", None)

            if token is None:
                return False
            else:
                self._token = token
                return True
        else:
            return False

    def create_reading(self, reading_type, value):
        if not self._token:
            return False

        headers = {"Authorization": "Bearer " + self._token}
        data = {"type": reading_type, "value": value}

        r = requests.post(self._endpoint + "/readings", json=data,
                          headers=headers)

        if r.status_code == 200:

            return True
        elif r.status_code == 401:
            return False
        else:
            return False
