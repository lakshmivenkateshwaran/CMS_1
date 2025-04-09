from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from databases.database import SessionLocal
from models.models import User
from schemas.schemas import LoginRequest, TokenResponse, ForgotPasswordRequest, ResetPasswordRequest
from security.security import create_access_token, get_current_user
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from jose import jwt, JWTError
import os
from fastapi_mail import ConnectionConfig
from config.email_config import settings
from fastapi.responses import JSONResponse

router = APIRouter()

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_STARTTLS=settings.MAIL_STARTTLS,
    MAIL_SSL_TLS=settings.MAIL_SSL_TLS,
    USE_CREDENTIALS=settings.USE_CREDENTIALS,
    VALIDATE_CERTS=settings.VALIDATE_CERTS
)

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == request.username).first()
    if not user or user.password != request.password: 
        raise HTTPException(status_code=400, detail="Invalid username or password")
    
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/forgot-password")
def forgot_password_basic(request: ForgotPasswordRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Email not found")
    
    return {"message": "Password reset link sent to your email"}

@router.post("/forgot_password_email")
def forgot_password_email(request: ForgotPasswordRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Email not found")

    # Step 1: Generate JWT token
    token_data = {"sub": user.email}
    token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)

    # Step 2: Reset link (frontend handles this route)
    reset_link = f"http://localhost:3000/reset-password?token={token}"

    # Step 3: Email content
    message = MessageSchema(
        subject="Password Reset Request",
        recipients=[user.email],
        body=f"Hi {user.username},\n\nClick the link to reset your password:\n{reset_link}",
        subtype="plain"
    )

    # Step 4: Send email
    fm = FastMail(conf)
    fm.send_message(message)

    return {"message": "Password reset link sent to your email"}

@router.post("/forgot_password_token")
def forgot_password_token(request: ForgotPasswordRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Email not found")

    # Step 1: Generate JWT token
    token_data = {"sub": user.email}
    token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)

    # Step 2: Reset link (frontend handles this route)
    reset_link = f"http://localhost:3000/reset-password?token={token}"

    # Step 3: Email content
    message = MessageSchema(
        subject="Password Reset Request",
        recipients=[user.email],
        body=f"Hi {user.username},\n\nClick the link to reset your password:\n{reset_link}",
        subtype="plain"
    )

    # Step 4: Send email
    fm = FastMail(conf)
    fm.send_message(message)

    # Step 5: Return token (for Swagger testing purpose only)
    return {
        "message": "Password reset link sent to your email",
        "token": token,
        "reset_link": reset_link  
    }

@router.post("/reset-password")
def reset_password(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    try:
        # Decode token
        payload = jwt.decode(request.token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=400, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    # Fetch user
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Update password (should ideally hash this)
    user.password = request.new_password
    db.commit()

    return {"message": "Password has been reset successfully"}

@router.post("/logout")
def logout(current_user: str = Depends(get_current_user)):
    return JSONResponse(
        status_code=200,
        content={"message": f"User '{current_user}' logged out successfully."}
    )
