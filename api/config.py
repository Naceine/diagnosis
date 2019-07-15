import secrets

__all__ = [
    'Production', 'Development', 'Testing',
]


class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = secrets.token_hex(32)
    # DATABASE_URI = 'sqlite: // : memory:'


class Production(Config):
    pass
    # DATABASE_URI = 'mysql: // user@localhost/foo'


class Development(Config):
    DEBUG = True


class Testing(Config):
    TESTING = True
