from flask import Flask
from flask_restful import Api
from api.resources.person import Person
from api.resources.person_list import PersonList

app = Flask(__name__)
api = Api(app)

api.add_resource(Person, '/person', '/person/<string:id>')
api.add_resource(PersonList, '/person/fetch-all')

if __name__ == '__main__':
    app.run(debug=True)
