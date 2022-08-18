from config import DBConnector

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
  

def insert_user(email: str, password: str, name: str, nickname: str, phone: str) -> tuple[bool, int]:
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
        print(e)
        is_success = False
        err_code = e.args[0]

    return is_success, err_code


def update_user_by_password(email: str, password: str) -> tuple[bool, int]:
    is_success = True
    err_code = 0
    
    try:
        dc = DBConnector()
        conn = dc.connection
        with conn.cursor() as curs:
            sql = 'UPDATE user SET password = sha2(%s, 256), update_date = CURRENT_TIMESTAMP \
                    WHERE email = %s;'
            curs.execute(sql, (password, email,))
        conn.commit()
    except Exception as e:
        print(e)
        err_code = e.args[0]
        is_success = False

    return is_success, err_code


def select_user_by_email_and_password(email: str, password: str) -> tuple[bool, dict]:
    is_success = True
    result = {}
    
    try:
        dc = DBConnector()
        conn = dc.connection
        with conn.cursor() as curs:
            sql = 'SELECT * FROM user WHERE email = %s and password = sha2(%s, 256);'
            curs.execute(sql, (email, password,))
            result = curs.fetchone()
    except Exception as e:
        print(e)
        is_success = False

    return is_success, result
  
    
def select_user_by_id(user_id: int) -> tuple[bool, dict]:
    is_success = True
    result = {}
    
    try:
        dc = DBConnector()
        conn = dc.connection
        with conn.cursor() as curs:
            sql = 'SELECT * FROM user WHERE user_id = %s;'
            curs.execute(sql, user_id)
            result = curs.fetchone()
    except Exception as e:
        print(e)
        is_success = False

    return is_success, result


def select_user_by_email(email: str) -> tuple[bool, dict]:
    is_success = True
    result = {}
    
    try:
        dc = DBConnector()
        conn = dc.connection
        with conn.cursor() as curs:
            sql = 'SELECT * FROM user WHERE email = %s;'
            curs.execute(sql, email)
            result = curs.fetchone()
    except Exception as e:
        print(e)
        is_success = False

    return is_success, result