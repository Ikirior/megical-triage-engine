from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from beanie import PydanticObjectId
from jose import JWTError
from services import auth
from models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """
    Validates the JWT token and retrieves the current active user.

    Acts as the primary authentication dependency. It extracts the token from 
    the Authorization header, decodes the cryptographic payload, and verifies 
    the user"s existence in the database to ensure the session is still active.

    Args:
        token: The Bearer token automatically extracted by FastAPI.

    Returns:
        The User document object corresponding to the token"s subject.

    Raises:
        HTTPException: If the token is invalid, expired, or the user no longer 
                       exists in the database (HTTP 401 Unauthorized).
    """
    
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail = "Could not validate credentials",
                                          headers={"WWW-Authenticate": "Bearer"})
    
    try:
        payload = auth.AuthService.decode_access_token(token)
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = await User.get(PydanticObjectId(user_id))
    
    if user is None:
        raise credentials_exception
    
    return user

async def get_current_nurse_user(current_user: User = Depends(get_current_user)) -> User:
    """
    Enforces Role-Based Access Control (RBAC) for nursing operations.

    Args:
        current_user: The authenticated User object, injected by get_current_user.

    Returns:
        The validated User object if the role requirements are met.

    Raises:
        HTTPException: If the user lacks "nurse" or "admin" privileges (HTTP 403 Forbidden).
    """
    
    if current_user.role != "nurse" and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Privilege escalation blocked. Required role: nurse"
        )
        
    return current_user

async def get_current_doctor_user(current_user: User = Depends(get_current_user)) -> User:
    """
    Enforces Role-Based Access Control (RBAC) for medical operations.

    Args:
        current_user: The authenticated User object, injected by get_current_user.

    Returns:
        The validated User object if the role requirements are met.

    Raises:
        HTTPException: If the user lacks "doctor" or "admin" privileges (HTTP 403 Forbidden).
    """
    
    if current_user.role != "doctor" and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Privilege escalation blocked. Required role: doctor"
        )
        
    return current_user

async def get_current_receptionist_user(current_user: User = Depends(get_current_user)) -> User:
    """
    Enforces Role-Based Access Control (RBAC) for front-desk operations.

    Args:
        current_user: The authenticated User object, injected by get_current_user.

    Returns:
        The validated User object if the role requirements are met.

    Raises:
        HTTPException: If the user lacks "receptionist" or "admin" privileges (HTTP 403 Forbidden).
    """
    
    if current_user.role != "receptionist" and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Privilege escalation blocked. Required role: receptionist"
        )
        
    return current_user

async def get_current_admin_user(current_user: User = Depends(get_current_user)) -> User:
    """
    Enforces strict Role-Based Access Control (RBAC) for administrative operations.

    Args:
        current_user: The authenticated User object, injected by get_current_user.

    Returns:
        The validated User object if the administrative role is confirmed.

    Raises:
        HTTPException: If the user is not an "admin" (HTTP 403 Forbidden).
    """
    
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Privilege escalation blocked. Required role: admin."
        )
        
    return current_user