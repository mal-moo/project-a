import re
from flask import jsonify
from random import randint
from password_strength import PasswordPolicy
from email_validator import validate_email, EmailNotValidError


def is_validated_password(password):
    policy = PasswordPolicy.from_names(
                            length=8,
                            uppercase=1,
                            numbers=1,
                            special=1,
                        )
    return not policy.test(password)


def is_validated_email(email):
    is_validate = True
    try:
        email = validate_email(email).email
        
    except EmailNotValidError as e:
        print(str(e))
        is_validate = False

    return is_validate


def is_validated_phone(phone):
    return re.search('^01([0|1|6|7|8|9])?([0-9]{3,4})?([0-9]{4})$', phone)
    

def is_validated_name(name):
    if len(name) > 0 and len(name) <= 20:
        return re.search('([ㄱ-힣a-zA-Z])', name)
    else:
        return None


def is_validated_nickname(nickname):
    if len(nickname) > 0 and len(nickname) <= 20:
        return re.search('([ㄱ-힣a-zA-Z0-9])', nickname)
    else:
        return None


def make_auth_code():
    return randint(1000, 10000)


def call_sms_submit_api():
    return True


def err_resp_form(status_code, message):
    form = {
        'msg': message,
    }
    return jsonify(form), status_code


def resp_form(status_code, data):
    form = {
        'data': data,
    }
    return jsonify(form), status_code