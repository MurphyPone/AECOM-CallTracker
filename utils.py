from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from config import *
from datetime import date
from datetime import timedelta
from copy import deepcopy
import pandas as pd
import math
import time
import json
import os

# Remove old files if present
def clean_up():
    try:
        os.remove("downloads/Export_dashboard.csv")
        os.remove("downloads/Export_dashboard(1).csv")
        os.remove("downloads/Export_dashboard(2).csv")
    except FileNotFoundError:
        print("One or more of the files was not found, fetching new files")

# Configure web driver
def build_driver():
    fp = webdriver.FirefoxProfile()
    fp.set_preference("browser.download.folderList", 2)
    fp.set_preference("browser.download.dir", DOWNLOAD_PATH)
    fp.set_preference("browser.helperApps.neverAsk.openFile", "application/csv, txt/csv")
    fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/csv, txt/csv, text/csv, attachment/csv, multipart/form-data")

    return webdriver.Firefox(firefox_profile=fp, executable_path=EXECUTABLE_PATH)

def login(driver):
    # Navigate to and login
    driver.get(URL)
    driver.set_window_size(1173, 817)
    driver.find_element(By.ID, "user_email1").click()
    driver.find_element(By.ID, "user_email1").send_keys(USERNAME)
    driver.find_element(By.CSS_SELECTOR, "html").click()
    driver.find_element(By.ID, "user_password").click()
    driver.find_element(By.ID, "user_password").send_keys(PASSWORD)
    driver.find_element(By.ID, "user_password").submit()
    driver.execute_script("window.scrollTo(0,0)")

    # Nav to dashboard
    time.sleep(10)
    driver.find_element(By.ID, "dashboard-button").click()
    time.sleep(10)

def fix_dates(driver):
    end_date = driver.find_element_by_xpath("//*[contains(@ng-click, 'openedEndDate ')]")
    start_date = driver.find_element_by_xpath("//*[contains(@ng-click, 'openedStartDate ')]")

    end_date_val = date.fromisoformat(end_date.get_attribute('value')) # Date object
    start_date_val = deepcopy(end_date_val)
    end_date_val = end_date_val + timedelta(days=1)
    # print("Start date: ", start_date_val, "End date: ", end_date_val)

    start_date.clear()
    end_date.clear()

    start_date.send_keys(start_date_val.isoformat())
    end_date.send_keys(end_date_val.isoformat())

# Gets .csv logging missed calls
def first_bucket(driver, filters, download, apply):
    driver.find_elements_by_xpath("//*[contains(@ng-click, 'onClickQueueFilter')]")[5].click()
    apply.click()
    time.sleep(5)
    download.click()

    # clear filters Repeat
    driver.find_elements_by_xpath("//*[contains(text(), 'clear')]")[21].click()
    filters.click()
    time.sleep(1)

# Gets .csv logging successful calls
def second_bucket(driver, filters, download, apply):
    driver.find_elements_by_xpath("//*[contains(@ng-click, 'onClickQueueFilter')]")[2].click()
    driver.find_elements_by_xpath("//*[contains(@ng-click, 'onClickQueueFilter')]")[4].click()
    driver.find_elements_by_xpath("//*[contains(@ng-click, 'onClickQueueFilter')]")[6].click()
    apply.click()
    time.sleep(5)
    download.click()

    # clear filters Repeat
    driver.find_elements_by_xpath("//*[contains(text(), 'clear')]")[23].click()             # For whatever reason the number of clears increases...
    filters.click()
    time.sleep(1)

def third_bucket(driver, filters, download, apply):
    driver.find_elements_by_xpath("//*[contains(@ng-click, 'onClickQueueFilter')]")[3].click()
    time.sleep(5)
    download.click()

def download_files(driver):
    # Instantiate common elements
    filters = driver.find_element_by_xpath("//*[contains(text(), '+filters')]")
    download = driver.find_element_by_xpath("//*[contains(@ng-click, 'activateOnDownloadCsv')]")
    filters.click()
    apply = driver.find_element_by_xpath("//*[contains(@ng-click, 'applyFilterBox()')]")
    time.sleep(1)

    first_bucket(driver, filters, download, apply)  # Get first .csv
    second_bucket(driver, filters, download, apply) # Get second .csv
    third_bucket(driver, filters, download, apply)  # Get third .csv

def extract_from_csv(data):
    for filename in os.listdir(DOWNLOAD_PATH):
        try:
            d = pd.read_csv(DOWNLOAD_PATH+ "/" +str(filename), usecols=['Title of Report'])
        except FileNotFoundError:
            print("One or more of the files was not found, fetching new files")

        if filename == "Export_dashboard.csv":
            data['missed'] = int(d['Title of Report'][5])
        if filename == "Export_dashboard(1).csv":
            data['successful'] = int(d['Title of Report'][5])
        if filename == "Export_dashboard(2).csv":
            data['follow_up'] = int(d['Title of Report'][5])

        data['total'] = data['missed'] + data['successful']

def scrape(data, driver, build=False):
    print(data)
    clean_up()                      # delete old files if present
    if build == True:
        login(driver)                   # Logs in and navigates to dashboard
    else:
        fix_dates(driver)               # sets the daterange to today + tomorrow
        download_files(driver)          # Downloads the three .csv files
        extract_from_csv(data)          # Extracts relevant fields from the downloaded files
    print(data)
