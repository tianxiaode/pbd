from pbd_core import InternalException

class InvalidResourceFormatException(InternalException):
    def __init__(self, cls_name: str):
        code = 'Invalid resource format '
        data = {"class": cls_name}
        message = f"{cls_name} 必须设置 resources 格式为 字典"
        super().__init__(message,code=code, data=data)


class InvalidDefaultLanguageException(InternalException):
    def __init__(self):
        code = 'Invalid default language'
        message = "默认语言必须是非空字符串"
        super().__init__(message, code=code)