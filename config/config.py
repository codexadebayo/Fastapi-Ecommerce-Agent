
from functools import lru_cache
import os
from pydantic import HttpUrl, root_validator
from typing import List, Union, Optional
from pathlib import Path
from dotenv import load_dotenv
from pydantic_settings import BaseSettings



env_path = Path(".") / ".env"
load_dotenv(dotenv_path= env_path)


class Config(BaseSettings):
    """
    Application settings class.

    This class defines all the configuration settings for the FastAPI application.
    It uses Pydantic's BaseSettings to automatically load settings from
    environment variables, with support for default values and type validation.
    """

    PROJECT_NAME: str
    API_V1_STR: str = os.environ.get("API_V1_STR", "/api/v1")
    SECRET_KEY: str
    ALGORITHM: str = os.environ.get("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

    # Database settings
    DB_HOST: str = os.environ.get("DB_HOST", "localhost")
    DB_PORT: Union[str, int] = os.environ.get("DB_PORT", "5432")
    DB_USER: str = os.environ.get("DB_USER", "postgres")
    DB_PASSWORD: Optional[str] = os.environ.get("DB_PASSWORD")
    DB_NAME: str = os.environ.get("DB_NAME", "fastapi_ecommerce")

    #  The database URL is constructed from the other DB settings.
    SQLALCHEMY_DATABASE_URL: str
    #  The @root_validator decorator is used to validate the entire model
    #  and set the SQLALCHEMY_DATABASE_URL.  It's called after Pydantic
    #  has loaded all the other fields.

    
    @root_validator(pre=True)
    def calculate_db_url(cls, values):
        """
        Calculates the database URL from the individual database settings.

        This class method is a Pydantic root validator.  It's called after
        all the other fields have been parsed and validated.  It constructs
        the `SQLALCHEMY_DATABASE_URL` from the other database-related
        settings.

        Args:
            values (dict): The dictionary of field values.

        Returns:
            dict: The updated dictionary of field values, including the
                  `SQLALCHEMY_DATABASE_URL`.

        Raises:
            ValueError: If any of the required database settings
                (DB_HOST, DB_PORT, DB_USER, DB_NAME) are missing.
        """
        db_host = values.get("DB_HOST")
        db_port = values.get("DB_PORT")
        db_user = values.get("DB_USER")
        db_password = values.get("DB_PASSWORD")
        db_name = values.get("DB_NAME")

        if not all([db_host, db_port, db_user, db_name]):
            raise ValueError("Missing required database settings")

        # Construct the database URL.  Include the password if provided.
        if db_password:
            values["SQLALCHEMY_DATABASE_URL"] = (
                f"postgresql+asyncpg://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
            )
        else:
            values["SQLALCHEMY_DATABASE_URL"] = (
                f"postgresql://{db_user}@{db_host}:{db_port}/{db_name}"
            )
        return values

    # CORS settings (Cross-Origin Resource Sharing)
    BACKEND_CORS_ORIGINS: List[str] = os.environ.get("BACKEND_CORS_ORIGINS", "http://localhost,http://localhost:8080").split(",")

    #  Email Settings (Optional, for sending emails)
    MAIL_SERVER: Optional[str] = os.environ.get("MAIL_SERVER")
    MAIL_PORT: Optional[int] = int(os.environ.get("MAIL_PORT")) if os.environ.get("MAIL_PORT") else None
    MAIL_USERNAME: Optional[str] = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD: Optional[str] = os.environ.get("MAIL_PASSWORD")
    MAIL_USE_TLS: Optional[bool] = os.environ.get("MAIL_USE_TLS", "True").lower() == "true"
    MAIL_USE_SSL: Optional[bool] = os.environ.get("MAIL_USE_SSL", "False").lower() == "true"
    #  Email from address.
    EMAIL_FROM: Optional[str] = os.environ.get("EMAIL_FROM", "example@example.com")

    #  Base URL of the application.  Useful for generating absolute URLs
    #  in email templates, etc.
    BASE_URL: HttpUrl = os.environ.get("BASE_URL", "http://localhost:8000")

    class Config:
        """
        Configuration class for Pydantic settings.

        This class provides configuration options for Pydantic's BaseSettings.
        Specifically, it tells BaseSettings to load variables from the
        environment and use case-sensitive matching.
        """
        env_file = ".env"  # Load variables from a .env file
        case_sensitive = True  # Make environment variable names case-sensitive


# Create a global settings instance.  This is what you import and use.
config = Config()



@lru_cache
def get_config():
    return Config()