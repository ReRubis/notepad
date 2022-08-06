import requests


def test_create_new_notepad(random_string):
    url = 'http://127.0.0.1:5000/api/notepad'
    payload = {
        'name': random_string,
        'text': random_string,
    }

    resp = requests.post(url, json=payload)
    assert resp.ok
    resp_json = resp.json()

    print(payload)

    assert resp_json['name'] == payload['name']
    assert resp_json['text'] == payload['text']


def test_get_notepad(random_string):
    # create new notepad
    url = 'http://127.0.0.1:5000/api/notepad'
    payload = {
        'name': random_string,
        'text': random_string,
    }

    resp = requests.post(url, json=payload)
    assert resp.ok
    resp_of_creation_json = resp.json()

    # get the just created notepad
    url = f"http://127.0.0.1:5000/api/notepad/{resp_of_creation_json['id']}"

    resp = requests.get(url)
    assert resp.ok
    resp_json = resp.json()

    print(payload)

    assert resp_json['name'] == payload['name']
    assert resp_json['text'] == payload['text']


def test_delete_notepad(random_string):
    # create new notepad
    url = 'http://127.0.0.1:5000/api/notepad'
    payload = {
        'name': random_string,
        'text': random_string,
    }

    resp = requests.post(url, json=payload)
    assert resp.ok
    resp_of_creation_json = resp.json()

    # delete the just created notepad
    url = f"http://127.0.0.1:5000/api/notepad/delete/{resp_of_creation_json['id']}"

    resp = requests.get(url)
    assert resp.ok