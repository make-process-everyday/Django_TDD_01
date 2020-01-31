from django.test import TestCase
# unittest.TestCase 的增强版

# Create your tests here.
class SmokeTest(TestCase):
    def test_bad_maths(self):
        self.assertEqual(1 + 1, 3)