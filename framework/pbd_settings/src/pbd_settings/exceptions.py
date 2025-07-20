from pbd_core import InternalException

class SettingValueProviderNotNameError(InternalException):
    def __init__(self, provider_name: str):
        code = 'Setting value provider not name error'
        data = {'target': provider_name}
        message = f"配置值提供者{provider_name}没有定义name属性"
        super().__init__(code, data, message)

class SettingDefinitionError(InternalException):
    def __init__(self, message: str):
        code = 'Setting definition error'
        data = {'message': message}
        super().__init__(code, data, message)

class SettingTypeError(SettingDefinitionError):
    def __init__(self, type_name: str):        
        message = f"不支持的子节点类型: {type_name}"
        super().__init__(message)

class SettingDuplicateError(SettingDefinitionError):
    def __init__(self, key: str):
        message = f"重复设置定义：{key}"
        super().__init__(message)
