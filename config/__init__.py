from flask import Flask
import pymysql
from flask_jwt_extended import JWTManager
from .settings import DATABASE, JWT

app = Flask(__name__)
app.config.update(
    DEBUG = True,
    JWT_SECRET_KEY = JWT['SECRET_KEY']
)

jwt = JWTManager(app)

class DBConnector:    
    def __init__(self):
        self.host = DATABASE['HOST']
        self.user = DATABASE['USER']
        self.password = DATABASE['PASSWORD']
        self.port = DATABASE['PORT']
        self.name = DATABASE['NAME']
        self.connect()

    def connect(self):
        try:
            self.connection = pymysql.connect(
                            host=self.host,
                            user=self.user,
                            password=self.password,
                            database=self.name,
                            charset='utf8mb4',
                            cursorclass=pymysql.cursors.DictCursor
                        )
        except Exception as e:
            print(e)

    def __del__(self):
        self.connection.close()
        

import users.views
import auth.views