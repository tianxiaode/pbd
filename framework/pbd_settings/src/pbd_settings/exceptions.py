from pbd_core import InternalException

class SettingValueProviderNotNameError(InternalException):

    def __init__(self, provider_name: str):
        code = 'Setting value provider not name error'
        data= { 'target' : provider_name }
        message = f"配置值提供者{provider_name}没有定义name属性"
        super().__init__(code, data, message)