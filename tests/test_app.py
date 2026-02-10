from http import HTTPStatus

from fast_project.squemas import UserPublic


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


def test_created_user_already_exists(client, user):

    client.post(
        '/users/',
        json={
            'username': 'bob',
            'email': 'bob@gmail.com',
            'password': '123s',
        },
    )

    response = client.post(
        '/users/',
        json={
            'username': 'bob',
            'email': 'bob1234@gmail.com',
            'password': '123s',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Username already exists'}


def test_created_email_already_exists(client, user):

    client.post(
        '/users/',
        json={
            'username': 'bob_bondoso',
            'email': 'bob@gmail.com',
            'password': '123s',
        },
    )

    response = client.post(
        '/users/',
        json={
            'username': 'bob',
            'email': 'bob@gmail.com',
            'password': '123s',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Email already exists'}


def test_read_users_with_users(client, user, token):

    user_squema = UserPublic.model_validate(user).model_dump()

    response = client.get(
        '/users/', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.json() == {'user': [user_squema]}


def test_update_user(client, user, token):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
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


def test_update_user_not_found(client, user, token):
    response = client.put(
        '/users/999',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'test',
            'email': 'test@gmail.com',
            'password': '1234',
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_update_integrity_error(client, user, token):

    client.post(
        '/users/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'test',
            'email': 'test@gmail.com',
            'password': '1234',
        },
    )

    response_update = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'test',
            'email': 'bob@gmail.com',
            'password': '12345',
        },
    )

    assert response_update.status_code == HTTPStatus.CONFLICT
    assert response_update.json() == {
        'detail': 'username or email already exists'
    }


def test_delete_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}', headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'user deleted'}


def test_get_token(client, user):

    response = client.post(
        '/login',
        data={'username': user.email, 'password': user.clean_password},
    )

    token = response.json()
    assert response.status_code == HTTPStatus.OK
    assert token['token_type'] == 'Bearer'
    assert 'access_token' in token
