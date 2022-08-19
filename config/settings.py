DATABASE = {
    "HOST": "localhost",
    "NAME": "ably",
    "PASSWORD": "dp2qmfflWkd!",
    "USER": "ably_backend",
    "PORT": "3306",
}

JWT = {
    "SECRET_KEY": "ably",
    "EXPIRES_IN": { # minute
        "AUTH": 6,
        "USER": 60 * 24
    }
}
