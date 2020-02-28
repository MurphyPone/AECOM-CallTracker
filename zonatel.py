# Generated by Selenium IDE
#import pytest
import time
import json

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import config

# Globals that would need to be configured
executable_path = r'F:\Users\Peter\Documents\Zonatel_scraper\Zonatel_scraper\geckodriver.exe'

fp = webdriver.FirefoxProfile()
fp.set_preference("browser.download.folderList", 2)
fp.set_preference("browser.download.dir", "F:\\Users\\Peter\\Documents\\Zonatel_scraper\\Zonatel_scraper\\downloads")
fp.set_preference("browser.helperApps.neverAsk.openFile", "application/csv, txt/csv")
fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/csv, txt/csv, multipart/form-data")

driver = webdriver.Firefox(firefox_profile=fp, executable_path=executable_path)


driver.get("https://mybilling.zonatel.com:8444/index.html")
driver.set_window_size(1173, 817)
driver.find_element(By.ID, "pb_auth_user").click()
driver.find_element(By.ID, "pb_auth_user").send_keys("USERNAME")
driver.find_element(By.NAME, "log").click()
driver.find_element(By.CSS_SELECTOR, "html").click()
driver.find_element(By.ID, "pb_auth_password").click()
driver.find_element(By.ID, "pb_auth_password").send_keys("PASSWORD")
driver.find_element(By.CSS_SELECTOR, ".tabFormButton").click()
driver.execute_script("window.scrollTo(0,0)")

time.sleep(5)
#WebDriverWait(driver, 10).until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, "#ext-gen119 .x-tab-strip-text")))
driver.find_element(By.CSS_SELECTOR, "#ext-gen119 .x-tab-strip-text").click()
time.sleep(5)
#WebDriverWait(driver, 10).until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, ".x-tree-node-over > .x-tree-node-anchor > span")))
#driver.find_element(By.CSS_SELECTOR, ".x-tree-node-over > .x-tree-node-anchor > span").click()

element = driver.find_element(By.ID, "ext-gen419")
actions = ActionChains(driver)
actions.move_to_element(element).perform()
time.sleep(5)
driver.find_element(By.CSS_SELECTOR, "#ext-gen425 > div:nth-child(1) > li:nth-child(4) > div:nth-child(1) > a:nth-child(4) > span:nth-child(1)").click()
#driver.execute_script("window.scrollTo(0,0)")
time.sleep(5)
driver.find_element(By.CSS_SELECTOR, "div.x-grid3-row:nth-child(14) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > div:nth-child(1) > a:nth-child(1) > img:nth-child(1)").click()
time.sleep(5)
driver.find_element(By.CSS_SELECTOR, "#ext-gen560 > em:nth-child(1) > span:nth-child(1) > span:nth-child(1)").click()
element = driver.find_element(By.CSS_SELECTOR, "body")
actions = ActionChains(driver)
#actions.move_to_element(element, 0, 0).perform()
time.sleep(5)
driver.find_element(By.CSS_SELECTOR, "#ext-gen935 > div:nth-child(1) > li:nth-child(7) > div:nth-child(1) > a:nth-child(4) > span:nth-child(1)").click()
time.sleep(5)
driver.find_element(By.CSS_SELECTOR, "#ext-gen1153").click()

#driver.find_element(By.ID, "x-form-el-ext-comp-1364").send_keys("23:59:59")     # Change hours to be hours of the day
driver.find_element_by_xpath("//*[contains(text(), 'Show Records')]").click()  # Click show records to reveal download
time.sleep(3)
driver.find_element_by_xpath("//*[contains(text(), 'Download')]").click()  # Click download
print("downloading...\n")
time.sleep(30)
