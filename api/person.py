from flask import make_response, abort
from config import db
from models import Person, PersonSchema, PersonAudit, PersonAuditSchema


def fetch_all():
    """
    This function responds to a GET request for /api/persons
    with the complete lists of persons
    :return:        sorted list of persons
    """
    persons = Person.query.order_by(Person.last_name).all()
    person_schema = PersonSchema(many=True)

    return person_schema.dump(persons)


def fetch_one(id):
    """
    This function responds to a GET request for /api/persons/{id}
    with one matching person
    :param id:   ID of person to fetch
    :return:        person matching ID
    """
    person = Person.query \
        .filter(Person.id == id) \
        .one_or_none()

    if person is not None:
        person_schema = PersonSchema()
        return person_schema.dump(person)
    else:
        abort(404, f'Person not found for Id: {id}')


def fetch_one_version(id, version):
    """
    This function responds to a GET request for /api/persons/{id}/{version}
    with one specific version record of a matching person
    :param id:      ID of person to fetch
    :param version: version ID of record to fetch
    :return:        person matching ID and version
    """
    # check if they're looking for the latest version
    person = Person.query \
        .filter(Person.id == id) \
        .filter(Person.version == version) \
        .one_or_none()

    # return latest version
    if person is not None:
        person_schema = PersonSchema()
        return person_schema.dump(person)
    else:
        # check if the version exists in person_audit table
        person_version = PersonAudit.query \
            .with_entities(PersonAudit.person_id.label('id'), PersonAudit.first_name, PersonAudit.middle_name,
                           PersonAudit.last_name, PersonAudit.email, PersonAudit.age, PersonAudit.meta_create_ts,
                           PersonAudit.version) \
            .filter(PersonAudit.person_id == id) \
            .filter(PersonAudit.version == version) \
            .one_or_none()

        # return version
        if person_version is not None:
            person_audit_schema = PersonAuditSchema()
            return person_audit_schema.dump(person_version)
        else:
            abort(404, f'Record not found for Id: {id}, Version: {version}')


def create(person):
    """
    This function creates a new person in the persons database
    based on the passed in person data
    :param person:  person to create in persons structure
    :return:        201 on success, 406 on person already exists
    """
    first_name = person.get('first_name')
    last_name = person.get ('last_name')
    email = person.get('email')
    age = person.get('age')

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
    else:
        abort(
            409,
            f"Person with name {first_name} {last_name} already exists"
        )


def update(id, person):
    """
    This function updates an existing person in the persons database
    :param id:   ID of person to update in the persons database
    :param person:  person data to update
    :return:        updated person structure
    """
    # Get the person from the db
    update_person = Person.query.filter(
        Person.id == id
    ).one_or_none()

    # Abort if we can't find the person
    if update_person is None:
        abort(
            404,
            f"Person not found for Id: {id}",
        )

    # turn the passed in person into a db object
    person_schema = PersonSchema()
    update = person_schema.load(person, session=db.session)

    # Set the id to the person we want to update
    update.id = update_person.id

    # merge the new object into the old and commit it to the db
    db.session.merge(update)
    db.session.commit()

    # return updated person in the response
    data = person_schema.dump(update_person)

    return data, 200


def delete(id):
    """
    This function deletes a person from the persons database
    :param id:   ID of person to delete
    :return:     200 on successful delete, 404 if not found
    """
    # Get the person requested
    person = Person.query.filter(Person.id == id).one_or_none()

    if person is not None:
        db.session.delete(person)
        db.session.commit()
        return make_response(
            f"Person {id} deleted", 200
        )

    # Couldn't find person
    else:
        abort(
            404,
            f"Person not found for Id: {id}",
        )
