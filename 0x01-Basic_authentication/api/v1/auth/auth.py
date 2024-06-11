#!/usr/bin/env python3
"""
Manages API authentication system
"""
from typing import List, TypeVar
from flask import request


class Auth:
    """doc"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """doc"""
        return False

    def authorization_header(self, request=None) -> str:
        """doc"""
        return None

    def current_user(self, request=None) -> TypeVar("User"):
        """doc"""
        return None
