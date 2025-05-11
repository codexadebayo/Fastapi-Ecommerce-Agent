import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from models.user import User

@pytest.mark.asyncio
async def test_create_user(test_db_session: AsyncSession):
    """Test creating a new user."""
    # Create a test user
    test_user = User(
        email="test@example.com",
        hashed_password="hashed_password_here",
        name="Test User",
        is_active=True
    )
    
    # Add and commit the user
    test_db_session.add(test_user)
    await test_db_session.commit()
    await test_db_session.refresh(test_user)
    
    # Verify the user was created
    assert test_user.id is not None
    assert test_user.email == "test@example.com"
    assert test_user.name == "Test User"
    assert test_user.is_active is True

@pytest.mark.asyncio
async def test_get_user(test_db_session: AsyncSession):
    """Test retrieving a user."""
    # Create a test user
    test_user = User(
        email="get_test@example.com",
        hashed_password="hashed_password_here",
        name="Get Test User",
        is_active=True
    )
    
    # Add and commit the user
    test_db_session.add(test_user)
    await test_db_session.commit()
    
    # Retrieve the user
    retrieved_user = await test_db_session.get(User, test_user.id)
    
    # Verify the user was retrieved correctly
    assert retrieved_user is not None
    assert retrieved_user.email == "get_test@example.com"
    assert retrieved_user.name == "Get Test User" 