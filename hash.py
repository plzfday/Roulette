import hashlib


def hash_password(original):
    password = hashlib.sha256()
    password.update(original.encode('utf-8'))
    password = password.hexdigest()

    return password


def check_hash(original, value):
    return original == hash_password(value)
