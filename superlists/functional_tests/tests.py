import time
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase



class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # 访问网站时，不用硬编码的本地地址（localhost:8000）
        self.browser.get(self.live_server_url)
        time.sleep(3)
        # 她注意到网页的标题和头部都包含“To-Do”这个词
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)


        # 应用邀请她输入一个待办事项
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'),
                         'Enter a to-do item')

        # 她在一个文本框中输入了“Buy peacock feathers”（购买孔雀羽毛）
        # 伊迪丝的爱好是使用假蝇做鱼饵钓鱼
        # 她按回车键后，页面更新了
        # 待办事项表格中显示了“1: Buy peacock feathers”
        # Keys 是发送回车键等特殊的按键
        # 按下回车键后页面会刷新。time.sleep 的作用是等待页面加载完毕，这样才能针对新页面下断言。
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Buy peacock feathers")

        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table("1: Buy peacock feathers")
        self.wait_for_row_in_list_table("2: Use peacock feathers to make a fly")
        # 伊迪丝想知道这个网站是否会记住她的清单
        # 她看到网站为她生成了一个唯一的URL
        # 页面中有一些解说这个功能的文字
        self.fail('Finish the test!')

    def wait_for_row_in_list_table(self, row_text):
        MAX_WAIT = 10
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.25)

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # 伊迪丝新建一个待办事项清单
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy peacock feathers')
        # 她注意到清单有个唯一的URL
        edith_list_url = self.browser.current_url
        ## assertRegex 用于检查字符串是否匹配正则表达式。我们利用它检查新的
        self.assertRegex(edith_list_url, '/lists/.+')

        ## 确保伊迪丝的信息不会从cookie中泄露出去
        self.browser.quit()
        self.browser = webdriver.Firefox()
        # 页面中看不到伊迪丝的清单
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        # 弗朗西斯输入一个新待办事项，新建一个清单# 他不像伊迪丝那样兴趣盎然
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        # 弗朗西斯获得了他的唯一URL
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        # 这个页面还是没有伊迪丝的清单
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)