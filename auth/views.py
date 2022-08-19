from datetime import datetime, timedelta
from http import HTTPStatus
from flask import request, Response
from flask_jwt_extended import create_access_token

from config import app
from config.settings import JWT
from common.utils import is_validated_phone, make_auth_code, call_sms_submit_api, \
                        resp_form, err_resp_form
from .models import *


@app.route('/auth', methods=['POST', 'GET'])
def auth_phone() -> tuple[Response, int]:
    """
    This is authentication of client's phone API
    ---
    tags:
      - Authentication of Phone API
    parameters:
      - name: phone
        in: query(GET), form(POST)
        type: str
        required: True
        description: phone number
        example: 01012341234
      - name: code
        in: query
        type: int
        required: True
        description: 4-digit auth code
        example: 1234
    responses:
      500:
        description: 'Internal Server Error'
      401:
        description: 1. 'Login Not Required'
                     2. 'Unauthorized'
                     3. 'Authcode has been revoked'
      400:
        description: 1. 'Missing Paramaters'
                     2. 'Invalid Parameters'
      201:
        description: Successful creation of auth code
        schema:
          {
            'msg': 'success',
            'data': {}
          }
    """
    if 'Authorization' in request.headers:
        return err_resp_form(HTTPStatus.UNAUTHORIZED, 'Login Not Required')
    
    if request.method == 'POST':
        try:
            phone = request.form['phone']
        except KeyError:
            return err_resp_form(HTTPStatus.BAD_REQUEST, 'Missing Paramaters')

        if not is_validated_phone(phone):
            return err_resp_form(HTTPStatus.BAD_REQUEST, 'Invalid Parameters')

        auth_code = make_auth_code()
        is_suc = insert_auth_code(phone, auth_code)

        if not is_suc:
            return err_resp_form(HTTPStatus.INTERNAL_SERVER_ERROR, 'Internal Server Error')
        
        success = call_sms_submit_api(phone)
        if success:
            return resp_form(HTTPStatus.CREATED, {})
        else:
            return err_resp_form(HTTPStatus.INTERNAL_SERVER_ERROR, 'Internal Server Error')
    
    elif request.method == 'GET':
        try:
            phone = request.args['phone']
            auth_code = request.args['code']
        except KeyError:
            return err_resp_form(HTTPStatus.BAD_REQUEST, 'Missing Paramaters')
    
        if not is_validated_phone(phone):
            return err_resp_form(HTTPStatus.BAD_REQUEST, 'Invalid Paramaters')

        is_suc, auth_info = select_auth_code(phone, auth_code)
        if not is_suc:
            return err_resp_form(HTTPStatus.INTERNAL_SERVER_ERROR, 'Internal Server Error')
        if not auth_info:
            return err_resp_form(HTTPStatus.UNAUTHORIZED, 'Unauthorized')
        
        if (datetime.now() - auth_info['create_date']).total_seconds() < 300:
            access_token = create_access_token(identity = {'is_auth': True},
                                            expires_delta = timedelta(minutes=JWT['EXPIRES_IN']['AUTH']))
            return resp_form(HTTPStatus.OK, {
                'access_token': access_token
            })
        else:
            return err_resp_form(HTTPStatus.UNAUTHORIZED, 'Authcode has been revoked')
