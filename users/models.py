import traceback
from config import DBConnector


def insert_user(email: str, password: str, name: str, nickname: str, phone: str) -> tuple[bool, int]:
    """
        Insert Data in `user` Table
    """
    is_success = True
    err_code = 0
    
    try:
        dc = DBConnector()
        conn = dc.connection
        with conn.cursor() as curs:
            sql = 'INSERT INTO user(`email`, `password`, `name`, `nickname`, `phone`) \
                    VALUES (%s, SHA2(%s, 256), %s, %s, %s);'
            curs.execute(sql, (email, password, name, nickname, phone,))
        conn.commit()
    except Exception as e:
        print(traceback.format_exc())
        is_success = False
        err_code = e.args[0]

    return is_success, err_code


def update_user_by_password(user_id: int, password: str) -> tuple[bool, int]:
    """
        Update `password` matched `user_id` in `user` Table
    """
    is_success = True
    
    try:
        dc = DBConnector()
        conn = dc.connection
        with conn.cursor() as curs:
            sql = 'UPDATE user SET password = SHA2(%s, 256), update_date = CURRENT_TIMESTAMP \
                    WHERE user_id = %s;'
            curs.execute(sql, (password, user_id,))
        conn.commit()
    except Exception:
        print(traceback.format_exc())
        is_success = False

    return is_success


def select_user_id_by_email_and_password(email: str, password: str) -> tuple[bool, dict]:
    """
        Select `user_id` matched `email` and `password` in `user` Table
    """
    is_success = True
    result = {}
    
    try:
        dc = DBConnector()
        conn = dc.connection
        with conn.cursor() as curs:
            sql = 'SELECT user_id FROM user WHERE email = %s and password = SHA2(%s, 256);'
            curs.execute(sql, (email, password,))
            result = curs.fetchone()
    except Exception:
        print(traceback.format_exc())
        is_success = False

    return is_success, result
  
    
def select_user_info_by_id(user_id: int) -> tuple[bool, dict]:
    """
        Select `name`, `nickname`, `phone`, `email`, `create_date`, `update_date` 
        matched `user_id` in `user` Table
    """
    is_success = True
    result = {}
    
    try:
        dc = DBConnector()
        conn = dc.connection
        with conn.cursor() as curs:
            sql = 'SELECT name, nickname, phone, email, create_date, update_date FROM user WHERE user_id = %s;'
            curs.execute(sql, user_id)
            result = curs.fetchone()
    except Exception:
        print(traceback.format_exc())
        is_success = False

    return is_success, result


def select_user_id_by_email(email: str) -> tuple[bool, dict]:
    """
        Select `user_id` matched `email` in `user` Table
    """
    is_success = True
    result = {}
    
    try:
        dc = DBConnector()
        conn = dc.connection
        with conn.cursor() as curs:
            sql = 'SELECT user_id FROM user WHERE email = %s;'
            curs.execute(sql, email)
            result = curs.fetchone()
    except Exception:
        print(traceback.format_exc())
        is_success = False

    return is_success, result
