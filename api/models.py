"""
SQLAlchemy and Marshmallow Models
for storing, retrieving, serializing, deserializing Person data
"""
from datetime import datetime
from config import db
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy.dialects.postgresql import UUID


class Person(db.Model):
    """
    api.person SQLAlchemy model
    """
    __tablename__ = "person"
    __table_args__ = {'schema': 'api'}
    id = db.Column(UUID(as_uuid=True), primary_key=True, server_default=db.text("uuid_generate_v4()"))
    first_name = db.Column(db.String)
    middle_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String)
    age = db.Column(db.Integer)
    meta_create_ts = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    version = db.Column(db.Integer)


class PersonSchema(SQLAlchemyAutoSchema):
    """
    api.person marshmallow model
    """
    class Meta:
        model = Person
        load_instance = True


class PersonAudit(db.Model):
    """
    api.person_audit SQLAlchemy model
    """
    __tablename__ = "person_audit"
    __table_args__ = {'schema': 'api'}
    id = db.Column(db.Integer, primary_key=True)
    stamp = db.Column(db.DateTime)
    db_user_id = db.Column(db.String)
    deleted = db.Column(db.Boolean)
    person_id = db.Column(db.Integer)
    first_name = db.Column(db.String)
    middle_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String)
    age = db.Column(db.Integer)
    meta_create_ts = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    version = db.Column(db.Integer)


class PersonAuditSchema(SQLAlchemyAutoSchema):
    """
    api.person_audit marshmallow model
    """
    class Meta:
        model = PersonAudit
        load_instance = True
