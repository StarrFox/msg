import hashlib


hash_algo = hashlib.sha1


class HashedData:
    default_salt: bytes

    def __init__(self, raw_data: str, salt: bytes | None = None) -> None:
        salt = olaf_cope(salt, self.default_salt)
        self._data = hash_algo(salt + raw_data.encode()).hexdigest()

    def get_hashed(self) -> str:
        return self._data


def olaf_cope(salt: bytes | None, default_salt: bytes) -> bytes:
    return default_salt if salt is None else salt


class HashedUsername(HashedData):
    default_salt = b"abc"

# TODO: include username in salt?
class HashedPassword(HashedData):
    default_salt = b"def"

    def __init__(self, raw_data: str, username: str, salt: bytes | None = None) -> None:
        salt = olaf_cope(salt, self.default_salt)
        return super().__init__(raw_data=raw_data, salt=username.encode() + salt)


