from http import HTTPStatus

from jwt import decode

from fast_project.security import ALGORITHM, SECRET_KEY, create_access_token


def test_jwt():
    claim = {'test': 'test'}

    token = create_access_token(claim)

    decoded = decode(token, SECRET_KEY, algorithms=ALGORITHM)

    assert decoded['test'] == claim['test']
    assert 'exp' in decoded


def test_jwt_invalid_token(client):
    response = client.delete(
        '/users/1', headers={'Authorization': 'bearer token-invalid'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'could not validate credentials'}


def test_email_does_not_exists(client):
    data = {'no-email': 'test'}
    token = create_access_token(data)

    response = client.delete(
        '/users/1',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'could not validate credentials'}


def test_get_current_user_does_not_exists__exercicio(client):
    data = {'sub': 'test@test'}
    token = create_access_token(data)

    response = client.delete(
        '/users/1',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'could not validate credentials'}
