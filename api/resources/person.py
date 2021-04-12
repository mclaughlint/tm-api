from datetime import datetime
from flask import make_response, abort


def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# Data to serve with our API
persons = {
    "Farrell": {
        "fname": "Doug",
        "lname": "Farrell",
        "timestamp": get_timestamp()
    },
    "Brockman": {
        "fname": "Kent",
        "lname": "Brockman",
        "timestamp": get_timestamp()
    },
    "Easter": {
        "fname": "Bunny",
        "lname": "Easter",
        "timestamp": get_timestamp()
    }
}


def fetch_all():
    """
    This function responds to a request for /api/persons
    with the complete lists of persons
    :return:        sorted list of persons
    """

    return [persons[key] for key in sorted(persons.keys())]


def fetch_one(lname):
    """
    This function responds to a request for /api/persons/{lname}
    with one matching person
    :param lname:   last name of person to find
    :return:        person matching last name
    """
    # Check if person exists already
    if lname in persons:
        person = persons.get(lname)
        return person
    else:
        abort(
            404, f"Person with last name {lname} not found"
        )


def create(person):
    """
    This function creates a new person in the persons database
    based on the passed in person data
    :param person:  person to create in persons structure
    :return:        201 on success, 406 on person already exists
    """
    lname = person.get("lname", None)
    fname = person.get("fname", None)

    # Check if person exists already
    if lname not in persons and lname is not None:
        persons[lname] = {
            "lname": lname,
            "fname": fname,
            "timestamp": get_timestamp(),
        }
        return make_response(
            f"{lname} successfully created", 201
        )
    else:
        abort(
            406,
            f"Person with last name {lname} already exists"
        )


def update(lname, person):
    """
    This function updates an existing person in the persons database
    :param lname:   last name of person to update in the persons database
    :param person:  person to update
    :return:        updated person structure
    """
    # Check if person exists already
    if lname in persons:
        persons[lname]["fname"] = person.get("fname")
        persons[lname]["timestamp"] = get_timestamp()

        return person[lname]
    else:
        abort(
            404, f"Person with last name {lname} not found"
        )


def delete(lname):
    """
    This function deletes a person from the persons database
    :param lname:   last name of person to delete
    :return:        200 on successful delete, 404 if not found
    """
    # Does the person to delete exist?
    if lname in persons:
        del persons[lname]
        return make_response(
           f"{lname} successfully deleted", 200
        )
    else:
        abort(
            404, f"Person with last name {lname} not found"
        )