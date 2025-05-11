import bcrypt
from fastapi import HTTPException, status


def get_password_hash(password: str) -> str:
    """
    Hashes a password using bcrypt.

    Args:
        password: The password to hash.

    Returns:
        The hashed password as a string.
    """
    try:
        # Generate a salt and hash the password
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
        return hashed_password.decode("utf-8")  # Decode bytes to string
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error hashing password: {str(e)}",
        )



def verify_password(password: str, hashed_password: str) -> bool:
    """
    Verifies a password against its hash using bcrypt.

    Args:
        password: The password to verify.
        hashed_password: The hashed password to compare against.

    Returns:
        True if the password matches the hash, False otherwise.
    """
    try:
        # Use bcrypt.checkpw() to compare the encoded password with the stored hash
        return bcrypt.checkpw(
            password.encode("utf-8"), hashed_password.encode("utf-8")
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error verifying password: {str(e)}",
        )
