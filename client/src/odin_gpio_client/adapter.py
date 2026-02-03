import logging

from odin.adapters.adapter import ApiAdapter, ApiAdapterResponse
from odin_gpio_client.controller import ClientController
from odin.adapters.parameter_tree import ParameterTreeError

class ClientAdapter(ApiAdapter):
    def __init__(self, **kwargs):
        super(ClientAdapter, self).__init__(**kwargs)

        output_chip_path = str(self.options.get('output_chip_path', '1'))
        output_line_offset = int(self.options.get('output_line_offset', 4))

        input_chip_path = str(self.options.get('input_chip_path', '0'))
        input_line_offset = int(self.options.get('input_line_offset', 12))

        self.controller = ClientController(output_chip_path, output_line_offset, input_chip_path, input_line_offset)
        logging.debug("Adapter Loaded")

    def get(self, path, request):
        try:
            response = self.controller.get(path)
            status_code = 200
        except ParameterTreeError as e:
            response = {'error': str(e)}
            status_code = 400

        content_type = 'application/json'

        return ApiAdapterResponse(response, content_type=content_type, status_code=status_code)

    def cleanup(self):
        self.controller.cleanup()
