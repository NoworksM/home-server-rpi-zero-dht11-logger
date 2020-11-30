from unittest import TestCase
from home_server_api_client import HomeServerApiClient


class TestHomeServerApiClient(TestCase):

    def test_authenticate(self):
        client = HomeServerApiClient("http://localhost:8081", "6c8c2ee2-b277-4448-ae4c-c625190e94d3", "testsecret")
        if not client.authenticate():
            self.fail()

    def test_create_reading(self):
        client = HomeServerApiClient("http://localhost:8081", "6c8c2ee2-b277-4448-ae4c-c625190e94d3", "testsecret")
        if not client.authenticate():
            self.fail()
        if not client.create_reading("Temperature", 69):
            self.fail()
