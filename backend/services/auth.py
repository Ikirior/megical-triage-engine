import os
from datetime import datetime, timedelta, timezone
from typing import Optional
import bcrypt
from jose import jwt, JWTError
from dotenv import load_dotenv
from fastapi import HTTPException, status
from models import User
import smtplib
from email.mime.text import MIMEText

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.abspath(os.path.join(CURRENT_DIR, "..", "..", ".env.back"))

load_dotenv(dotenv_path=ENV_PATH)

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("Critical Error: SECRET_KEY not found in .env.back file.")

ALGORITHM = os.getenv("ALGORITHM", "HS256")

class AuthService:
    """
    Manages security operations, cryptography, and JWT token lifecycle.

    This service centralizes all hashing and validation logic, ensuring that
    the rest of the application does not handle raw cryptographic operations.
    It utilizes bcrypt for password hashing and python-jose for JWT signing.
    """
    
    @staticmethod
    def get_password_hash(password: str) -> str:
        """
        Generates a cryptographic hash from a plain text password.

        Uses the bcrypt algorithm, which automatically generates a secure salt
        and embeds it within the resulting hash string.

        Args:
            password: The plain text password.

        Returns:
            A string containing the bcrypt hash.
        """
        
        password_bytes = password.encode("utf-8")
        
        hashed_bytes = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
        
        return hashed_bytes.decode("utf-8")
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Verifies a plain text password against a stored bcrypt hash.

        Args:
            plain_password: The password provided during the login attempt.
            hashed_password: The securely stored bcrypt hash from the database.

        Returns:
            True if the password matches the hash, False otherwise.
        """
        
        plain_bytes = plain_password.encode("utf-8")
        hashed_bytes = hashed_password.encode('utf-8')
        
        return bcrypt.checkpw(plain_bytes, hashed_bytes)
    
    @staticmethod
    async def authenticate_user(email: str, password: str) -> Optional[User]:
        """
        Validates a user's credentials against the database records.

        Args:
            email: The email address provided by the user.
            password: The plain text password provided by the user.

        Returns:
            The matched User document object if credentials are valid, None otherwise.
        """
        
        user = await User.find_one(User.email == email)
        
        if not user:
            return None
        
        if not AuthService.verify_password(password, user.password_hash):
            return None
        
        return user
    
    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """
        Generates a signed JSON Web Token (JWT) for session management.

        Args:
            data: A dictionary containing the payload (e.g., user ID and role).
            expires_delta: The validity duration of the token. Defaults to 120 minutes if None.

        Returns:
            The signed JWT as a string.
        """
        
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=120)
        
        to_encode.update({"exp": expire})
        
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    @staticmethod
    def decode_access_token(token: str) -> dict:
        """
        Decodes and validates the signature and expiration of a JWT.

        Used primarily by FastAPI dependency injection to authorize protected routes.

        Args:
            token: The JWT string intercepted from the request headers.

        Returns:
            The decoded payload as a dictionary.

        Raises:
            HTTPException: If the token is invalid, tampered with, or expired (HTTP 401).
        """
        
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
    @staticmethod
    async def send_passwd_email(email: str) -> bool:
        """
        Given an e-mail address, sends a password reset e-mail.

        Args:
            email: the e-mail address to send a message to.

        Returns:
            If the operation was successful.

        Raises:
            HTTPException: If the token is invalid, tampered with, or expired (HTTP 401).
        """
        
        sending_email = os.getenv('SMTP_SERVER_EMAIL')

        content = ''

        token = AuthService.create_access_token({'email': email, 'function': 'passwd_reset'}, )
        frontend_page_url = f"http://{os.getenv('FRONTEND_HOSTNAME')}/resetpassword/?token={token}"

        html_path = os.path.join(os.getcwd(), 'static', 'email.html')
        with open(html_path) as html_file:
            content = html_file.read()
            content = content.replace('$USER', email)
            content = content.replace('$HREF', frontend_page_url)


        # https://mailtrap.io/blog/python-send-email-gmail/#Send-HTML-email
        message = MIMEText(content, 'html')
        message['Subject'] = 'Enable yout MTE account'
        message['From'] = sending_email
        message['To'] = email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(
                user=sending_email,
                password=os.getenv('SMTP_APP_KEY')
            )
            server.sendmail(sending_email, email, message.as_string()) 
            return True