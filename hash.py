import hashlib


def hash_password(original: str) -> str:
    """
    Hash a password string using the SHA-256
    :param original: a password needed to be hashed
    :return: a hashed password
    """
    password = hashlib.sha256()
    password.update(original.encode('utf-8'))
    password = password.hexdigest()

    return password


def check_hash(original: str, value: str) -> bool:
    """
    Check whether two password strings are identical
    :param original: original hashed password in the 'data.json' file
    :param value: a password needed to be compared with the original
    :return: if they are identical, returns True.
             Otherwise, returns False
    """
    return original == hash_password(value)
