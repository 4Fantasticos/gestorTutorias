import json

from dajaxice.decorators import dajaxice_register
from django.core import serializers


@dajaxice_register
def sayHello(request, data):
    print data['dia']
    print data['profesor']
    print data['alumno']
    return json.dumps({'message':data})