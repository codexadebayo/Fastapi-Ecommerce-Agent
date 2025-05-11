from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from repositories.user_repository import UserRepository
from models.user import User
from schemas.user_schemas import UserCreate, UserUpdate
from utils.hashing import get_password_hash



class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def create_user(self, user_data: UserCreate) -> User:
        """Create a new user."""
        try:
            # Convert Pydantic model to dict
            user_dict = user_data.dict()
            
            # Pop the password and hash it
            password = user_dict.pop('password')
            hashed_password = get_password_hash(password)
            
            # Create user with hashed password
            user = User(
                email=user_dict['email'],
                hashed_password=hashed_password,
                name=user_dict['name'],
            )
            return await self.repository.create(user)
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error creating user: {str(e)}"
            )

    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get a user by ID."""
        return await self.repository.get_by_id(user_id)

    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Get a user by email."""
        return await self.repository.get_by_email(email)

    async def update_user(self, user_id: int, user_data: UserUpdate) -> Optional[User]:
        """Update a user."""
        user = await self.repository.get_by_id(user_id)
        if not user:
            return None

        for field, value in user_data.dict(exclude_unset=True).items():
            setattr(user, field, value)

        return await self.repository.update(user)

    async def delete_user(self, user_id: int) -> bool:
        """Delete a user."""
        user = await self.repository.get_by_id(user_id)
        if not user:
            return False

        await self.repository.delete(user)
        return True 