from jose import jwt
from models import User
import os

SECRET = os.getenv("TOKEN_SECRET")

def create_jwt_token(user: User):
    token = jwt.encode(
        {
            "id": str(user.id),
            "name": user.name,
            "email": user.email,
            "role": user.role,
        },
        SECRET,
        algorithm="HS256"
    )
    return token

def decode_jwt_token(token: str):
    try:
        decoded_token = jwt.decode(token, SECRET, algorithms=["HS256"])
        return decoded_token
    except:
        return None