import unittest
from pbd_security import CurrentUser

class TestCurrentUser(unittest.TestCase):

    def test_happy_path(self):
        user = CurrentUser(id="123", username="testuser", name="John", surname="Doe", email="john.doe@example.com",
                           email_verified=True, phone_number="1234567890", phone_number_verified=True, tenant_id="tenant1",
                           roles=["admin", "user"], claims={"claim1": "value1", "claim2": "value2"})
        self.assertTrue(user.is_authenticated)
        self.assertEqual(user.id, "123")
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.name, "John")
        self.assertEqual(user.surname, "Doe")
        self.assertEqual(user.email, "john.doe@example.com")
        self.assertTrue(user.email_verified)
        self.assertEqual(user.phone_number, "1234567890")
        self.assertTrue(user.phone_number_verified)
        self.assertEqual(user.tenant_id, "tenant1")
        self.assertEqual(user.roles, ["admin", "user"])
        self.assertEqual(user.claims, {"claim1": "value1", "claim2": "value2"})

    def test_default_values(self):
        user = CurrentUser()
        self.assertTrue(user.is_authenticated)
        self.assertIsNone(user.id)
        self.assertIsNone(user.username)
        self.assertIsNone(user.name)
        self.assertIsNone(user.surname)
        self.assertIsNone(user.email)
        self.assertFalse(user.email_verified)
        self.assertIsNone(user.phone_number)
        self.assertFalse(user.phone_number_verified)
        self.assertIsNone(user.tenant_id)
        self.assertEqual(user.roles, [])
        self.assertEqual(user.claims, {})

    def test_partial_values(self):
        user = CurrentUser(id="456", email="jane.doe@example.com", roles=["guest"])
        self.assertTrue(user.is_authenticated)
        self.assertEqual(user.id, "456")
        self.assertIsNone(user.username)
        self.assertIsNone(user.name)
        self.assertIsNone(user.surname)
        self.assertEqual(user.email, "jane.doe@example.com")
        self.assertFalse(user.email_verified)
        self.assertIsNone(user.phone_number)
        self.assertFalse(user.phone_number_verified)
        self.assertIsNone(user.tenant_id)
        self.assertEqual(user.roles, ["guest"])
        self.assertEqual(user.claims, {})

    def test_email_verified(self):
        user = CurrentUser(email_verified=True)
        self.assertTrue(user.is_authenticated)
        self.assertTrue(user.email_verified)

    def test_email_not_verified(self):
        user = CurrentUser(email_verified=False)
        self.assertTrue(user.is_authenticated)
        self.assertFalse(user.email_verified)

    def test_phone_number_verified(self):
        user = CurrentUser(phone_number_verified=True)
        self.assertTrue(user.is_authenticated)
        self.assertTrue(user.phone_number_verified)

    def test_phone_number_not_verified(self):
        user = CurrentUser(phone_number_verified=False)
        self.assertTrue(user.is_authenticated)
        self.assertFalse(user.phone_number_verified)

    def test_empty_roles(self):
        user = CurrentUser(roles=[])
        self.assertTrue(user.is_authenticated)
        self.assertEqual(user.roles, [])

    def test_single_role(self):
        user = CurrentUser(roles=["user"])
        self.assertTrue(user.is_authenticated)
        self.assertEqual(user.roles, ["user"])

    def test_multiple_roles(self):
        user = CurrentUser(roles=["admin", "user"])
        self.assertTrue(user.is_authenticated)
        self.assertEqual(user.roles, ["admin", "user"])

    def test_empty_claims(self):
        user = CurrentUser(claims={})
        self.assertTrue(user.is_authenticated)
        self.assertEqual(user.claims, {})

    def test_single_claim(self):
        user = CurrentUser(claims={"claim1": "value1"})
        self.assertTrue(user.is_authenticated)
        self.assertEqual(user.claims, {"claim1": "value1"})

    def test_multiple_claims(self):
        user = CurrentUser(claims={"claim1": "value1", "claim2": "value2"})
        self.assertTrue(user.is_authenticated)
        self.assertEqual(user.claims, {"claim1": "value1", "claim2": "value2"})

    def test_none_roles(self):
        user = CurrentUser(roles=None)  # type: ignore
        self.assertTrue(user.is_authenticated)
        self.assertEqual(user.roles, [])

    def test_none_claims(self):
        user = CurrentUser(claims=None)  # type: ignore
        self.assertTrue(user.is_authenticated)
        self.assertEqual(user.claims, {})

    def test_is_in_role(self):
        user = CurrentUser(roles=["admin", "user"])
        self.assertTrue(user.is_in_role("admin"))
        self.assertTrue(user.is_in_role("user"))
        self.assertFalse(user.is_in_role("guest"))

    def test_has_claim(self):
        user = CurrentUser(claims={"claim1": "value1", "claim2": "value2"})
        self.assertTrue(user.has_claim("claim1"))
        self.assertTrue(user.has_claim("claim2"))
        self.assertFalse(user.has_claim("claim3"))

    def test_find_claim(self):
        user = CurrentUser(claims={"claim1": "value1", "claim2": "value2"})
        self.assertEqual(user.find_claim("claim1"), "value1")
        self.assertEqual(user.find_claim("claim2"), "value2")
        self.assertIsNone(user.find_claim("claim3"))

    def test_get_all_claims(self):
        claims = {"claim1": "value1", "claim2": "value2"}
        user = CurrentUser(claims=claims)
        self.assertEqual(user.get_all_claims(), claims)
        self.assertEqual(user.get_all_claims(), {"claim1": "value1", "claim2": "value2"})


if __name__ == '__main__':
    unittest.main()