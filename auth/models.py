import traceback
from config import DBConnector


def insert_auth_code(phone: str, auth_code: int) -> bool:
    """
        Insert Data in `user` Table
    """
    is_success = True
    
    try:
        dc = DBConnector()
        conn = dc.connection
        with conn.cursor() as curs:
            sql = 'INSERT INTO auth_phone(`phone`, `auth_code`) VALUES (%s, %s) \
                    ON DUPLICATE KEY UPDATE auth_code = %s, create_date = CURRENT_TIMESTAMP;'
            curs.execute(sql, (phone, auth_code, auth_code,))
        conn.commit()
    except Exception:
        print(traceback.format_exc())
        is_success = False

    return is_success


def select_auth_code(phone: str, auth_code: int) -> tuple[bool, dict]:
    """
        Select `create_date` matched `phone` and `auth_code` in `auth_phone` Table
    """
    is_success = True
    result = {}
    
    try:
        dc = DBConnector()
        conn = dc.connection
        with conn.cursor() as curs:
            sql = 'SELECT create_date FROM auth_phone WHERE phone = %s AND auth_code = %s;'
            curs.execute(sql, (phone, auth_code,))
            result = curs.fetchone()
    except Exception:
        print(traceback.format_exc())
        is_success = False

    return is_success, result
