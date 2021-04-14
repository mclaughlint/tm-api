"""
Methods for handling CRUD actions on Person objects
"""
import logging

import sqlalchemy.exc
from flask import make_response, abort
from config import db
from models import Person, PersonSchema, PersonAudit, PersonAuditSchema


def fetch_all():
    """
    This function responds to a GET request for /api/persons
    with the complete lists of persons
    :return: sorted list of persons
    """
    try:
        persons = Person.query.order_by(Person.last_name).all()
        person_schema = PersonSchema(many=True)

        return person_schema.dump(persons)
    except sqlalchemy.exc.SQLAlchemyError as e:
        logging.error(f'SQLAlchemyError: {e}')


def fetch_one(person_id):
    """
    This function responds to a GET request for /api/persons/{id}
    with one matching person
    :param person_id:   UUID of person to fetch
    :return:            person matching ID
    """
    try:
        person = Person.query \
            .filter(Person.id == person_id) \
            .one_or_none()

        if person is None:
            abort(404, f'Person not found for Id: {person_id}')

        person_schema = PersonSchema()
        return person_schema.dump(person)

    except sqlalchemy.exc.SQLAlchemyError as e:
        logging.error(f'SQLAlchemyError: {e}')


def fetch_one_version(person_id, version):
    """
    This function responds to a GET request for /api/persons/{id}/{version}
    with one specific version record of a matching person
    :param person_id:      ID of person to fetch
    :param version: version ID of record to fetch
    :return:        person matching ID and version
    """
    try:
        # check if they're looking for the latest version
        person = Person.query \
            .filter(Person.id == person_id) \
            .filter(Person.version == version) \
            .one_or_none()

        # return latest version
        if person is not None:
            person_schema = PersonSchema()
            return person_schema.dump(person)

        # check if the version exists in person_audit table
        person_version = PersonAudit.query \
            .with_entities(PersonAudit.person_id.label('id'), PersonAudit.first_name, PersonAudit.middle_name,
                           PersonAudit.last_name, PersonAudit.email, PersonAudit.age, PersonAudit.meta_create_ts,
                           PersonAudit.version) \
            .filter(PersonAudit.person_id == person_id) \
            .filter(PersonAudit.version == version) \
            .one_or_none()

        # return version
        if person_version is not None:
            person_audit_schema = PersonAuditSchema()
            return person_audit_schema.dump(person_version)

        abort(404, f'Record not found for Id: {person_id}, Version: {version}')
    except sqlalchemy.exc.SQLAlchemyError as e:
        logging.error(f'SQLAlchemyError: {e}')


def create(person):
    """
    This function creates a new person in the persons database
    based on the passed in person data
    :param person:  person to create in persons structure
    :return:        201 on success, 409 on person already exists
    """
    first_name = person.get('first_name')
    last_name = person.get('last_name')
    email = person.get('email')
    age = person.get('age')

    try:
        # Check if person exists already
        existing_person = Person.query \
            .filter(Person.first_name == first_name) \
            .filter(Person.last_name == last_name) \
            .filter(Person.email == email) \
            .filter(Person.age == age) \
            .one_or_none()

        if existing_person is None:
            person_schema = PersonSchema()
            new_person = person_schema.load(person, session=db.session)
            db.session.add(new_person)
            db.session.commit()

            data = person_schema.dump(new_person)
            return data, 201

        abort(409, f"Person with name {first_name} {last_name} already exists")
    except sqlalchemy.exc.SQLAlchemyError as e:
        logging.error(f'SQLAlchemyError: {e}')


def update(person_id, person):
    """
    This function updates an existing person in the persons database
    :param person_id:   ID of person to update in the persons database
    :param person:  person data to update
    :return:        updated person structure
    """
    # Get the person from the db
    update_person = Person.query.filter(
        Person.id == person_id
    ).one_or_none()

    # Abort if we can't find the person
    if update_person is None:
        abort(
            404,
            f"Person not found for Id: {person_id}",
        )

    # turn the passed in person into a db object
    person_schema = PersonSchema()
    updater = person_schema.load(person, session=db.session)

    # Set the id to the person we want to update
    updater.id = update_person.id

    # merge the new object into the old and commit it to the db
    db.session.merge(updater)
    db.session.commit()

    # return updated person in the response
    data = person_schema.dump(update_person)

    return data, 200


def delete(person_id):
    """
    This function deletes a person from the persons database
    :param person_id:   ID of person to delete
    :return:     200 on successful delete, 404 if not found
    """
    try:
        # Get the person requested
        person = Person.query.filter(Person.id == person_id).one_or_none()

        if person is not None:
            db.session.delete(person)
            db.session.commit()
            return make_response(
                f"Person {person_id} deleted", 200
            )

        # Couldn't find person
        abort(404, f"Person not found for Id: {person_id}")
    except sqlalchemy.exc.SQLAlchemyError as e:
        logging.error(f'SQLAlchemyError: {e}')
