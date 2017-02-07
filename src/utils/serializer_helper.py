# from itsdangerous import URLSafeTimedSerializer
# from . import app
#
# key = app.config['SECRET_KEY']
# salt = app.config['SECURITY_LOGIN_SALT']
# time = app.config['MAX_AGE']
#
#
# def get_serializer():
#     return URLSafeTimedSerializer(key, salt)
#
#
# def serialize_data(data):
#     return get_serializer().dumps(data)
#
#
# def deserialize_data(data):
#     return get_serializer().loads(data, time)
