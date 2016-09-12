from st2reactor.sensor.base import Sensor
from flask import Flask, request
import json

WEBHOOK_TRIGGER_REF = "example.echo"


class EchoSensor(Sensor):
    def __init__(self, sensor_service, config):
        super(EchoSensor, self).__init__(sensor_service=sensor_service, config=config)
        self.host = "0.0.0.0"
        self.port = 10001
        route = '/api/{}'.format('<string:action>')

        self.app = Flask(__name__)
        self.log = self._sensor_service.get_logger(__name__)

        @self.app.route('/status')
        def status():
            return json.dumps({"response": "OK"})

        @self.app.route(route, methods=['POST'])
        def echo(action):
            payload = {'headers': self._get_headers_as_dict(request.headers), 'body': request.json, 'action': action}
            self._sensor_service.dispatch(WEBHOOK_TRIGGER_REF, payload)
            return json.dumps({"response": "triggerposted"})

    def setup(self):
        pass

    def run(self):
        self.app.run(host=self.host, port=self.port, debug=True)

    def cleanup(self):
        # This is called when the st2 system goes down.
        pass

    # Methods required for programmable sensors.
    def add_trigger(self, trigger):
        pass

    def update_trigger(self, trigger):
        pass

    def remove_trigger(self, trigger):
        pass

    def _get_headers_as_dict(self, headers):
        headers_dict = {}
        for key, value in headers:
            headers_dict[key] = value
        return headers_dict
