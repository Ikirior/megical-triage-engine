
from beanie import PydanticObjectId
from beanie.operators import Or
from typing import Optional, List
from models import User
from contracts import (UserCreate, UserResponse, UserUpdate, UserUpdatePassword)
from services.auth import AuthService
from exceptions import UserNotFoundError, DuplicateUserError, InadequateTokenError
import secrets
import asyncio

class UserService:
    """
    Provides administrative operations for staff member management.

    This service handles the business logic for User (staff) CRUD operations,
    including registration, authentication retrieval for the AuthService,
    and administrative updates for the dashboard.

    Note:
        All database operations are asynchronous and utilize the Beanie ODM.
    """
    
    @staticmethod
    async def create_user(user_data: UserCreate) -> UserResponse:
        """
        Creates a new staff member in the system.

        Validates if the Email or CPF already exists to prevent duplicates.
        Hashes the raw password before persistence.

        Args:
            user_data: A UserCreate schema containing registration details.

        Returns:
            The created User document object, or None if a conflict is found.
        """
        
        find_exist_user = await User.find_one(
            Or(User.email == user_data.email, User.cpf == user_data.cpf)
        )
        
        if find_exist_user:
            raise DuplicateUserError("Email or CPF already registered.")
        
        password_hash = AuthService.get_password_hash(secrets.token_urlsafe(30)) # user_data.password is no longer used. A random password is generated instead.
        asyncio.create_task(AuthService.send_passwd_email(user_data.email)) # do not await
            
        new_user = User(
            **user_data.model_dump(exclude={"password"}),
            password_hash=password_hash
        )
        
        await new_user.insert()
        return new_user
    
    @staticmethod
    async def change_user_password(change_password_token: UserUpdatePassword) -> UserResponse:
        """
        Change the password of a user, by providing a server-generated change password token.
        This token is issued by `AuthService.send_passwd_email` upon account creation or password reset request. 

        Args:
            change_password_token: a schema containing a password and a token string. It should include `email` and `function`=`passwd_reset` fields.

        Returns:
            The User document object, or None if a conflict is found.

        Raises:
            HTTPException: If the token is invalid, tampered with, or expired (HTTP 401).
            InadequateTokenError: If the token is not adequate for the function of resetting a password.
            UserNotFoundError: If the user email does not exist within the database.


        """
        decoded_token = AuthService.decode_access_token(change_password_token.token)
        
        if 'email' not in decoded_token.keys() or ('function' not in decoded_token.keys() and decoded_token['function'] == 'passwd_reset'):
            raise InadequateTokenError('Provided token is not adequate for password reset action.')
        
        user = await UserService.get_user_by_email(decoded_token['email'])
        if not user:
            raise UserNotFoundError("Incorrect user ID or user does not exist")
        
        new_password = change_password_token.password
        user.password_hash = AuthService.get_password_hash(new_password)
        
        await user.save()
        
        return UserResponse(**user.model_dump())
            
    
    @staticmethod
    async def get_user_by_email(email:str) -> Optional[User]:
        """
        Retrieves a full user document by email for authentication.

        Used by AuthService to verify credentials during login.

        Args:
            email: The unique email address of the user.

        Returns:
            The complete User document including the password hash, or None.
        """
        
        return await User.find_one(User.email == email)

    @staticmethod
    async def get_user_by_id(user_id: PydanticObjectId) -> UserResponse:
        """
        Fetches a single user by their unique database ID.

        Args:
            user_id: The PydanticObjectId of the target user.

        Returns:
            A UserResponse DTO for frontend display, or None if not found.
        """
        
        user = await User.get(user_id)
        
        if not user:
            raise UserNotFoundError("Incorrect user ID or user does not exist")
        
        return UserResponse(**user.model_dump())
    
    @staticmethod
    async def list_users() -> List[UserResponse]:
        """
        Retrieves all registered staff members for the Admin panel.

        Returns:
            A list of UserResponse objects representing all users in the database.
        """
        
        users_from_db = await User.find_all().to_list()
        
        return [UserResponse(**user.model_dump()) for user in users_from_db]
    
    @staticmethod
    async def update_user(user_id: PydanticObjectId, new_data: UserUpdate) -> UserResponse:
        """
        Updates specific fields of an existing user.

        Supports partial updates. If a new password is provided, it is
        automatically re-hashed before saving.

        Args:
            user_id: The ID of the user to be updated.
            new_data: A UserUpdate schema with the fields to be modified.

        Returns:
            The updated UserResponse DTO, or None if the user does not exist.
        """
        
        user = await User.get(user_id)
        
        if not user:
            raise UserNotFoundError("Incorrect user ID or user does not exist")

        update_dict = new_data.model_dump(exclude_unset=True)
        
        # if "password" in update_dict:
        #     new_password = update_dict.pop("password")
        #     user.password_hash = AuthService.get_password_hash(new_password)
        
        for key, value in update_dict.items():
            setattr(user, key, value)
        
        await user.save()
        
        return UserResponse(**user.model_dump())

    @staticmethod
    async def delete_user(user_id: PydanticObjectId) -> bool:
        """
        Removes a staff member's access by deleting their record.

        Args:
            user_id: The ID of the user to be removed.

        Returns:
            True if the operation was successful, None otherwise.
        """
        
        user = await User.get(user_id)
        
        if not user:
            raise UserNotFoundError("Incorrect user ID or user does not exist")
        
        await user.delete()
        
        return True