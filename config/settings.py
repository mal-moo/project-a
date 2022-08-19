DATABASE = {
    "HOST": "localhost",
    "NAME": "commerce",
    "PASSWORD": "dp2qmfflWkd!",
    "USER": "commerce_backend",
    "PORT": "3306",
}

JWT = {
    "SECRET_KEY": "commerce",
    "EXPIRES_IN": {  # minute
        "AUTH": 6,
        "USER": 60 * 24
    }
}
