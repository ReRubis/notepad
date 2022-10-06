import random
import string
import requests
import pytest

RAND_STRING_LENGTH = 10
CHARACTERS_FOR_GENERATIONS = string.ascii_letters + string.digits


@pytest.fixture
def random_string():
    the_random_string = ''
    for _ in range(RAND_STRING_LENGTH):
        the_random_string += random.choice(CHARACTERS_FOR_GENERATIONS)
    return the_random_string


@pytest.fixture
def get_jwt(random_string):
    
    url = 'http://127.0.0.1:5000/api/notepad/registration'
    payload = {
        'login': random_string,
        'password': random_string,
    }
    resp = requests.post(url, json=payload)
    assert resp.ok

    url = 'http://127.0.0.1:5000/api/notepad/login'
    resp = requests.post(url, json=payload)
    assert resp.ok
    resp_of_creation_json = resp.json()
    jwt_user = resp_of_creation_json['jwt']
    return jwt_user