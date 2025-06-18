from abc import ABC, abstractmethod
from typing import Optional
from pbd_di import ITransientDependency, IReplaceableInterface

class IStringEncryptionService(ITransientDependency,IReplaceableInterface, ABC):
    @abstractmethod
    def encrypt(self, plain_text: Optional[str], pass_phrase: str, salt: str) -> Optional[str]:
        raise NotImplementedError()
    
    @abstractmethod
    def decrypt(self, encrypted_text: Optional[str], pass_phrase: str, salt: str) -> Optional[str]:
        raise NotImplementedError()

