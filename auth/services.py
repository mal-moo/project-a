from datetime import datetime, timedelta
from http import HTTPStatus
from flask_jwt_extended import create_access_token

from auth.models import insert_auth_code, select_auth_code
from common.utils import call_sms_submit_api, err_resp_form, make_auth_code, resp_form
from config.settings import JWT


def create_auth_code_service(phone):
    auth_code = make_auth_code()
    is_suc = insert_auth_code(phone, auth_code)

    if not is_suc:
        return err_resp_form(HTTPStatus.INTERNAL_SERVER_ERROR, 'Internal Server Error')
    
    success = call_sms_submit_api(phone)
    if success:
        return resp_form(HTTPStatus.CREATED, {})
    else:
        return err_resp_form(HTTPStatus.INTERNAL_SERVER_ERROR, 'Internal Server Error')


def check_auth_code_service(phone, auth_code):
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
