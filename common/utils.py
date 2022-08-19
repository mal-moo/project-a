import re
from flask import jsonify, Response
from random import randint
from password_strength import PasswordPolicy
from email_validator import validate_email, EmailNotValidError


def is_validated_password(password: str) -> bool:
    policy = PasswordPolicy.from_names(
                            length=8,
                            uppercase=1,
                            numbers=1,
                            special=1,
                        )
    return not bool(policy.test(password))


def is_validated_email(email: str) -> bool:
    is_validate = True
    try:
        email = validate_email(email).email
        
    except EmailNotValidError as e:
        print(str(e))
        is_validate = False

    return is_validate


def is_validated_phone(phone: str) -> bool:
    return bool(re.search('^01([0|1|6|7|8|9])?([0-9]{3,4})?([0-9]{4})$', phone))
    

def is_validated_name(name: str) -> bool:
    if len(name) > 0 and len(name) <= 20:
        return bool(re.search('^[가-힣]{2,10}$', name))
    else:
        return False


def is_validated_nickname(nickname: str) -> bool:
    if len(nickname) > 0 and len(nickname) <= 20:
        return bool(re.search('^[ㄱ-힣a-zA-Z0-9]{1,20}$', nickname))
    else:
        return False


def make_auth_code() -> int:
    return randint(1000, 10000)


def call_sms_submit_api(phone: str) -> bool:
    return True


def err_resp_form(status_code: int, message: str) -> tuple[Response, int]:
    form = {
        'msg': message,
    }
    return jsonify(form), status_code


def resp_form(status_code: int, data: dict) -> tuple[Response, int]:
    form = {
        'msg': 'success',
        'data': data,
    }
    return jsonify(form), status_code