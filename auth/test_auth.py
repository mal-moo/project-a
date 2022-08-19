from config import app
import pytest
import json

# @pytest.fixture
# def api():
#     app.config['TEST'] = True
#     return api

@pytest.fixture
def client():
    return app.test_client()


def test_auth(client):
    resp = client.post('/auth', data={'phone': '01066383223'})
    assert resp.status_code == 201
    assert resp.json['data'] == {}


def test_auth_bad_http_method(client):
    resp = client.put('/auth')
    assert resp.status_code == 405


def test_auth_no_form_body(client):
    resp = client.post('/auth', json='something')
    assert resp.status_code == 400
    assert resp.json.get('msg')
    

def test_auth_missing_parameter(client):
    resp = client.post('/auth', data={})
    assert resp.status_code == 400
    assert resp.json.get('msg')

    resp = client.get('/auth', data={})
    assert resp.status_code == 400
    assert resp.json.get('msg')


