from flask_restful import Resource, fields, marshal_with, reqparse

post_parser = reqparse.RequestParser()
post_parser.add_argument('id', type=int, location='form', required=True, help='The person\'s ID number')
post_parser.add_argument('first_name', type=str, location='form', required=True, help='The person\'s first name')
post_parser.add_argument('middle_name', type=str, location='form', help='The person\'s middle name')
post_parser.add_argument('last_name', type=str, location='form', required=True, help='The person\'s last name')
post_parser.add_argument('email', type=str, location='form', required=True, help='The person\'s email')
post_parser.add_argument('age', type=int, location='form', required=True, help='The person\'s last name')
args = post_parser.parse_args()

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


class Person(Resource):
    def get(self):
        pass

    def post(self):
        pass