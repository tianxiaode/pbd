from pbd_core import BusinessException

class PbdAuthenticationError(BusinessException):

    def __init__(self, message:str, code: str, data: dict):
        super().__init__(message,code=code, data=data)
