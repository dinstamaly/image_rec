from os import environ


POSTGRES = {
    'user': environ.get('POSTGRES_USER', 'img_core'),
    'pw': environ.get('POSTGRES_PASS', 'qwerty123'),
    'db': environ.get('POSTGRES_DB', 'discount_card'),
    'host': environ.get('POSTGRES_HOST', 'localhost'),
    'port': environ.get('POSTGRES_PORT', '5432'),
}
SQLALCHEMY_DATABASE_URI = (
    'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
)
SQLALCHEMY_POOL_SIZE = 10
SQLALCHEMY_TRACK_MODIFICATIONS = False

DEBUG = True
