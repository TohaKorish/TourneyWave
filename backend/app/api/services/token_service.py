import os
import jwt
from datetime import timedelta, datetime, timezone

from fastapi import HTTPException
from jwt import ExpiredSignatureError
from starlette import status

from app.api.models.user import User
from app.api.schema.auth.token_response import TokenResponse


class TokenService:
    def create_access_token(self, user: User) -> TokenResponse:
        to_encode = {
            'user_id': user.id,
            'role': user.role.value,
        }

        expire_minutes = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', 30))
        secret_key = os.getenv('JWT_SECRET')
        algorithm = os.getenv('ALGORITHM')

        expires_delta = timedelta(minutes=expire_minutes)

        expire = datetime.now(timezone.utc) + expires_delta
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)

        return TokenResponse(access_token=encoded_jwt, token_type="Bearer")

    def validate_token(self, token: str) -> int:
        try:
            payload = jwt.decode(token, os.getenv('JWT_SECRET'), algorithms=[os.getenv('ALGORITHM')])

            return payload.get('user_id')
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
