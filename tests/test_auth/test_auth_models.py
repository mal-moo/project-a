from auth.models import *


def test_insert_auth_code():
    assert insert_auth_code(phone='01012341234', auth_code='1234') == True
    

def test_insert_auth_code_duplicate_phone():
    assert insert_auth_code(phone='01012341234', auth_code='9876') == True



def test_select_auth_code():
    is_suc, result = select_auth_code(phone='01012341234', auth_code='9876')
    
    assert is_suc == True
    assert result.get('create_date')