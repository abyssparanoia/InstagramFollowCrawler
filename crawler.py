from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import quote_plus
import time
import pprint
import bs4


class InstagramFollowCrawler():

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def login(self, headless=False):
        if headless:
            self.options = Options()
            self.options.add_argument('--headless')
            self.driver = webdriver.Chrome(options=self.options)
        else:
            self.driver = webdriver.Chrome()

        self.driver.get('https://www.instagram.com/accounts/login/')
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "i24fI")))
        self.driver.find_element_by_xpath(
            "//div/input[@name='username']").send_keys(self.username)
        time.sleep(1)
        self.driver.find_element_by_xpath(
            "//div/input[@name='password']").send_keys(self.password)
        time.sleep(1)
        self.driver.find_element_by_xpath('//span/button').click()
        time.sleep(3)
        return True

    def following(self):
        self.followingList = []
        try:
            self.driver.get(
                "https://www.instagram.com/{0}/".format(self.username))
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "g47SY")))
            self.driver.find_element_by_partial_link_text("following").click()
            time.sleep(3)
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "FPmhX")))

            self.driver.execute_script(
                "followingbox = document.getElementsByClassName('j6cq2')[0];")
            self.last_height = self.driver.execute_script(
                "return followingbox.scrollHeight;")

            while True:
                self.driver.execute_script(
                    "followingbox.scrollTo(0, followingbox.scrollHeight);")

                time.sleep(10)
                self.new_height = self.driver.execute_script(
                    "return followingbox.scrollHeight;")

                if self.new_height == self.last_height:
                    break

                self.last_height = self.new_height
                self.soup = bs4.BeautifulSoup(self.driver.page_source, 'lxml')
                self.users = self.soup.find_all('a', class_='FPmhX')
                self.followingList.extend(self.users)

            time.sleep(3)

        finally:
            self.result_following = []
            for following in self.followingList:
                self.result_following.append(following.text)
            print('following is done!!!')
            return self.result_following

    def follower(self):
        self.followerList = []
        try:
            self.driver.get(
                "https://www.instagram.com/{0}/".format(self.username))
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "g47SY")))
            self.driver.find_element_by_partial_link_text("follower").click()
            time.sleep(3)
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "FPmhX")))

            self.driver.execute_script(
                "followersbox = document.getElementsByClassName('j6cq2')[0];")
            self.last_height = self.driver.execute_script(
                "return followersbox.scrollHeight;")

            while True:
                self.driver.execute_script(
                    "followersbox.scrollTo(0, followersbox.scrollHeight);")

                time.sleep(10)
                self.new_height = self.driver.execute_script(
                    "return followersbox.scrollHeight;")

                if self.new_height == self.last_height:
                    break

                self.last_height = self.new_height
                self.soup = bs4.BeautifulSoup(self.driver.page_source, 'lxml')
                self.users = self.soup.find_all('a', class_='FPmhX')
                self.followerList.extend(self.users)

            time.sleep(3)

        finally:
            self.result_follower = []
            for follower in self.followerList:
                self.result_follower.append(follower.text)
            print('follower is done!!!!')
            return self.result_follower

    def __del__(self):
        self.driver.close()
        self.driver.quit()
