from common.utils import *


def test_is_validated_nickname():
    invalid_nicknames= [
        None,
        '',
        'nick_name',
        'nicknamelenthtestdata',
    ]

    for nickname in invalid_nicknames:
        result = is_validated_nickname(nickname)
        assert type(result) == bool
        assert result == False


def test_is_validated_name():
    invalid_names= [
        None,
        '',
        '!!!',
        '123',
        'name1',
        'name!',
        'name!1',
        'namelenthtestdataabcde',
    ]

    for name in invalid_names:
        result = is_validated_name(name)
        assert type(result) == bool
        assert result == False


def test_is_validated_email():
    invalid_emails= [
        None,
        '',
        'test@test.test',
        'test',
        'gmail.com',
    ]

    for email in invalid_emails:
        result = is_validated_email(email)
        assert type(result) == bool
        assert result == False


def test_is_validated_phone():
    invalid_phones= [
        None,
        '',
        '0123',
        '010-1234-1234',
        '01312341234',
        '0212341234',
        '0212341234123412341234',
        '!@#$%^&*(',
        'testword'
    ]

    for phone in invalid_phones:
        result = is_validated_phone(phone)
        assert type(result) == bool
        assert result == False


def test_is_validated_password():
    invalid_password= [
        None,
        '',
        'test',
        'testpasswd',
        'testpasswd0',
        'testpasswd0!',
        'testpasswd!',
        'Testpasswd',
    ]

    for password in invalid_password:
        result = is_validated_password(password)
        assert type(result) == bool
        assert result == False


def test_make_auth_code():
    auth_code = make_auth_code()
    assert len(str(auth_code)) == 4
    assert type(auth_code) == int
