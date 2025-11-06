import logging

from odin.adapters.adapter import ApiAdapter, ApiAdapterResponse
from odin.adapters.parameter_tree import ParameterTreeError
from pico_comms.controller import TestController

class TestAdapter(ApiAdapter):
    def __init__(self, **kwargs):
        super(TestAdapter, self).__init__(**kwargs)

        self.controller = TestController()
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