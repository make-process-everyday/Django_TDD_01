import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
    def tearDown(self):
        self.browser.quit()
    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get('http://localhost:8000')
        time.sleep(5)
        # 她注意到网页的标题和头部都包含“To-Do”这个词
        self.assertIn('To-Do', self.browser.title.strip())
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # 应用邀请她输入一个待办事项
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'),
                         'Enter a to-do item')

        # 她在一个文本框中输入了“Buy peacock feathers”（购买孔雀羽毛）
        # 伊迪丝的爱好是使用假蝇做鱼饵钓鱼
        inputbox.send_keys('Buy peacock feathers')
        time.sleep(5)
        # 她按回车键后，页面更新了
        # 待办事项表格中显示了“1: Buy peacock feathers”
        # Keys 是发送回车键等特殊的按键
        inputbox.send_keys(Keys.ENTER)

        # 按下回车键后页面会刷新。time.sleep 的作用是等待页面加载完毕，这样才能针对新页面下断言。
        time.sleep(1)
        print(self.browser)

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')

        self.assertTrue(
            any(row.text == '1: Buy peacock feathers' for row in rows),
            "New to-do item did not appear in table"
        )
        # 页面中又显示了一个文本框，可以输入其他的待办事项
        # 她输入了“Use peacock feathers to make a fly”（使用孔雀羽毛做假蝇）
        # 伊迪丝做事很有条理
        self.fail('Finish the test!')

if __name__ == '__main__':
    unittest.main()
