import logging

from odin.adapters.adapter import ApiAdapter, ApiAdapterResponse
from odin.adapters.parameter_tree import ParameterTreeError
from odin_gpio_server.controller import GpioServerController, GpioServerControllerError
from tornado.escape import json_decode

class GpioServerAdapter(ApiAdapter):
    def __init__(self, **kwargs):
        super(GpioServerAdapter, self).__init__(**kwargs)

        self.controller = GpioServerController()
        logging.debug("Adapter Loaded")

    def get_controller(self):
        return self.controller

    def get(self, path, request):
        try:
            response = self.controller.get(path)
            status_code = 200
        except ParameterTreeError as e:
            response = {'error': str(e)}
            status_code = 400

        content_type = 'application/json'

        return ApiAdapterResponse(response, content_type=content_type, status_code=status_code)

    def put(self, path, request):
        """Handle a HTTP PUT request."""
        content_type = "application/json"

        try:
            # Send the set request to the controller
            data = json_decode(request.body)
            self.controller.set(path, data)
            response = self.controller.get(path)
            status_code = 200
        except GpioServerControllerError as e:
            response = {"error": str(e)}
            status_code = 400
        except (TypeError, ValueError) as e:
            response = {"error": f"Failed to decode PUT request body: {str(e)}"}
            status_code = 400

        return ApiAdapterResponse(
            response, content_type=content_type, status_code=status_code
        )

    def cleanup(self):
        self.controller.cleanup()