from pydantic import BaseModel
from typing import Optional

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class ForgotPasswordRequest(BaseModel):
    email: str

class TokenData(BaseModel):
    user_id: Optional[str] = None

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str