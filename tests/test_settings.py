DATABASE = {
    "HOST": "localhost",
    "NAME": "test_commerce",
    "PASSWORD": "testdp2qmfflWkd!",
    "USER": "test_commerce_backend",
    "PORT": "3306",
}

JWT = {
    "SECRET_KEY": "test_commerce",
    "EXPIRES_IN": {  # minute
        "AUTH": 6,
        "USER": 60 * 24
    }
}
