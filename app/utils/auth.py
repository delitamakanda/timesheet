import bcrypt
import shortuuid

from itsdangerous.timed import TimestampSigner
from itsdangerous.timed import BadTimeSignature, SignatureExpired, BadSignature
from cryptography.fernet import Fernet, InvalidToken

from app.config import SECRET_KEY, TOKEN_EXPIRATION_TIME, UUID_ALPHABET, UUID_LENGTH

app_secret_key = Fernet(SECRET_KEY)

def get_common_key():
    return app_secret_key

def uuid():
    return shortuuid.ShortUUID(alphabet=UUID_ALPHABET).random(UUID_LENGTH)


def encrypt_password(password):
    encryptor = get_common_key()
    return encryptor.encrypt(password.encode('utf-8'))

def decrypt_password(encrypted_password):
    try:
        decryptor = get_common_key()
        return decryptor.decrypt(encrypted_password.encode('utf-8'))
    except InvalidToken:
        return None

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def verify_password(plain_password, hashed_password):
    return bcrypt.hashpw(plain_password.encode('utf-8'), hashed_password) == hashed_password

def generate_timed_token(user_dict, expiration=TOKEN_EXPIRATION_TIME):
    s = TimestampSigner(SECRET_KEY, expires_in=expiration)
    return s.dumps(user_dict)

def verify_timed_token(token):
    s = TimestampSigner(SECRET_KEY)
    try:
        data = s.loads(token)
    except (SignatureExpired, BadSignature):
        return None
    return data
