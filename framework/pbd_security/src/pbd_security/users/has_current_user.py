from pbd_di import IDependencyBase, NotDependencyBaseSubclassException
from .current_user import CurrentUser

class HasCurrentUser:
    """
    Interface for classes that have a current user.
    """
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        # 检查当前被定义的子类（cls）是否继承自 IDependencyBase
        if not issubclass(cls, IDependencyBase):
            raise NotDependencyBaseSubclassException(cls)
        

    @property
    def current_user(self):
        """
        Get the current user.
        
        :return: The current user object.
        """
        return self.get_dependency(CurrentUser)
        
