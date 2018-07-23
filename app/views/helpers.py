import json

from flask import request, abort
from flask.views import MethodView

from app.database import db


class APIView(MethodView):
    get_fields = []
    post_fields = []
    datetime_format = '%Y-%m-%d %H:%M:%S'

    def __init__(self):
        super().__init__()
        self.session = db.session
        self.request = request

    @staticmethod
    def parse_data(data):
        data = data.decode()
        if not data:
            data = '{}'
        return json.loads(data)

    @staticmethod
    def validate_data(data, fields):
        for f in fields:
            if not data.get(f):
                return abort(400, f'{f} field is required!')

    @staticmethod
    def abort(message, status_code=400):
        return abort(status_code, message)

    @staticmethod
    def make_response(data):
        return json.dumps(data)

    def get(self, **kwargs):
        data = self.parse_data(self.request.data)
        self.validate_data(data, self.get_fields)
        return data

    def post(self, **kwargs):
        data = self.parse_data(self.request.data)
        self.validate_data(data, self.post_fields)
        return data

    def delete(self, **kwargs):
        data = self.parse_data(self.request.data)
        self.validate_data(data, self.post_fields)
        return data

    def put(self, **kwargs):
        data = self.parse_data(self.request.data)
        self.validate_data(data, self.post_fields)
        return data
