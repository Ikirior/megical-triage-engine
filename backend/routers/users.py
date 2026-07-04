from fastapi import APIRouter, HTTPException, Depends
from http import HTTPStatus
from typing import List

from models import User
from contracts import UserCreate, UserResponse, UserUpdate, UserUpdatePassword
from services.users import UserService
from dependencies import get_current_admin_user, get_current_user
from exceptions import UserNotFoundError, DuplicateUserError

router = APIRouter(prefix = "/users",  tags=["user_management"])

@router.get("/", response_model=List[UserResponse])
async def list_users(current_admin: User = Depends(get_current_admin_user)):
    """
    Retrieves a list of all registered staff members.

    Args:
        current_admin: The authenticated administrator, injected by dependency.

    Returns:
        A list of User objects formatted as UserResponse DTOs.
    """
    
    users_list = await UserService.list_users()
    
    return users_list

@router.get("/{user_id}", response_model = UserResponse)
async def get_user(user_id: str, current_user: User = Depends(get_current_user)):
    """
    Fetches a specific staff member by their unique database ID.

    Args:
        user_id: The unique PydanticObjectId of the target user.
        current_admin: The authenticated administrator, injected by dependency.

    Returns:
        The requested User object formatted as a UserResponse DTO.

    Raises:
        HTTPException: If the user ID does not exist in the database (HTTP 404).
    """
    if current_user.role != "admin" and str(current_user.id) != str(user_id):
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail="Access denied. Users can only access their own profiles."
        )
    
    try:
        user = await UserService.get_user_by_id(user_id=user_id)
        return user
    
    except UserNotFoundError:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Incorrect user ID or user does not exist in the database."
        )

@router.post("/", response_model = UserResponse, status_code = HTTPStatus.CREATED)
async def create_user(user_data: UserCreate, current_admin: User = Depends(get_current_admin_user)):
    """
    Registers a new staff member in the system.

    Args:
        user_data: A UserCreate schema containing the registration details.
        current_admin: The authenticated administrator, injected by dependency.

    Returns:
        The newly created User object formatted as a UserResponse DTO.

    Raises:
        HTTPException: If a user with the provided Email or CPF already exists (HTTP 409).
    """
    try:
        new_user = await UserService.create_user(user_data)
        return new_user

    except DuplicateUserError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail="User with this Email or CPF already exists."
        )

@router.put("/{user_id}", response_model = UserResponse)
async def update_user(user_id: str, user_data: UserUpdate, current_admin: User = Depends(get_current_admin_user)):
    """
    Updates specific fields of an existing staff member.

    Args:
        user_id: The unique PydanticObjectId of the user to update.
        user_data: A UserUpdate schema containing the modified fields.
        current_admin: The authenticated administrator, injected by dependency.

    Returns:
        The updated User object formatted as a UserResponse DTO.

    Raises:
        HTTPException: If the user ID does not exist in the database (HTTP 404).
    """
    
    try:
        updated_user = await UserService.update_user(user_id=user_id, new_data=user_data)
        return updated_user
    
    except UserNotFoundError:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Incorrect user ID or user does not exist in the database."
        )

@router.delete("/{user_id}",status_code = HTTPStatus.NO_CONTENT)
async def delete_user(user_id: str, current_admin: User = Depends(get_current_admin_user)):
    """
    Removes a staff member's record from the database.

    Args:
        user_id: The unique PydanticObjectId of the user to delete.
        current_admin: The authenticated administrator, injected by dependency.

    Raises:
        HTTPException: If the user ID does not exist in the database (HTTP 404).
    """
    
    try:
        deleted_user = await UserService.delete_user(user_id)
        return deleted_user
    
    except UserNotFoundError:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Incorrect user ID or user does not exist in the database."
        )


@router.put("/resetpassword/", response_model = UserResponse)
async def update_user(user_update_password: UserUpdatePassword):
    """
    Updates the user password.

    Args:
        token: token.
        password: new user password.

    Returns:
        The updated User object formatted as a UserResponse DTO.

    Raises:
        HTTPException: If the user ID does not exist in the database (HTTP 404).
    """
    
    try:
        updated_user = await UserService.change_user_password(user_update_password)
        return updated_user
    
    except UserNotFoundError:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Incorrect user ID or user does not exist in the database."
        )