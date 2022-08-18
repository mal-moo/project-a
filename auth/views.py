from datetime import datetime, timedelta
from flask import request
from flask_jwt_extended import create_access_token
from http import HTTPStatus

from config import app
from config.settings import JWT
from config.utils import is_validated_phone, make_auth_code, call_sms_submit_api, \
                        resp_form, err_resp_form
from .models import *


@app.route('/auth', methods=['POST', 'GET'])
def auth_phone():
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
        if is_suc:
            success = call_sms_submit_api()
            if success:
                return resp_form(HTTPStatus.CREATED, '')
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
        
        if is_suc:
            if (datetime.now() - auth_info['create_date']).total_seconds() < 300:
                access_token = create_access_token(identity = {'is_auth': True},
                                                expires_delta = timedelta(minutes=JWT['EXPIRES_IN']['AUTH']))
                return resp_form(HTTPStatus.CREATED, {
                    'access_token': access_token
                })
            else:
                return err_resp_form(HTTPStatus.UNAUTHORIZED, 'Authcode has been revoked')
