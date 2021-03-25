from selenium.webdriver.chrome.webdriver import WebDriver

from django.test import LiveServerTestCase


class TitleTest(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):  # set up selenium for test
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)


    @classmethod
    def tearDownClass(cls): # stop the application after test is done running
        cls.selenium.quit()
        super().tearDownClass()


    def test_title_on_home_page(self): # test to make sure that the home page title is displayed
        self.selenium.get(self.live_server_url)
        self.assertIn('Travel Wishlist', self.selenium.title)


class AddPlacesTest(LiveServerTestCase):

    fixtures = ['test_places'] # add test data to the database

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)


    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()


    def test_add_new_place(self):

        self.selenium.get(self.live_server_url)
        input_name = self.selenium.find_element_by_id('id_name') 
        input_name.send_keys('Denver') # add a sample place to the list

        add_button = self.selenium.find_element_by_id('add-new-place') 
        add_button.click() # initiate a click event for add-new-place

        denver = self.selenium.find_element_by_id('place-name-5')
        self.assertEqual('Denver', denver.text) 

        # Make sure the expected places are in the list
        self.assertIn('Denver', self.selenium.page_source) 
        self.assertIn('New York', self.selenium.page_source)
        self.assertIn('Tokyo', self.selenium.page_source)
        

