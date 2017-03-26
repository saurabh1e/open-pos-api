from sqlalchemy.exc import OperationalError, IntegrityError


class SQlOperationalError(OperationalError):
    def __init__(self, data, message, operation, status):

        self.message = self.construct_error_message(data, message, operation)
        self.status = status

    def _get_message(self):
        return self._message

    def _set_message(self, message):
        self._message = message

    message = property(_get_message, _set_message)

    def _get_status(self):
        return self._status

    def _set_status(self, status):
        self._status = status

    status = property(_get_status, _set_status)

    @staticmethod
    def construct_error_message(data, message, operation):
        return {'data': data, 'message': message, 'operation': operation}


class SQLIntegrityError(IntegrityError):
    def __init__(self, data, message, operation, status):

        self.message = self.construct_error_message(data, message, operation)
        self.status = status

    def _get_message(self):
        return self._message

    def _set_message(self, message):
        self._message = message

    message = property(_get_message, _set_message)

    def _get_status(self):
        return self._status

    def _set_status(self, status):
        self._status = status

    status = property(_get_status, _set_status)

    @staticmethod
    def construct_error_message(data, message, operation):
        return {'data': data, 'message': message, 'operation': operation}


class CustomException(Exception):

    def __init__(self, data, message, operation, status=400):

        self.message = self.construct_error_message(data, message, operation)
        self.status = status

    def _get_message(self):
        return self._message

    def _set_message(self, message):
        self._message = message

    message = property(_get_message, _set_message)

    def _get_status(self):
        return self._status

    def _set_status(self, status):
        self._status = status

    status = property(_get_status, _set_status)

    @staticmethod
    def construct_error_message(data, message, operation):
        return {'data': data, 'message': message, 'operation': operation}


class ResourceNotFound(CustomException):

    status = 404


class RequestNotAllowed(CustomException):

    status = 401
