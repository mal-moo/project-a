import pytest
from config import DBConnector, app


@pytest.fixture
def client():
    return app.test_client()


def test_auth_post(client):
    resp = client.post('/auth', data={'phone': '01012341234'})
    assert resp.status_code == 201
    assert resp.json['msg'] == 'success'


def test_auth_get(client):
    # select auth code from db
    dc = DBConnector()
    conn = dc.connection
    with conn.cursor() as curs:
        sql = 'SELECT auth_code FROM auth_phone WHERE phone = %s;'
        curs.execute(sql, ('01012341234',))
        result = curs.fetchone()
        print(result)

    resp = client.get('/auth?phone=01012341234&code={}'.format(result['auth_code']))
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


def test_auth_get_missing_parameter(client):
    resp = client.get('/auth')
    assert resp.status_code == 400
    assert resp.json.get('msg')
