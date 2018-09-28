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

    def extractControllerMethods(self):
        controllerMethods = []
        {% for controller in controllers %}
        controllerMethods.append({'{{ controller.micName }}' : {
            'fileName': '{{ controller.fileName }}',
            'controllerName': '{{ controller.controllerName }}',
            'micName': '{{ controller.micName }}',
            'exposedMethodsInController': list({{controller.controllerName}}().controllerProcessor().keys()) }
        })
        {% endfor %}
        return controllerMethods
