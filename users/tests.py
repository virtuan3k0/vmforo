from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserTests(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(
            email='user@example.com',
            username='testuser',
            password='testpass123'
        )
        self.assertEqual(user.email, 'user@example.com')
        self.assertEqual(user.username, 'testuser')
        self.assertTrue(user.check_password('testpass123'))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertIsNone(user.subscription_start_date)
        self.assertIsNone(user.subscription_end_date)
        self.assertEqual(user.subscription_status, 'inactive')
        self.assertFalse(user.is_trial_used)
        self.assertFalse(user.is_auto_renewal)
        self.assertIsNone(user.stripe_customer_id)
        self.assertIsNone(user.stripe_subscription_id)
        self.assertFalse(bool(user.avatar))
        self.assertIsNone(user.bio)
        self.assertIsNone(user.educational_status)
        self.assertIsNone(user.desired_specialty)

    def test_create_superuser(self):
        admin_user = User.objects.create_superuser(
            email='admin@example.com',
            username='adminuser',
            password='adminpass123'
        )
        self.assertEqual(admin_user.email, 'admin@example.com')
        self.assertEqual(admin_user.username, 'adminuser')
        self.assertTrue(admin_user.check_password('adminpass123'))
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        self.assertIsNone(admin_user.subscription_start_date)
        self.assertIsNone(admin_user.subscription_end_date)
        self.assertEqual(admin_user.subscription_status, 'inactive')
        self.assertFalse(admin_user.is_trial_used)
        self.assertFalse(admin_user.is_auto_renewal)
        self.assertIsNone(admin_user.stripe_customer_id)
        self.assertIsNone(admin_user.stripe_subscription_id)
        self.assertFalse(bool(admin_user.avatar))
        self.assertIsNone(admin_user.bio)
        self.assertIsNone(admin_user.educational_status)
        self.assertIsNone(admin_user.desired_specialty)
