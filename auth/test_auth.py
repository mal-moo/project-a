import pytest
from config import app


@pytest.fixture
def client():
    return app.test_client()


def test_auth_post(client):
    resp = client.post('/auth', data={'phone': '01012341234'})
    assert resp.status_code == 201
    assert resp.json['msg'] == 'success'


def test_auth_get(client):
    resp = client.get('/auth?phone=01012341234&code=2753')
    assert resp.status_code == 200
    assert resp.json['msg'] == 'success'


def test_auth_bad_http_method(client):
    resp = client.put('/auth')
    assert resp.status_code == 405


def test_auth_post_no_form_body(client):
    resp = client.post('/auth', json='something')
    assert resp.status_code == 400
    assert resp.json.get('msg')


def test_auth_get_no_params(client):
    resp = client.get('/auth', data={'phone': '01012341234', 'code': 1234})
    assert resp.status_code == 400
    assert resp.json.get('msg')
    

def test_auth_post_missing_parameter(client):
    resp = client.post('/auth', data={})
    assert resp.status_code == 400
    assert resp.json.get('msg')


def test_auth_get_missing_parameter(clint):
    resp = client.get('/auth')
    assert resp.status_code == 400
    assert resp.json.get('msg')
