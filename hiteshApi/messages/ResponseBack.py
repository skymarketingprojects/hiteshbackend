import dotsi
from rest_framework.response import Response

# d = dotsi.Dict({"foo": {"bar": "baz"}})
# d.foo.bar


def LocalResponseBack(message='', data={}, code=1):
    obj = {
        'message': message,
        'data': data,
        'code': code
    }
    model = dotsi.Dict(obj)
    return model

def ResponseBack(message='', data={}, code=1):
    obj = {
        'message': message,
        'data': data,
        'code': code
    }
    return Response(obj)

