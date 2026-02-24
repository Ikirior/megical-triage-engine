from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from services.auth import AuthService 
from contracts import TokenResponse

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=TokenResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Authenticates a user and generates an access token.

    Processes the credentials provided via an OAuth2 compatible form.
    It delegates the cryptographic and database validation to the AuthService.
    If successful, a JSON Web Token (JWT) containing the user"s ID and role 
    is generated and returned for subsequent API requests.

    Args:
        form_data: The standard OAuth2 form dependency containing the "user_id"
                    and "password".

    Returns:
        A TokenResponse model containing the signed JWT and the token type.

    Raises:
        HTTPException: If the provided email or password is incorrect (HTTP 401).
    """
    
    user = await AuthService.authenticate_user(email=form_data.username,
                                               password=form_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    token_payload = {
        "sub": str(user.id),
        "role": user.role
    }
    
    access_token = AuthService.create_access_token(data=token_payload)
    
    return TokenResponse(access_token=access_token, token_type="bearer")