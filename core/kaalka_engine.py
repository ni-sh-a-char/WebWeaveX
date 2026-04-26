from kaalka import encrypt


def encrypt_canonical(canonical, timestamp):
    encrypted = encrypt(
        data=canonical,
        time_key=timestamp
    )
    return encrypted