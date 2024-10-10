from django.test import TestCase
from account.models import User

class UserModelTest(TestCase):
    def setUp(self):
        self.email = "test@example.com"
        self.name = "Test User"
        self.password = "password123"
        self.mobile = "666666666"
        self.country = "91"
        self.tc = 'True'
        self.gender = 'F'

    def test_create_user(self):
        user = User.objects.create_user(email=self.email, name=self.name, password=self.password, tc = self.tc, mobile = self.mobile, country = self.country, gender = self.gender)
        
        self.assertEqual(user.email, self.email)
        self.assertEqual(user.name, self.name)
        self.assertTrue(user.check_password(self.password))  # Correct way to check password
        self.assertEqual(user.mobile, self.mobile)
        self.assertEqual(user.country, self.country)
        self.assertTrue(user.tc, self.tc)
        self.assertEqual(user.gender, self.gender)