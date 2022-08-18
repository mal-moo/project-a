from datetime import timedelta
from http import HTTPStatus
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token

from config import app
from config.settings import JWT
from config.utils import is_validated_email, is_validated_name, is_validated_password, \
                        is_validated_phone, is_validated_nickname, err_resp_form, resp_form
from .models import *


@app.route('/user/password', methods=["PUT"])
@jwt_required()
def user_password():
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

    # 파라미터 검증
    if not is_validated_password(password) or not is_validated_email(email):
        return err_resp_form(HTTPStatus.BAD_REQUEST, 'Invalid Paramaters')

    # 기가입자 고객인지 확인
    is_suc, user_info = select_user_by_email(email)
    if not is_suc:
        return err_resp_form(HTTPStatus.INTERNAL_SERVER_ERROR, 'Internal Server Error')
    if not user_info:
        return err_resp_form(HTTPStatus.FORBIDDEN, 'Forbbiden')

    # 기존 비밀번호랑 같은지 확인
    is_suc, user_info = select_user_by_email_and_password(email, password)
    if not is_suc:
        return err_resp_form(HTTPStatus.INTERNAL_SERVER_ERROR, 'Internal Server Error')
    if user_info:
        return err_resp_form(HTTPStatus.UNPROCESSABLE_ENTITY, 'Duplicated')
    
    is_suc = update_user_by_password(email, password)
    if not is_suc:
        return err_resp_form(HTTPStatus.INTERNAL_SERVER_ERROR, 'Internal Server Error')

    return resp_form(HTTPStatus.OK, '')


@app.route('/signup', methods=["POST"])
@jwt_required()
def sign_up():
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

    is_suc, err_code = insert_user(email, password, name, nickname, phone)
    
    if not is_suc:
        if err_code == 1062:
            return err_resp_form(HTTPStatus.UNPROCESSABLE_ENTITY, 'Duplicated')
        else:
            return err_resp_form(HTTPStatus.INTERNAL_SERVER_ERROR, 'Internal Server Error')

    return resp_form(HTTPStatus.CREATED, '')
    

@app.route("/login", methods=['POST'])
def login():
    try:
        email = request.form['email']
        password = request.form['password']
    except KeyError:
        return err_resp_form(HTTPStatus.BAD_REQUEST, 'Missing Paramaters')

    if not is_validated_email(email):
        return err_resp_form(HTTPStatus.BAD_REQUEST, 'Invalid Paramaters')

    is_suc, user_info = select_user_by_email_and_password(email, password)
    if not is_suc:
        return err_resp_form(HTTPStatus.INTERNAL_SERVER_ERROR, 'Internal Server Error')
    if not user_info:
        return err_resp_form(HTTPStatus.FORBIDDEN, 'Forbbiden')
    
    access_token = create_access_token(identity = {'user_id': user_info['user_id']},
                                        expires_delta = timedelta(minutes=JWT['EXPIRES_IN']['USER']))
    return resp_form(HTTPStatus.OK, {
        'access_token': access_token
    })
    

@app.route('/user', methods=["GET"])
@jwt_required()
def user_info():
    jwt_identity = get_jwt_identity()
    if not jwt_identity or not 'user_id' in jwt_identity:
        return err_resp_form(HTTPStatus.FORBIDDEN, 'Forbbiden')
    
    user_id = jwt_identity['user_id']
    is_suc, user_info = select_user_by_id(user_id)
    if not is_suc:
        return err_resp_form(HTTPStatus.INTERNAL_SERVER_ERROR, 'Internal Server Error')
    if not user_info:
        return err_resp_form(HTTPStatus.FORBIDDEN, 'Forbbiden')

    user_info.pop('password')
    user_info.pop('user_id')
    
    return resp_form(HTTPStatus.OK, user_info)