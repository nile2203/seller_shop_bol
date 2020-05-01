import uuid


def get_24_char_uuid():
    uid = uuid.uuid4().hex
    for i in range(0, 8):
        uid = uid[:i] + uid[i + 1:]
    return uid.upper()
