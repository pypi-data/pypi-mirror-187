from cgi import FieldStorage


class Request:
    # only 1 worker or middlewares
    _values_storage = {}

    def __init__(self, environ, response):
        self.environ = environ
        self.response = response
        self.url = ''
        self.form: FormData = None
        self.url_arguments = {}

    def append_value_to_storage(self, **kwargs):
        self._values_storage.update(kwargs)

    def get_storage_value(self, key: str):
        return self._values_storage.get(key)

    def clear_storage(self):
        self._values_storage.clear()

    def set_url_arguments(self, **kwargs):
        self.url_arguments.update(kwargs)

    def set_form_data(self, field_storage: FieldStorage):
        self.form = FormData(field_storage)

    def set_url(self, url: str):
        self.url = url


class FormData:
    def __init__(self, form_data):
        self.form_data: FieldStorage = form_data

    def get(self, key, default=None):
        return {'filename': self.form_data[key].filename, 'value': self.form_data.getvalue(key, default)}

    def get_value(self, key, default=None):
        return self.form_data.getvalue(key, default)

    def get_name(self, key):
        return self.form_data[key].filename

    def get_keys(self):
        return self.form_data.keys()
