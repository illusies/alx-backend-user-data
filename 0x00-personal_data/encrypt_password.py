#!/usr/bin/env python3
"""An app that encrypts passwords for a database"""


import bcrypt


def hash_password(password: str) -> bytes:
    """
    A function that expects one string argument name password
    and returns a salted, hashed password, which is a byte string
    """
    pass_encoded = password.encode()
    pass_hashed = bcrypt.hashpw(pass_encoded, bcrypt.gensalt())

    return pass_hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """A function that expects 2 arguments and returns a boolean"""
    valid = False
    pass_encoded = password.encode()
    if bcrypt.checkpw(pass_encoded, hashed_password):
        valid = True
    return valid
