from http import HTTPStatus

from fastapi.testclient import TestClient

from fast_project.app import app


def test_read_root_must_return_ok_and_hello_world():
    client = TestClient(app)  # arrange(organizaçao)

    response = client.get('/')  # act(agir)

    assert response.status_code == HTTPStatus.OK  # assert(garantir)

    assert response.json() == {'message': 'hello world'}
