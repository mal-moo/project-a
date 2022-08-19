from http import HTTPStatus
from flask import request, Response
from flask_jwt_extended import jwt_required, get_jwt_identity

from config import app
from common.utils import is_validated_email, is_validated_name, is_validated_password, \
                        is_validated_phone, is_validated_nickname, err_resp_form
from .services import *


@app.route('/user/password', methods=["PUT"])
@jwt_required()
def user_password() -> tuple[Response, int]:
    """
    This is rest password API
    ---
    tags:
      - Reset Password API
    ---
    parameters:
      - name: email
        in: form
        type: str
        required: True
        example: honggildong@gmail.com
      - name: password
        in: form
        type: str
        required: True
        example: mypassword!1
    responses:
      500:
        description: 'Internal Server Error'
      422:
        description: 'Duplicated'
      403:
        description: 'Forbbiden'
      401:
        description:  'Unauthorized'
      400:
        description: 1. 'Missing Paramaters'
                     2. 'Invalid Parameters'
      200:
        description: Successful reset password
        schema:
          {
            'msg': 'success',
            'data': {}
          }
    """
    jwt_identity = get_jwt_identity()
    if jwt_identity and 'is_auth' in jwt_identity:
        if not jwt_identity['is_auth']:
            return err_resp_form(HTTPStatus.FORBIDDEN, 'Forbbiden')
    else:
        return err_resp_form(HTTPStatus.FORBIDDEN, 'Forbbiden')

    try:
        email = request.form['email']
        password = request.form['password']
    except KeyError:
        return err_resp_form(HTTPStatus.BAD_REQUEST, 'Missing Paramaters')

    if not is_validated_password(password) or not is_validated_email(email):
        return err_resp_form(HTTPStatus.BAD_REQUEST, 'Invalid Paramaters')

    return reset_user_password_service(email, password)


@app.route('/signup', methods=["POST"])
@jwt_required() 
def sign_up() -> tuple[Response, int]:
    """
    This is User Signup API
    ---
    tags:
      - Sign up API
    ---
    parameters:
      - name: email
        in: form
        type: str
        required: True
        example: honggildong@gmail.com
      - name: password
        in: form
        type: str
        required: True
        example: mypassword!1
      - name: name
        in: form
        type: str
        required: True
        example: 홍길동
      - name: nickname
        in: form
        type: str
        required: True
        example: 길동이
      - name: phone
        in: form
        type: str
        required: True
        description: phone number
        example: 01012341234
    responses:
      500:
        description: 'Internal Server Error'
      422:
        description: 'Duplicated'
      403:
        description: 'Forbbiden'
      400:
        description: 1. 'Missing Paramaters'
                     2. 'Invalid Parameters'
      201:
        description: Successful sign up
        schema:
          {
            'msg': 'success',
            'data': {}
          }
    """
    jwt_identity = get_jwt_identity()
    if jwt_identity and 'is_auth' in jwt_identity:
        if not jwt_identity['is_auth']:
            return err_resp_form(HTTPStatus.FORBIDDEN, 'Forbbiden')
    else:
        return err_resp_form(HTTPStatus.FORBIDDEN, 'Forbbiden')

    try:
        email = request.form['email']
        password = request.form['password']
        name = request.form['name']
        nickname = request.form['nickname']
        phone = request.form['phone']
    except KeyError:
        return err_resp_form(HTTPStatus.BAD_REQUEST, 'Missing Paramaters')

    if not is_validated_password(password) or not is_validated_email(email) \
        or not is_validated_phone(phone) or not is_validated_name(name) \
        or not is_validated_nickname(nickname):
        return err_resp_form(HTTPStatus.BAD_REQUEST, 'Invalid Paramaters')

    return user_sign_up_service(email, password, name, nickname, phone)
    

@app.route("/login", methods=['POST'])
def login() -> tuple[Response, int]:
    """
    This is User login API
    ---
    tags:
      - Login API
    ---
    parameters:
      - name: email
        in: form
        type: str
        required: True
        example: honggildong@gmail.com
      - name: password
        in: form
        type: str
        required: True
        example: mypassword!1
      responses:
      500:
        description: 'Internal Server Error'
      403:
        description: 'Forbbiden'
      400:
        description: 1. 'Missing Paramaters'
                     2. 'Invalid Parameters'
      200:
        description: Successful login
        schema:
          {
            'msg': 'success',
            'data': {
                'access_token': 'my.access.token'
          }
    """
    try:
        email = request.form['email']
        password = request.form['password']
    except KeyError:
        return err_resp_form(HTTPStatus.BAD_REQUEST, 'Missing Paramaters')

    if not is_validated_email(email):
        return err_resp_form(HTTPStatus.BAD_REQUEST, 'Invalid Paramaters')

    return user_login_service(email, password)


@app.route('/user', methods=["GET"])
@jwt_required()
def user_info() -> tuple[Response, int]:
    """
    This is getting User's Infomation API
    ---
    tags:
      - User Info API
    ---
    headers:
      - name: Authorization
        in: headers
        type: str
        required: True
        description: jwt access token
    responses:
      500:
        description: 'Internal Server Error'
      403:
        description: 'Forbbiden'
      200:
        description: Successful get user infomation
        schema:
          {
            'msg': 'success',
            'data': {
                'email': 'honggildong@gmail.com',
                'name': '홍길동',
                'nickname': '길동이',
                'create_date': '2022-01-01 01:01:01',
                'update_date': '2022-01-01 01:01:01'
          }
    """
    jwt_identity = get_jwt_identity()
    if not jwt_identity or not 'user_id' in jwt_identity:
        return err_resp_form(HTTPStatus.FORBIDDEN, 'Forbbiden')
    
    user_id = jwt_identity['user_id']

    return user_info_service(user_id)