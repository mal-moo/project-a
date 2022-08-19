


from datetime import timedelta
from http import HTTPStatus
from flask_jwt_extended import create_access_token

from common.utils import err_resp_form, resp_form
from config.settings import JWT
from .models import *


def reset_user_password_service(email, password):
    is_suc, user_id = select_user_id_by_email(email)
    if not is_suc:
        return err_resp_form(HTTPStatus.INTERNAL_SERVER_ERROR, 'Internal Server Error')
    if not user_id:
        return err_resp_form(HTTPStatus.FORBIDDEN, 'Forbbiden')

    is_suc, dupl_user_id = select_user_id_by_email_and_password(email, password)
    if not is_suc:
        return err_resp_form(HTTPStatus.INTERNAL_SERVER_ERROR, 'Internal Server Error')
    if dupl_user_id:
        return err_resp_form(HTTPStatus.UNPROCESSABLE_ENTITY, 'Duplicated')
    
    is_suc = update_user_by_password(user_id['user_id'], password)
    if not is_suc:
        return err_resp_form(HTTPStatus.INTERNAL_SERVER_ERROR, 'Internal Server Error')

    return resp_form(HTTPStatus.OK, {})


def user_sign_up_service(email, password, name, nickname, phone):
    is_suc, err_code = insert_user(email, password, name, nickname, phone)
    
    if not is_suc:
        if err_code == 1062:
            return err_resp_form(HTTPStatus.UNPROCESSABLE_ENTITY, 'Duplicated')
        else:
            return err_resp_form(HTTPStatus.INTERNAL_SERVER_ERROR, 'Internal Server Error')

    return resp_form(HTTPStatus.CREATED, {})


def user_login_service(email, password):
    is_suc, user_info = select_user_id_by_email_and_password(email, password)
    if not is_suc:
        return err_resp_form(HTTPStatus.INTERNAL_SERVER_ERROR, 'Internal Server Error')
    if not user_info:
        return err_resp_form(HTTPStatus.FORBIDDEN, 'Forbbiden')
    
    access_token = create_access_token(identity = {'user_id': user_info['user_id']},
                                        expires_delta = timedelta(minutes=JWT['EXPIRES_IN']['USER']))
    return resp_form(HTTPStatus.OK, {
        'access_token': access_token
    })

def user_info_service(user_id):
    is_suc, user_info = select_user_info_by_id(user_id)
    if not is_suc:
        return err_resp_form(HTTPStatus.INTERNAL_SERVER_ERROR, 'Internal Server Error')
    if not user_info:
        return err_resp_form(HTTPStatus.FORBIDDEN, 'Forbbiden')
    
    return resp_form(HTTPStatus.OK, user_info)

    