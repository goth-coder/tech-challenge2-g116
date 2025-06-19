from typing import Annotated

from pydantic import BaseModel, EmailStr, Field, StringConstraints


class LoginSchema(BaseModel):
    """
    Schema for user login credentials.
    Attributes:
        email (EmailStr): User's email address.
        password (str): User's password (6-50 characters).
    """

    email: EmailStr
    password: Annotated[str, StringConstraints(min_length=6, max_length=50)]


class SignupSchema(BaseModel):
    """
    Schema for user signup credentials.
    Attributes:
        name (str): User's full name. Must be between 3 and 100 characters.
        username (str): User's username. Must be between 6 and 100 characters.
        age (int, optional): User's age. Must be greater than 0 if provided.
        password (str): User's password. Must be between 6 and 50 characters.
    """

    name: Annotated[str, StringConstraints(min_length=3, max_length=100)]
    username: Annotated[str, StringConstraints(min_length=6, max_length=100)]
    email: EmailStr
    age: Annotated[int | None, Field(gt=0)] | None = None
    password: Annotated[str, StringConstraints(min_length=6, max_length=50)]
