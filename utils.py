from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from main import PATH, DOWNLOAD_PATH, EXECUTABLE_PATH, OS
from config import *
    
from datetime import timedelta
from datetime import date
from copy import deepcopy
import pandas as pd
import math
import time
import json
import sys
import os


# Remove old files if present
def clean_up():
    for filename in os.listdir(DOWNLOAD_PATH):
        if ".gitkeep" not in filename:
            try:
                os.remove(DOWNLOAD_PATH + str(filename))
            except FileNotFoundError:
                print(f"{DOWNLOAD_PATH + str(filename)} was not found, fetching new files")
        else: 
            pass


# Configure web driver
def build_driver():
    print("building driver..")

    fp = webdriver.FirefoxProfile()
    fp.set_preference("browser.download.folderList", 2)
    fp.set_preference("browser.download.dir", DOWNLOAD_PATH)
    fp.set_preference("browser.helperApps.neverAsk.openFile", "application/csv, txt/csv")
    fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/csv, txt/csv, text/csv, attachment/csv, multipart/form-data")
    
    cap = DesiredCapabilities().FIREFOX
    cap["marionette"] = True

    if OS == "Linux":
        print("building for AWS")
        from selenium.webdriver.firefox.firefox_binary import FirefoxBinary 
        from selenium.webdriver.firefox.options import Options

        options = Options()
        options.headless = True # No display
        print(PATH+'/drivers/firefox/firefox-bin', PATH+'/drivers/firefox/firefox-bin.log')
        BINARY = FirefoxBinary(firefox_path=PATH+'/drivers/firefox/firefox-bin', log_file=PATH+'/drivers/firefox/firefox-bin.log')
        # binary = FirefoxBinary(PATH+'/drivers/firefox/firefox')    # probably needs to be custom configured
        return webdriver.Firefox(firefox_profile=fp, firefox_binary=BINARY, options=options, capabilities=cap, executable_path=EXECUTABLE_PATH)
   
    else: 
        return webdriver.Firefox(firefox_profile=fp, capabilities=cap, executable_path=EXECUTABLE_PATH)

# Used to delete old Firefox windows if they exist
def delete_old(driver):
    driver.current_window_handle
    handles = list(driver.window_handles)
    print(f"Handles: {handles}")
    
    if len(handles) > 1:
        for i in range(1, len(handles)):
            handles.remove(handles[i])
            print("Removed duplicate window")

    assert len(handles) == 1

    driver.switch_to_window(handles[0])
    # do your stuffs
    # driver.close()
    # driver.switch_to_window(default_handle)


def login(driver):
    # Navigate to and login
    driver.get(URL)
    driver.set_window_size(1200, 800)
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
    filters.click()
    time.sleep(1)
    driver.find_elements_by_xpath("//*[contains(@ng-click, 'onClickQueueFilter')]")[5].click()
    apply.click()
    time.sleep(5)
    download.click()
    time.sleep(2)

    # clear filters Repeat -- driver.find_elements_by_xpath("//*[contains(text(), 'clear')]")[21].click()
    filters.click()
    time.sleep(1)
    driver.find_elements_by_xpath("//*[contains(@ng-click, 'onClickQueueFilter')]")[5].click()
    time.sleep(2)
    apply.click()
    time.sleep(5)


# Gets .csv logging successful calls
def second_bucket(driver, filters, download, apply):
    filters.click()
    time.sleep(1)
    driver.find_elements_by_xpath("//*[contains(@ng-click, 'onClickQueueFilter')]")[2].click()
    driver.find_elements_by_xpath("//*[contains(@ng-click, 'onClickQueueFilter')]")[4].click()
    driver.find_elements_by_xpath("//*[contains(@ng-click, 'onClickQueueFilter')]")[6].click()
    apply.click()
    time.sleep(5)
    download.click()
    time.sleep(2)

    # clear filters Repeat -- driver.find_elements_by_xpath("//*[contains(text(), 'clear')]")[23].click() 
    filters.click()
    time.sleep(1)
    driver.find_elements_by_xpath("//*[contains(@ng-click, 'onClickQueueFilter')]")[2].click()
    driver.find_elements_by_xpath("//*[contains(@ng-click, 'onClickQueueFilter')]")[4].click()
    driver.find_elements_by_xpath("//*[contains(@ng-click, 'onClickQueueFilter')]")[6].click()    
    time.sleep(2)
    apply.click()
    time.sleep(5)


# Gets .csv logging follow up calls
def third_bucket(driver, filters, download, apply):
    filters.click()
    time.sleep(5)
    driver.find_elements_by_xpath("//*[contains(@ng-click, 'onClickQueueFilter')]")[3].click()
    apply.click()
    time.sleep(5)
    download.click()

    # Clears filters -- driver.find_elements_by_xpath("//*[contains(text(), 'clear')]")[21].click()
    filters.click()
    time.sleep(1)
    driver.find_elements_by_xpath("//*[contains(@ng-click, 'onClickQueueFilter')]")[3].click()
    time.sleep(2)
    apply.click()
    time.sleep(5)
    

def download_files(driver):
    # Instantiate common elements
    filters = driver.find_element_by_xpath("//*[contains(text(), '+filters')]")
    download = driver.find_element_by_xpath("//*[contains(@ng-click, 'activateOnDownloadCsv')]")
    apply = driver.find_element_by_xpath("//*[contains(@ng-click, 'applyFilterBox()')]")
    time.sleep(2)

    first_bucket(driver, filters, download, apply)  # Get first .csv
    second_bucket(driver, filters, download, apply) # Get second .csv
    third_bucket(driver, filters, download, apply)  # Get third .csv


def extract_from_csv(data):
    print("Extracting data from .csv files...")
    for filename in os.listdir(DOWNLOAD_PATH):    
        if ".gitkeep" not in filename:
            try:
                #print(filename)
                d = pd.read_csv(DOWNLOAD_PATH + str(filename), usecols=["Title of Report"])
                #print(d['Title of Report'][3], int(d['Title of Report'][5]) )
            except FileNotFoundError:
                print(f"{filename} was not found, fetching new files")

            if d['Title of Report'][3] == "Missed Call_m":
                data['missed'] = int(d['Title of Report'][5])
            if d['Title of Report'][3] == "Damage Assessment_d":
                data['successful'] = int(d['Title of Report'][5])
            if d['Title of Report'][3] == "Follow Up Calls_f":
                data['follow_up'] = int(d['Title of Report'][5])

            data['total'] = data['missed'] + data['successful']

            if data['total'] == 0:
                    data['coverage'] = 0
            else:
                data['coverage'] = int((data['successful'] / data['total']) * 100)
        else: 
            pass


def scrape(data, driver, build=False):    
    if build == True:
        extract_from_csv(data)
        login(driver)                   # Logs in and navigates to dashboard
        fix_dates(driver)               # sets the daterange to today + tomorrow # TODO may need to be moved
    # else: 
        # try: 
        #     driver.close()
        #     print(driver.window_handles)
        # except:
        #     pass  
    
    # delete_old(driver)
    clean_up()                          # delete old files if present
    download_files(driver)              # Downloads the three .csv files
    extract_from_csv(data)              # Extracts relevant fields from the downloaded files
