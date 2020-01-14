# from selenium.webdriver import Chrome
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import pandas as pd
import config

# Selenium config
chrome_driver = "/Users/petermurphy/github/AECOM-CallTracker/chromedriver"
driver = webdriver.Chrome(chrome_driver)

# Login
username = driver.find_element_by_id("user_email1")
password = driver.find_element_by_id("user_password")

username.send_keys(USERNAME)
password.send_keys(PASSWORD)

driver.find_element_by_class_name('btn').click()
driver.find_element_by_name("submit").click()

# Nav to dashboard
driver.get("https://teamaecompr.mojohelpdesk.com/ma/#/dashboard")

# Click on the filter
driver.find_element_by_link_text('+filters').click()

# Select and apply filters
dmg_assess = driver.find_element_by_xpath('//button[normalize-space()="Damage Assessment"]')
intake = driver.find_element_by_xpath('//button[normalize-space()="Intake/Eligibility"]')
status = driver.find_element_by_xpath('//button[normalize-space()="Status Checks"]')

driver.execute_script("arguments[0].click(); arguments[1].click(); arguments[2].click();", dmg_assess, intake, status)

apply = driver.find_element_by_xpath('//button[normalize-space()="Apply"]')
driver.execute_script("arguments[0].click();", apply)



print(browser.parsed())
