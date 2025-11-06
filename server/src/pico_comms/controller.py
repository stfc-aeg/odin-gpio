import json
import logging
import zmq
from zmq.error import ZMQError
from zmq.eventloop.zmqstream import ZMQStream

from odin.adapters.parameter_tree import ParameterTree

class TestController():

    def __init__(self):
        self.active = False
        self.rises = 0

        self.param_tree = ParameterTree({
            'active': (True, None),
            'rises': (lambda: self.rises, None)
        })

        self.ctrl_endpoint = f"tcp://192.168.0.13:5555"

        try:
            self.ctx = zmq.Context()

            self.ctrl_channel = self.ctx.socket(zmq.ROUTER)
            self.ctrl_channel.bind(self.ctrl_endpoint)

            self.ctrl_stream = ZMQStream(self.ctrl_channel)
            self.ctrl_stream.on_recv(self.handle_receive)

        except ZMQError as error:
            logging.error("Error initializing RPC server: %s", error)

    def get(self, path):
        return self.param_tree.get(path)

    def handle_receive(self, frames):
        decoded_string = frames[1].decode('utf-8')
        rises = json.loads(decoded_string)
        self.rises = rises['times_risen']
        identity = frames[0]
        self.ctrl_stream.send_multipart([identity, b'b'])