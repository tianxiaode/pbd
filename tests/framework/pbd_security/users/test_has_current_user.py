import unittest
from unittest.mock import MagicMock, patch
from pbd_di import IDependencyBase, NotDependencyBaseSubclassException
from pbd_security import HasCurrentUser, CurrentUser

class TestHasCurrentUser(unittest.TestCase):

    def test_happy_path(self):
        class MockCurrentUser(CurrentUser):
            pass

        class MockDependencyBase(IDependencyBase):
            def get_dependency(self, dependency_type):
                if dependency_type == CurrentUser:
                    return MockCurrentUser()

        class MockHasCurrentUser(HasCurrentUser, MockDependencyBase):
            pass

        mock_instance = MockHasCurrentUser()
        self.assertIsInstance(mock_instance.current_user, CurrentUser)

    def test_edge_case_not_dependency_base_subclass(self):

        with self.assertRaises(NotDependencyBaseSubclassException):
            class MockHasCurrentUser(HasCurrentUser):
                pass

    def test_edge_case_dependency_not_found(self):
        class MockDependencyBase(IDependencyBase):
            def get_dependency(self, dependency_type):
                return None

        class MockHasCurrentUser(HasCurrentUser, MockDependencyBase):
            pass

        mock_instance = MockHasCurrentUser()
        self.assertIsNone(mock_instance.current_user)


if __name__ == '__main__':
    unittest.main()