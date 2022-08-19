import pytest
from flask_jwt_extended import create_access_token
from config import app


@pytest.fixture
def client():
    return app.test_client()


def test_user_password(client):
    with app.app_context():
        access_token = create_access_token({'is_auth': True})
        headers = {
            'Authorization': 'Bearer {}'.format(access_token)
        }
        resp = client.put('/user/password', 
                        data={
                            'email': 'malmoo3@gmail.com', 
                            'password': 'Rhdwldms2!1'
                        }, 
                        headers=headers
                    )
        assert resp.status_code == 200
        assert resp.json['msg'] == 'success'


def test_sign_up(client):
    with app.app_context():
        access_token = create_access_token({'is_auth': True})
        headers = {
            'Authorization': 'Bearer {}'.format(access_token)
        }

        resp = client.post('/signup',
                            data={
                                'name':'홍길동', 
                                'nickname': '길동이', 
                                'phone': '01012341234',
                                'email': 'honggildong@gmail.com', 
                                'password': 'Password1!'
                            }, 
                            headers=headers
                        )

        assert resp.status_code == 201
        assert resp.json['msg'] == 'success'


def test_login(client):
    resp = client.post('/login',
                        data={
                            'email': 'honggildong@gmail.com', 
                            'password': 'Password1!'
                        }, 
                    )

    assert resp.status_code == 200
    assert resp.json['msg'] == 'success'


def test_user(client):
     with app.app_context():
        access_token = create_access_token({'user_id': 1})
        headers = {
            'Authorization': 'Bearer {}'.format(access_token)
        }
        resp = client.get('/user', headers=headers)

        assert resp.status_code == 200
        assert resp.json['msg'] == 'success'

