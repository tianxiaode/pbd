from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import os
from typing import Optional
from .interface import IStringEncryptionService

class StringEncryptionService(IStringEncryptionService):
    """AES-GCM 安全加密实现"""
    
    def encrypt(self, plain_text: Optional[str], pass_phrase: str, salt: str) -> Optional[str]:
        if not plain_text or not pass_phrase or not salt:
            return None
        
        key = self._derive_key(pass_phrase, salt)
        aesgcm = AESGCM(key)
        nonce = os.urandom(12)
        ct = aesgcm.encrypt(nonce, plain_text.encode(), None)
        return (nonce + ct).hex()

    def decrypt(self, encrypted_text: Optional[str], pass_phrase: str, salt: str) -> Optional[str]:
        if not encrypted_text or not pass_phrase or not salt:
            return None
        
        encrypted_bytes = bytes.fromhex(encrypted_text)
        nonce = encrypted_bytes[:12]
        ct = encrypted_bytes[12:]
        
        key = self._derive_key(pass_phrase, salt)
        aesgcm = AESGCM(key)
        pt = aesgcm.decrypt(nonce, ct, None)
        return pt.decode()

    def _derive_key(self, pass_phrase: str, salt: str) -> bytes:

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,  # AES-256
            salt=salt.encode(),
            iterations=100_000,
            backend=default_backend()
        )
        return kdf.derive(pass_phrase.encode())