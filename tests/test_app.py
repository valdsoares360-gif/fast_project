from http import HTTPStatus


def test_read_root_must_return_ok_and_hello_world(client):

    response = client.get('/')

    assert response.status_code == HTTPStatus.OK

    assert response.json() == {'message': 'hello world'}


def test_text(client):
    response = client.get('/teste')
    assert response.status_code == HTTPStatus.OK
    assert response.text == '<h1>test ok</h1>'


def teste_create_user(client):

    response = client.post(
        '/users/',
        json={
            'username': 'bob',
            'email': 'bob@gmail.com',
            'password': '123s',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'username': 'bob',
        'email': 'bob@gmail.com',
    }


def test_read(client):
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'user': [{'id': 1, 'username': 'bob', 'email': 'bob@gmail.com'}]
    }


def test_update_user(client):
    response = client.put(
        '/users/1',
        json={
            'username': 'alice',
            'email': 'alice@gmail.com',
            'password': '1234',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'alice',
        'email': 'alice@gmail.com',
        'id': 1,
    }


def test_delete_user(client):
    response = client.delete('/users/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'alice',
        'email': 'alice@gmail.com',
        'id': 1,
    }
