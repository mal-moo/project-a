import re
from flask import jsonify, Response
from random import randint
from password_strength import PasswordPolicy
from email_validator import validate_email, EmailNotValidError


def is_validated_password(password: str) -> bool:
    """
    Validator of Password
    ---
    Usage
        'password_strength' library
    Policy
        1. length greater than 8
        2. one or more upper letters
        3. one or more digits
        4. one or more special characters
    """
    policy = PasswordPolicy.from_names(
                            length=8,
                            uppercase=1,
                            numbers=1,
                            special=1,
                        )
    return not bool(policy.test(password))


def is_validated_email(email: str) -> bool:
    """
    Validator of Email
    ---
    Usage
        'email_validator' library
    """
    is_validate = True
    try:
        email = validate_email(email).email
        
    except EmailNotValidError as e:
        print(str(e))
        is_validate = False

    return is_validate


def is_validated_phone(phone: str) -> bool:
    """
    Validator of Phone Number
    ---
    Policy
        1. 01012341234 Format
    """
    return bool(re.search('^01([0|1|6|7|8|9])?([0-9]{3,4})?([0-9]{4})$', phone))
    

def is_validated_name(name: str) -> bool:
    """
    Validator of Name
    ---
    Policy
        1. Only letters
        2. Only Korean
        2. 2 < length 20
    """
    if len(name) > 0 and len(name) <= 20:
        return bool(re.search('^[가-힣]{2,20}$', name))
    else:
        return False


def is_validated_nickname(nickname: str) -> bool:
    """
    Validator of Nickname
    ---
    Policy
        1. letters and digit
        2. 1 < length 20
    """
    if len(nickname) > 0 and len(nickname) <= 20:
        return bool(re.search('^[ㄱ-힣a-zA-Z0-9]{1,20}$', nickname))
    else:
        return False


def make_auth_code() -> int:
    """
        Make 4-digits auth code
    """
    return randint(1000, 10000)


def call_sms_submit_api(phone: str) -> bool:
    """
        (incomplete) Call SMS submit API 
        ---
        To do
            1. development with external api
    """
    return True


def err_resp_form(status_code: int, message: str) -> tuple[Response, int]:
    """
        Make Error Response Form
    """
    form = {
        'msg': message,
    }
    return jsonify(form), status_code


def resp_form(status_code: int, data: dict) -> tuple[Response, int]:
    """
        Make Success Response Form
    """
    form = {
        'msg': 'success',
        'data': data,
    }
    return jsonify(form), status_code
