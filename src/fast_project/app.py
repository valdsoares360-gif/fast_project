from http import HTTPStatus

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from fast_project.squemas import Message

app = FastAPI(title='PROJECT!')


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'hello world'}


@app.get(
    '/teste',
    tags=['testar'],
    response_class=HTMLResponse,
)
def test_html():
    return """
    <html>
        <head>
            <title>Home</title>
        </head>
        <body>
            <h1>Hello world</h1>
        </body>
    </html>
    """
