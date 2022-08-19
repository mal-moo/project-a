from config import app
from tests.test_settings import JWT

app.config.update({
    'TESTING': True,
    'JWT_SECRET_KEY': JWT['SECRET_KEY']
})