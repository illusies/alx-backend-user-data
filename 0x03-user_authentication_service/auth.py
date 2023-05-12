#!/usr/bin/env python3
""" Authentication Module """

from db import DB
from user import User
from bcrypt import hashpw, gensalt, checkpw
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4
from typing import Union


def _hash_password(password: str) -> str:
    """
    A function that takes in a password string arguments and
    returns bytes
    """
    return hashpw(password.encode('utf-8'), gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """A function to initialise the database"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        A function that takes mandatory email and password
        string arguments and return a User object
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            hashed_password = _hash_password(password)
            user = self._db.add_user(email, hashed_password)

            return user

        else:
            raise ValueError(f'User {email} already exists')

    def valid_login(self, email: str, password: str) -> bool:
        """If password is valid returns true, else, false"""
        try:
            user = self._db.find_user_by(email=email)
            return checkpw(password.encode('utf-8'), user.hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """
        A function that finds the user corresponding to the email,
        generate a new UUID and store it in the database as the user’s
        session_id, then return the session ID
        """
        try:
            locate = self._db.find_user_by(email=email)
        except NoResultFound:
            return None

        session_id = _generate_uuid()
        self._db.update_user(locate.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> Union[str, None]:
        """
        A function that takes a single session_id string argument
        and returns the corresponding User or None
        """
        if session_id is None:
            return None
        try:
            locate = self._db.find_user_by(session_id=session_id)
            return locate
        except NoResultFound:
            return None

    def destroy_session(self, user_id: str) -> None:
        """
        A function that takes a single user_id integer 
        argument and returns None
        """
        if user_id is None:
            return None
        try:
            locate = self._db.find_user_by(id=user_id)
            self._db.update_user(locate.id, session_id=None)
        except NoResultFound:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """
        A function that take an email string argument and returns a string
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError

        reset_token = _generate_uuid()

        self._db.update_user(user.id, reset_token=reset_token)

        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """
        A function that takes reset_token string argument and
        a password string argument and returns None
        """
        if reset_token is None or password is None:
            return None

        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError

        hashed_password = _hash_password(password)
        self._db.update_user(user.id,
                             hashed_password=hashed_password,
                             reset_token=None)


def _generate_uuid() -> str:
    """
    A function returns a string representation of a new UUID
    """
    return str(uuid4())
