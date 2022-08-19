import sys
import pymysql
from flask import Flask
from flask_jwt_extended import JWTManager
from .settings import JWT


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['JWT_SECRET_KEY'] = JWT['SECRET_KEY']


jwt = JWTManager(app)


class DBConnector:    
    def __init__(self):
        if app.config['TESTING']:
            from tests.test_settings import DATABASE
        else:
            from .settings import DATABASE
        
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
        

@app.route('/', methods=['GET'])
def index() -> str:
    return 'Hello, Project-a !'


import users.views
import auth.views