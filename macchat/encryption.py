import hashlib
import six
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Hash import HMAC
from Crypto.Protocol.KDF import PBKDF2


class AESCipher:

    def __init__(self, secret):
        secret_hash = hashlib.sha256(secret.encode('utf8')).digest()
        derived = PBKDF2(secret_hash[0::2], secret_hash[1::2], 64)
        self.key, self.hmac_key = derived[:32], derived[32:]

        BS = 16

        self.pad = (
            lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
        ) if six.PY2 else (
            lambda s: s.decode() + (BS - len(s) % BS) * chr(BS - len(s) % BS)
        )
        self.unpad = lambda s: s[:-ord(s[len(s) - 1:])]

    def encrypt(self, raw):
        raw = self.pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        encrypted_data = iv + cipher.encrypt(raw)
        sig = HMAC.new(self.hmac_key, encrypted_data).digest()
        return sig + encrypted_data

    def decrypt(self, enc):
        hmac, enc = enc[:16], enc[16:]
        sig = HMAC.new(self.hmac_key, enc).digest()
        if sig != hmac:
            return None
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self.unpad(cipher.decrypt(enc[AES.block_size:]))
