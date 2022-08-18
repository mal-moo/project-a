from config import DBConnectionManager

"""
CREATE TABLE `user` (
    `user_id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '유저 번호',
    `name` VARCHAR(20) NOT NULL COMMENT '이름',
    `nickname` VARCHAR(20) NOT NULL COMMENT '닉네임',
    `phone` VARCHAR(12) NOT NULL COMMENT '휴대전화',
    `email` VARCHAR(50) NOT NULL COMMENT '이메일',
    `password` VARCHAR(256) NOT NULL COMMENT '비밀번호',
    `create_date` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '등록 일시',
    `update_date` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '수정 일시',
    PRIMARY KEY (`user_id`),
    UNIQUE (`email`, `nickname`)
)
"""

def select_user_by_id(user_id):
    is_success = True
    result = {}
    
    try:
        dbm = DBConnectionManager()
        conn = dbm.connect()
        with conn.cursor() as curs:
            sql = 'select * from user where user_id = %s'
            curs.execute(sql, user_id)
            result = curs.fetchone()
        dbm.close()
    except Exception as e:
        print(e)
        is_success = False

    return is_success, result


def select_user_by_email(email):
    is_success = True
    result = {}
    
    try:
        dbm = DBConnectionManager()
        conn = dbm.connect()
        with conn.cursor() as curs:
            sql = 'select * from user where email = %s'
            curs.execute(sql, email)
            result = curs.fetchone()
        dbm.close()
    except Exception as e:
        print(e)
        is_success = False

    return is_success, result
  

def insert_user(email, password, name, nickname, phone):
    is_success = True
    error_code = 0
    
    try:
        dbm = DBConnectionManager()
        conn = dbm.connect()
        with conn.cursor() as curs:
            sql = 'INSERT INTO user(`email`, `password`, `name`, `nickname`, `phone`) \
                    VALUES (%s, SHA2(%s, 256), %s, %s, %s);'
            curs.execute(sql, (email, password, name, nickname, phone,))
        conn.commit()
        dbm.close()
    except Exception as e:
        print(e)
        is_success = False
        error_code = e.args[0]

    return is_success, error_code


def update_user_by_password(email, password):
    is_success = True
    
    try:
        dbm = DBConnectionManager()
        conn = dbm.connect()
        with conn.cursor() as curs:
            sql = 'UPDATE user SET password = sha2(%s, 256), update_date = CURRENT_TIMESTAMP \
                    WHERE email = %s;'
            curs.execute(sql, (password, email,))
        conn.commit()
        dbm.close()
    except Exception as e:
        print(e)
        is_success = False

    return is_success


def select_user_by_email_and_password(email, password):
    is_success = True
    result = {}
    
    try:
        dbm = DBConnectionManager()
        conn = dbm.connect()
        with conn.cursor() as curs:
            sql = 'select * from user where email = %s and password = sha2(%s, 256);'
            curs.execute(sql, (email, password,))
            result = curs.fetchone()
        dbm.close()
    except Exception as e:
        print(e)
        is_success = False

    return is_success, result
  
    
