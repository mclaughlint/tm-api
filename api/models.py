from datetime import datetime
from config import db
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


class Person(db.Model):
    __tablename__ = "person"
    __table_args__ = {'schema': 'api'}
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    middle_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String)
    age = db.Column(db.Integer)
    meta_create_ts = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )


class PersonSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Person
        load_instance = True
