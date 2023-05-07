#!/usr/bin/env python3
"""Module to manage API Authentication"""
from flask import request
from typing import List, TypeVar
from os import getenv


class Auth:
    """A class that manages the API authentication"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """A function that defines which route don't need authentication"""
        if path is None or excluded_paths is None or not len(excluded_paths):
            return True
        # Add slash to all cases for consistency
        if path[-1] != '/':
            path += '/'
        if excluded_paths[-1] != '/':
            excluded_paths += '/'
        if path in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """A function that handles the authorization header"""
        if request is None:
            return None

        return request.headers.get("Authorization", None)

    def current_user(self, request=None) -> TypeVar('User'):
        """A function that validates the current user"""
        return None

    def session_cookie(self, request=None):
        """A function that returns a cookie value from a request"""
        if request is None:
            return None

        cookie_key = getenv('SESSION_NAME')

        return request.cookies.get(cookie_key)
