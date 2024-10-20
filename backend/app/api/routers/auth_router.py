from fastapi import APIRouter
from starlette.responses import JSONResponse

from app.api.depenencies import TokenServiceIoC, AuthServiceIoC
from app.api.schema.auth.login_request import LoginRequest

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post('/login')
async def login(body: LoginRequest, token_service: TokenServiceIoC, auth_service: AuthServiceIoC):
    user = await auth_service.authenticate(body.email, body.password)
    print(user)
    if not user:
        return JSONResponse(status_code=401, content={"detail": "Invalid credentials"})

    return token_service.create_access_token(user)
