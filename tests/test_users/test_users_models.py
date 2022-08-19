from users.models import *


def test_insert_user():
    is_suc, err_code = insert_user(email='leesoonsin@gmail.com', 
                                    password='leesoonsinWkd!', 
                                    name='이순신', 
                                    nickname='장군', 
                                    phone='01098769876')
    
    assert is_suc == True
    assert err_code == 0


def test_insert_user_duplicate():
    is_suc, err_code = insert_user(email='leesoonsin@gmail.com', 
                                    password='leesoonsinWkd!', 
                                    name='이순신', 
                                    nickname='장군', 
                                    phone='01098769876')
    
    assert is_suc == False
    assert err_code == 1062


def test_update_user_by_password():
    is_suc = update_user_by_password(user_id=1, password='leesoonsinWkd!')
    
    assert is_suc == True


def test_select_user_id_by_email_and_password():
    is_suc, result = select_user_id_by_email_and_password(email='leesoonsin@gmail.com', 
                                    password='leesoonsinWkd!')

    assert is_suc == True
    assert type(result['user_id']) == int or None



def test_select_user_info_by_id():
    is_suc, result = select_user_info_by_id(user_id=1)

    assert is_suc == True
    assert type(result['name']) == '이순신'


def test_select_user_id_by_email():
    is_suc, result = select_user_id_by_email(email='leesoonsin@gmail.com')

    assert is_suc == True
    assert type(result['user_id']) == int or None
