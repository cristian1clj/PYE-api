import secrets
import string

CHARACTERS = string.ascii_letters + string.digits + string.punctuation
SECRET_KEY = ''.join(secrets.choice(CHARACTERS) for _ in range(130))

PROPAGATE_EXCEPTIONS = True

# Database configuration
SQLALCHEMY_DATABASE_URI = 'postgresql://admin:12345@localhost/pye'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SHOW_SQLALCHEMY_LOG_MESSAGES = False

ERROR_404_HELP = False