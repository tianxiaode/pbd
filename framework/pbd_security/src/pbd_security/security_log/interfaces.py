from pbd_di import ITransientDependency, IReplaceableInterface
from abc import ABC, abstractmethod
from .generic import SecurityLog

class ISecurityLogStore(ITransientDependency, IReplaceableInterface, ABC):

    @abstractmethod
    def save(self, log: SecurityLog) -> None:
        """保存安全日志"""
        raise NotImplementedError()