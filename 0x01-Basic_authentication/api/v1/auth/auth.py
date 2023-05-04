#!/usr/bin/env python3
"""Module to manage API Authentication"""
from flask import request
from typing import List, TypeVar


class Auth:
    """A class that manages the API authentication"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """A function that defines which route don't need authentication"""
        if path is None or excluded_paths is None or excluded_paths == []:
            return True

        slash_tolerant = True

        for excluded_path in excluded_paths:
            path_safe_slash = path
            excluded_path_safe_slash = excluded_path

            if slash_tolerant:
                if path_safe_slash[-1] != '/':
                    path_safe_slash += '/'
                if excluded_path_safe_slash[-1] != '/':
                    excluded_path_safe_slash += '/'

            if excluded_path_safe_slash[-2] == '*':
                if excluded_path_safe_slash[:-2] in path_safe_slash:
                    return False

            if path_safe_slash == excluded_path_safe_slash:
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
