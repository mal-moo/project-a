from config import DBConnectionManager

"""
CREATE TABLE `auth_phone` (
    `auth_phone_id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '인증번호 번호',
    `phone` VARCHAR(12) NOT NULL COMMENT '휴대전화',
    `auth_number` VARCHAR(4) NOT NULL COMMENT '휴대전화 인증번호 4자리',
    `create_date` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '등록 일시',
    PRIMARY KEY (`auth_phone_id`),
    UNIQUE (`phone`)
)
"""

def insert_auth_code(phone, auth_code):
    is_success = True
    
    try:
        dbm = DBConnectionManager()
        conn = dbm.connect()
        with conn.cursor() as curs:
            sql = 'INSERT INTO auth_phone(`phone`, `auth_code`) VALUES (%s, %s) \
                    ON DUPLICATE KEY UPDATE auth_code = %s, create_date = CURRENT_TIMESTAMP;'
            curs.execute(sql, (phone, auth_code, auth_code,))
        conn.commit()
        dbm.close()
    except Exception as e:
        #err_code = e.args[0]
        is_success = False

    return is_success#, err_code


def select_auth_code(phone, auth_code):
    is_success = True
    result = {}
    
    try:
        dbm = DBConnectionManager()
        conn = dbm.connect()
        with conn.cursor() as curs:
            sql = 'SELECT create_date FROM auth_phone WHERE phone = %s AND auth_code = %s;'
            curs.execute(sql, (phone, auth_code,))
            result = curs.fetchone()
        dbm.close()
    except Exception as e:
        print(e)
        is_success = False

    return is_success, result
