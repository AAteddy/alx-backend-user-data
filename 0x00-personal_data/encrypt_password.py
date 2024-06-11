#!/usr/bin/env python3
"""Password Encryption & Validation Project Module.
User passwords should NEVER be stored in plain text in a database.
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """A function that expects one string argument
    and returns a salted, hashed password.

    Generates a salted and hashed password.

    Args:
            password (str): A string containing the plain text
            password to be hashed.

    Returns:
            bytes: A byte string representing the salted, hashed password.

    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """A function that validate that the provided
    password matches the hashed password.

    Validates whether the provided password matches the hashed password.

    Args:
            hashed_password (bytes): A byte string representing
            the salted, hashed password.
            password (str): A string containing the plain text
            password to be validated.

    Returns:
            bool: True if the provided password matches the hashed
            password, False otherwise.

    """
    return bcrypt.checkpw(password.encode(), hashed_password)
