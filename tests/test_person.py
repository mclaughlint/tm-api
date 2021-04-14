"""
Endpoint tests.
TODO: add pytest-docker-compose and spin up/tear down new containers for testing on separate db
"""
import random
import requests


FIELDS = ['age', 'email', 'first_name', 'id', 'last_name', 'meta_create_ts', 'middle_name', 'version']


def get_sample_id():
    """
    Get first UUID from persons endpoint
    :return: sample_uuid (string)
    """
    response = requests.get('http://localhost:5000/api/persons')
    data = response.json()
    sample_uuid = data[0]['id']

    return sample_uuid


def test_fetch_all():
    """
    Test fetch all persons endpoint
    :return:
    """
    response = requests.get('http://localhost:5000/api/persons')
    data = response.json()

    assert response.status_code == 200
    for field in FIELDS:
        assert field in data[0]


def test_fetch_one():
    """
    Test fetch single person endpoint
    :return:
    """
    sample_uuid = get_sample_id()
    response = requests.get(f'http://localhost:5000/api/persons/{sample_uuid}')
    data = response.json()

    assert response.status_code == 200
    for field in FIELDS:
        assert field in data


def test_fetch_one_version():
    """
    Test fetch specific version of one person endpoint
    :return:
    """
    sample_uuid = get_sample_id()
    version = 1
    response = requests.get(f'http://localhost:5000/api/persons/{sample_uuid}/{version}')
    data = response.json()

    assert response.status_code == 200
    for field in FIELDS:
        assert field in data


def test_create():
    """
    Test create a new person endpoint
    :return:
    """
    test_person = {
        "age": random.randint(0, 99),
        "email": "test@gmail.com",
        "first_name": "Ben",
        "last_name": "Stiller",
        "middle_name": "James"
    }
    response = requests.post('http://localhost:5000/api/persons', json=test_person)
    data = response.json()

    assert response.status_code == 201
    for field in FIELDS:
        assert field in data


def test_update():
    """
    Test updating an existing person
    :return:
    """
    payload = {'age': 99}
    sample_uuid = get_sample_id()
    response = requests.put(f'http://localhost:5000/api/persons/{sample_uuid}', json=payload)
    data = response.json()

    assert response.status_code == 200
    for field in FIELDS:
        assert field in data


def test_delete():
    """
    Test deleting an existing person
    :return:
    """
    sample_uuid = get_sample_id()
    response = requests.delete(f'http://localhost:5000/api/persons/{sample_uuid}')

    assert response.status_code == 200
