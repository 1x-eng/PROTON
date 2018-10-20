__author__ = "Pruthvi Kumar, pruthvikumar.123@gmail.com"
__copyright__ = "Copyright (C) 2018 Pruthvi Kumar | http://www.apricity.co.in"
__license__ = "Public Domain"
__version__ = "1.0"

{% for controller in controllers %}
from mic.controllers.{{ controller.fileName }} import {{ controller.controllerName }}
{% endfor %}

class IFetch(object):

    def __init__(self):
        super(IFetch, self).__init__()

    def extract_controller_methods(self):
        controller_methods = []
        {% for controller in controllers %}
        controller_methods.append({'{{ controller.mic_name }}' : {
            'fileName': '{{ controller.fileName }}',
            'controllerName': '{{ controller.controllerName }}',
            'mic_name': '{{ controller.mic_name }}',
            'exposedMethodsInController': list({{controller.controllerName}}().controller_processor().keys()) }
        })
        {% endfor %}
        return controller_methods
