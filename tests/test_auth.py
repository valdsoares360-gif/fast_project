from http import HTTPStatus

from freezegun import freeze_time


def test_get_token(client, user):

    response = client.post(
        '/auth/login',
        data={'username': user.email, 'password': user.clean_password},
    )

    token = response.json()
    assert response.status_code == HTTPStatus.OK
    assert token['token_type'] == 'Bearer'
    assert 'access_token' in token


def test_token_wrong_user(client, user):
    response = client.post(
        'auth/login',
        data={'username': user.email, 'password': 'testepassword'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'incorrect email or password '}


def test_token_wrong_email(client, user):
    response = client.post(
        'auth/login',
        data={'username': 'inexistent@email.com', 'password': 'test'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'incorrect email or password '}


def test_token_expired_after_time(client, user):

    with freeze_time('2026-01-11 12:00:00'):
        response = client.post(
            'auth/login',
            data={'username': user.email, 'password': 'bobaqui'},
        )

    assert response.status_code == HTTPStatus.OK
    token = response.json()['access_token']

    with freeze_time('2026-01-11 12:31:00'):
        response = client.put(
            f'/users/{user.id}',
            headers={'Authorization': f'bearer {token}'},
            json={
                'username': 'wrong_user',
                'email': 'testar1234@example.com',
                'password': '1234',
            },
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {'detail': 'could not validate credentials'}


def test_refresh_token(client, token):
    response = client.post(
        '/auth/refresh_token',
        headers={'Authorization': f'bearer {token}'},
    )

    data = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in data
    assert 'token_type' in data
    assert data['token_type'] == 'bearer'


def test_token_expired_dont_refresh(client, user):
    with freeze_time('2026-01-11 12:00:00'):
        response = client.post(
            '/auth/login',
            data={'username': user.email, 'password': user.clean_password},
        )

        assert response.status_code == HTTPStatus.OK
        token = response.json()['access_token']

    with freeze_time('2026-01-11 12:31:00'):
        response = client.post(
            '/auth/refresh_token',
            headers={'Authorization': f'Bearer {token}'},
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {'detail': 'could not validate credentials'}
