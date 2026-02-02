import json
import logging
import zmq
from zmq.error import ZMQError
from zmq.eventloop.zmqstream import ZMQStream

from odin.adapters.parameter_tree import ParameterTree

class GpioServerControllerError(Exception):
    pass

class GpioServerController():

    def __init__(self):
        self.event_callback = None

        self.ctrl_endpoint = f"tcp://192.168.0.58:5555"

        try:
            self.ctx = zmq.Context()

            self.ctrl_channel = self.ctx.socket(zmq.ROUTER)
            self.ctrl_channel.bind(self.ctrl_endpoint)

            self.ctrl_stream = ZMQStream(self.ctrl_channel)
            self.ctrl_stream.on_recv(self.handle_receive)

        except ZMQError as error:
            logging.error("Error initializing RPC server: %s", error)

    def register_event(self, event_callback):
        self.event_callback = event_callback

    def handle_receive(self, frames):
        decoded_string = frames[1].decode('utf-8')
        triggers = json.loads(decoded_string)

        if self.event_callback:
            self.event_callback(frames[0])
        
    def reply(self, identity):
        self.ctrl_stream.send_multipart([identity, b'b'])

    def get_reply_method(self):
        return self.reply