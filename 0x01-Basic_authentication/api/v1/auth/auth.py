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
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True
        if path[-1] != "/":
            path += "/"

        return path not in excluded_paths

    def authorization_header(self, request=None) -> str:
        """doc"""
        if request is None:
            return None
        return request.headers.get("Authorization", None)

    def current_user(self, request=None) -> TypeVar("User"):
        """doc"""
        return None
