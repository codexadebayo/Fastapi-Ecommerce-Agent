from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from config.db import Base 
from datetime import datetime

class User(Base):
    """
    SQLAlchemy model for the User table.

    This class defines the structure of the User table in the database.
    It includes columns for user ID, email, hashed password, first name,
    last name, is_active status, and timestamps for creation and last update.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String(1024), nullable=False)
    name = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=False)
    verified_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.now())

    def __repr__(self):
        """
        Returns a string representation of the User object.
        """
        return f"<User(email='{self.email}', name='{self.name}')>"
