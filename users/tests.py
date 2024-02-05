from django.test import TestCase
from django.contrib.auth import get_user_model


class UserManagerTest(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            email="user@example.com", password="password123"
        )
        self.assertEqual(user.email, "user@example.com")
        self.assertTrue(user.check_password("password123"))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            email="admin@example.com", password="adminpassword"
        )
        self.assertEqual(admin_user.email, "admin@example.com")
        self.assertTrue(admin_user.check_password("adminpassword"))
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)

        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="admin2@example.com", password="adminpassword", is_staff=False
            )

        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="admin3@example.com", password="adminpassword", is_superuser=False
            )

    def test_create_user_with_extra_fields(self):
        User = get_user_model()
        user = User.objects.create_user(
            email="user2@example.com",
            password="password456",
            is_staff=True,
            is_superuser=True,
        )
        self.assertEqual(user.email, "user2@example.com")
        self.assertTrue(user.check_password("password456"))
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)


class UserTest(TestCase):
    def test_user_model(self):
        User = get_user_model()
        user = User.objects.create_user(
            email="user@example.com", password="password123"
        )
        self.assertEqual(user.email, "user@example.com")
        self.assertTrue(user.check_password("password123"))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertEqual(str(user), "user@example.com")
