from http import HTTPStatus
from flask import request, Response

from config import app
from config.settings import JWT
from common.utils import is_validated_phone, err_resp_form
from .services import create_auth_code_service, check_auth_code_service


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

        return create_auth_code_service(phone)
    
    elif request.method == 'GET':
        try:
            phone = request.args['phone']
            auth_code = request.args['code']
        except KeyError:
            return err_resp_form(HTTPStatus.BAD_REQUEST, 'Missing Paramaters')
    
        if not is_validated_phone(phone):
            return err_resp_form(HTTPStatus.BAD_REQUEST, 'Invalid Paramaters')

        return check_auth_code_service(phone, auth_code)