import hashlib


hash_algo = hashlib.sha512


class HashedData:
    default_salt: bytes

    def __init__(self, raw_data: str, salt: bytes | None = None) -> None:
        salt = self.default_salt if salt is None else salt
        self._data = hash_algo(salt + raw_data.encode()).hexdigest()

    def get_hashed(self) -> str:
        return self._data


class HashedUsername(HashedData):
    default_salt = b"abc"


class HashedPassword(HashedData):
    default_salt = b"def"
