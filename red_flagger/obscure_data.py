"""Functions for obscuring a string.

Modified from: https://stackoverflow.com/questions/2490334/simple-way-to-encode-a-string-according-to-a-password"""

import zlib
from base64 import urlsafe_b64decode as b64d
from base64 import urlsafe_b64encode as b64e


class ObscuringError(Exception):
    # Extremely unlikely (impossible?) to happen, but good to have.
    pass


def obscure(word: str) -> bytes:
    # Has to be encoded to be compressed.
    data = word.encode('utf-16')
    return b64e(zlib.compress(data, 9))


def unobscure(obscured: bytes) -> str:
    data = zlib.decompress(b64d(obscured))
    return data.decode("utf-16")


if __name__ == "__main__":
    # TODO delete this code when it is integrated
    with open("data/toxic_keywords_b16.txt", "rb") as toxic_file:
        for line in toxic_file:
            print(unobscure(line))
