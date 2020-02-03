import time

from django.template.loader import render_to_string
from django.urls import resolve
from lists.models import Item
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
        response = self.client.post('/', data={'new_item_text': 'A new list item'})
        self.assertTemplateUsed(response, 'home.html')
        self.assertIn('A new list item', response.content.decode())

class ItemModelTest(TestCase):
     def test_saving_and_retrieving_items(self):
         first_item = Item()
         first_item.text = 'The first (ever) list item'
         first_item.save()
         second_item = Item()
         second_item.text = 'Item the second'
         second_item.save()
         saved_items = Item.objects.all()
         self.assertEqual(saved_items.count(), 2)
         first_saved_item = saved_items[0]
         second_saved_item = saved_items[1]
         self.assertEqual(first_saved_item.text, 'The first (ever) list item')
         self.assertEqual(second_saved_item.text, 'Item the second')