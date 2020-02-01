from django.template.loader import render_to_string
from django.urls import resolve
from django.test import TestCase
# unittest.TestCase 的增强版

# Create your tests here.
class HomePageTest(TestCase):
    def test_home_page_returns_correct_html(self):
        # 单元测试
        response = self.client.get('/')
        # Django TestCase 类提供的测试方法，用于检查响应是使用哪个模板渲染的
        self.assertTemplateUsed(response, 'home.html')

    def test_can_save_a_POST_request(self):
        response = self.client.post('/', data={'item_text': 'A new list item'})
        self.assertIn('A new list item', response.content.decode())
        self.assertTemplateUsed(response, 'home.html')