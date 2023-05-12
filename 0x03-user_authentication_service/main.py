#!/usr/bin/env python3
"""Integration test module"""

import requests


def register_user(email: str, password: str) -> None:
    """A function that tests the registration of a user"""
    test_case = requests.post('http://127.0.0.1:5000/users', data={
        'email': email,
        'password': password
    })
    assert test_case.status_code == 200
    assert test_case.json() == {'email': email, 'message': "user created"}


def log_in_wrong_password(email: str, password: str) -> None:
    """A function that tests if there is a login with a wrong password"""
    test_case = requests.post('http://127.0.0.1:5000/sessions', data={
        'email': email,
        'password': password
    })
    assert test_case.status_code == 401


def log_in(email: str, password: str) -> str:
    """A function that tests if there is a login with the right password"""
    test_case = requests.post('http://127.0.0.1:5000/sessions', data={
        'email': email,
        'password': password
    })
    assert test_case.status_code == 200
    assert test_case.json() == {'email': email, 'message': "logged in"}
    # parse the response cookie to return the session_id for other methods
    return test_case.cookies.get('session_id')


def profile_unlogged() -> None:
    """A function to test if a session_id doesn't exist"""
    test_case = requests.get('http://127.0.0.1:5000/profile')
    assert test_case.status_code == 403


def profile_logged(session_id: str) -> None:
    """A function to test if a session_id exists"""
    test_case = requests.get('http://127.0.0.1:5000/profile', cookies={
        'session_id': session_id
    })
    assert test_case.status_code == 200
    assert test_case.json() == {'email': "guillaume@holberton.io"}


def log_out(session_id: str) -> None:
    """A function to test of the user is logged out"""
    test_case = requests.delete('http://127.0.0.1:5000/sessions', cookies={
        'session_id': session_id
    })

    for previous in test_case.history:
        assert previous.status_code == 302


def reset_password_token(email: str) -> str:
    """A function to check if the password reset token gets generated"""
    test_case = requests.post('http://127.0.0.1:5000/reset_password', data={
        'email': email,
    })
    assert test_case.status_code == 200

    return test_case.json().get('reset_token')


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """A function to test if a password can be changed"""
    test_case = requests.put('http://127.0.0.1:5000/reset_password', data={
        'email': email,
        'reset_token': reset_token,
        'new_password': new_password
    })
    assert test_case.status_code == 200
    assert test_case.json() == {'email': email, 'message': "Password updated"}


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
