import base64
from django.http import HttpRequest
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from accounts.models.tokens import Token as TokenModel
from cryptography.fernet import Fernet
from decouple import config

from accounts.models.users import UserAccount


def generate_token(user: UserAccount) -> str:
    """
    Generate a token for the user
    """
    try:
        token, _ = TokenModel.objects.get_or_create(user=user)
    except Exception:
        return None
    else:
        return token.key


# Ensure the SECRET_KEY is a valid Fernet key
# Generate a new Fernet key if SECRET_KEY is not provided or invalid

secret_key = config("FERNET_KEY")
try:
    secret_key = base64.urlsafe_b64encode(secret_key.encode())
except Exception:
    raise ValueError("Invalid Fernet key provided in SECRET_KEY")

cipher_suite = Fernet(secret_key)


def encrypt_token(token: str) -> str:
    """
    Encrypt the token using Fernet symmetric encryption
    """
    encrypted_token = cipher_suite.encrypt(token.encode())
    return encrypted_token.decode()


def decrypt_token(encrypted_token: str) -> str:
    """
    Decrypt the token using Fernet symmetric encryption
    """
    decrypted_token = cipher_suite.decrypt(encrypted_token.encode())
    return decrypted_token.decode()


def get_password_reset_token(key: str):
    """
    Get the reset token from the encrypted token
    """
    try:
        token = TokenModel.objects.get(key=key)
    except TokenModel.DoesNotExist:
        return None
    else:
        return token


def validate_posted_data(data: dict, fields: list[str]):
    """Validate against missing fields in posted data"""
    err: bool = False
    errors: dict = {}
    for field in fields:
        if not data.get(field):
            err = True
            errors.update({field: ["this field is required"]})

    return err, errors


def get_user_from_jwttoken(request: HttpRequest) -> UserAccount:
    "Return a user object when a valid jwt token is set in the request header"
    jwt = JWTAuthentication()
    try:
        user = jwt.get_user(
            jwt.get_validated_token((jwt.get_raw_token(jwt.get_header(request))))
        )
    except Exception as e:
        raise AuthenticationFailed(detail="Authorization header is required")
    return user
