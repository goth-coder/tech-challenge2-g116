from typing import Annotated
from pydantic import BaseModel, Field, EmailStr, constr, ValidationError, StringConstraints
class LoginSchema(BaseModel):
    """
    Schema for user login credentials.
    Attributes:
        email (EmailStr): User's email address.
        password (str): User's password (6-50 characters).
    """

    email: EmailStr
    password: Annotated[str, StringConstraints(min_length=6, 
                                               max_length=50,
                                               error_message="Password must be between 6 and 50 characters.")]



class SignupSchema(BaseModel):
    """
    Schema for user signup credentials.
    Attributes:
        name (str): User's full name. Must be between 3 and 100 characters.
        username (str): User's username. Must be between 6 and 100 characters.
        age (int, optional): User's age. Must be greater than 0 if provided.
        password (str): User's password. Must be between 6 and 50 characters.
    """

    name: Annotated[str, StringConstraints(min_length=3, max_length=100,error_message="Name must be between 3 and 100 characters.")]
    username: Annotated[str, StringConstraints(min_length=6, max_length=100,error_message="Username must be between 6 and 100 characters.")]
    email: EmailStr
    age: Annotated[int | None, Field(gt=0)] | None = None
    password: Annotated[str, StringConstraints(min_length=6, max_length=50,error_message="Password must be between 6 and 50 characters.")]