import json
import random
import zmq

from odin_gpio_client.input_manager import inputManager
from odin_gpio_client.output_manager import outputManager
from odin.adapters.parameter_tree import ParameterTree
from zmq.eventloop.zmqstream import ZMQStream

class ClientController:

    def __init__(self, output_chip_path, output_line_offset, input_chip_path, input_line_offset):
        self.output_manager = outputManager(output_chip_path, output_line_offset)
        self.input_manager = inputManager(input_chip_path, input_line_offset, self.output_manager, self.do_req)

        self.param_tree = ParameterTree({
            'active': (True, None)
        })

        self.ctrl_endpoint = f"tcp://192.168.0.58:5555"

        self.ctx = zmq.Context()
        self.ctrl_socket = self.ctx.socket(zmq.DEALER)

        identity = "{:04x}-{:04x}".format(random.randrange(0x10000), random.randrange(0x10000))
        self.ctrl_socket.setsockopt(zmq.IDENTITY, identity.encode("utf-8"))
        self.ctrl_socket.connect(self.ctrl_endpoint)

        self.ctrl_stream = ZMQStream(self.ctrl_socket)
        self.ctrl_stream.on_recv(self.output_manager.pulse)

    def get(self, path):
        return self.param_tree.get(path)

    def cleanup(self):
        self.input_manager.active = False

    def do_req(self, rises):
        message = json.dumps({'times_risen': rises})
        self.ctrl_stream.send_string(message)
