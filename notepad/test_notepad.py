import requests


def test_user_registration(random_string):
    url = 'http://127.0.0.1:5000/api/notepad/registration'
    payload = {
        'login': random_string,
        'password': random_string,
    }
    resp = requests.post(url, json=payload)
    assert resp.ok


def test_user_registration_same_login(random_string):
    # create new notepad
    url = 'http://127.0.0.1:5000/api/notepad/registration'
    payload = {
        'login': random_string,
        'password': random_string,
    }

    resp = requests.post(url, json=payload)
    assert resp.ok

    # get the just created notepad
    url = 'http://127.0.0.1:5000/api/notepad/registration'

    resp = requests.post(url, json=payload)
    assert resp.ok


def test_user_login(random_string):
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


def test_create_new_notepad(random_string, get_jwt):
    url = 'http://127.0.0.1:5000/api/notepad'
    payload = {
        'name': random_string,
        'text': random_string,
        'jwt': get_jwt,
    }

    resp = requests.post(url, json=payload)
    assert resp.ok
    resp_json = resp.json()

    assert resp_json['name'] == payload['name']
    assert resp_json['text'] == payload['text']


def test_get_notepad(random_string, get_jwt):
    # create new notepad
    url = 'http://127.0.0.1:5000/api/notepad'
    payload = {
        'name': random_string,
        'text': random_string,
        'jwt': get_jwt,
    }

    resp = requests.post(url, json=payload)
    assert resp.ok
    resp_of_creation_json = resp.json()

    # get the just created notepad
    url = f"http://127.0.0.1:5000/api/notepad/{resp_of_creation_json['id']}"

    payload_jwt = {
        'jwt': get_jwt,
    }
    resp = requests.get(url, json=payload_jwt)
    assert resp.ok
    resp_json = resp.json()

    assert resp_json['name'] == payload['name']
    assert resp_json['text'] == payload['text']


def test_delete_notepad(random_string, get_jwt):
    # create new notepad
    url = 'http://127.0.0.1:5000/api/notepad'
    payload = {
        'name': random_string,
        'text': random_string,
        'jwt': get_jwt,
    }

    resp = requests.post(url, json=payload)
    assert resp.ok
    resp_json = resp.json()

    assert resp_json['name'] == payload['name']
    assert resp_json['text'] == payload['text']

    print(resp_json['id'])

    # delete the just created notepad
    url = f"http://127.0.0.1:5000/api/notepad/delete/{resp_json['id']}"
    print(url)
    payload_jwt = {
        'jwt': get_jwt,
    }
    print(payload_jwt)
    resp = requests.post(url, json=payload_jwt)
    assert resp.ok
