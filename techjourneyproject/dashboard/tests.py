from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
# Create your tests here.


#Test for User Model Manager

class UsersManagersTests(TestCase):

    #Test for created user
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(self, email='normal@user.com',name="test", password='foo')
        self.assertEqual(user.email, 'normal@user.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(user.username)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email='')
        with self.assertRaises(TypeError):
            User.objects.create_user(name='')
        with self.assertRaises(ValueError):
            User.objects.create_user(self,email='',name='', password="foo")


    #Test for created Super user
    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(self,email='super@user.com', password='foo')
        self.assertEqual(admin_user.email, 'super@user.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(admin_user.username)
        except AttributeError:
            pass
        with self.assertRaises(ValueError):
            User.objects.create_superuser(self,email='super@user.com', password='foo', is_superuser=False)
