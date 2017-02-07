class Create:
    method = 'POST'
    slug = False


class Update:
    method = 'PATCH'
    slug = True


class BulkUpdate:
    method = 'PUT'
    slug = False


class Fetch:
    method = 'GET'
    slug = True


class List:
    method = 'GET'
    slug = False


class Delete:
    method = 'DELETE'
    slug = True
