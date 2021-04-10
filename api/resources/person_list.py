from flask_restful import Resource, fields, marshal_with

user_fields = {
    'id': fields.Integer,
    'first_name': fields.String,
    'middle_name': fields.String,
    'last_name': fields.String,
    'email': fields.String,
    'age': fields.Integer,
    'meta_create_ts': fields.DateTime,
    'meta_update_ts': fields.DateTime,
}


class PersonList(Resource):
    def get(self):
        pass

    def post(self):
        pass