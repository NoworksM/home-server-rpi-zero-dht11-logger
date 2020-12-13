class Config:
    def __init__(self, endpoint, sensor_id, secret, time_between_reports_in_seconds, pin_number):
        self.endpoint = endpoint
        self.sensor_id = sensor_id
        self.secret = secret
        self.time_between_reports_in_seconds = time_between_reports_in_seconds
        self.pin_number = pin_number

    def is_valid(self):
        return self.endpoint is str and self.sensor_id is str and self.secret is str and (
                self.time_between_reports_in_seconds is int or self.time_between_reports_in_seconds is float)
