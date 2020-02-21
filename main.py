from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, render_template
from datetime import datetime
from config import *
from utils import * 
from buffer import * 
import atexit
import os 

app = Flask(__name__)

PATH = os.getcwd()
DOWNLOAD_PATH = PATH
EXECUTABLE_PATH = PATH

# Expand config based on OSwhich executable to build with
if OS == "Windows":
    EXECUTABLE_PATH = PATH + r"\drivers\geckodriver.exe"
    DOWNLOAD_PATH   = f"{PATH}\\downloads\\"
elif OS == "OSX":
    EXECUTABLE_PATH =  PATH + r"/drivers/geckodriver"
    DOWNLOAD_PATH   = f"{PATH}/downloads/"
elif OS == "Linux":
    EXECUTABLE_PATH =  PATH + r"/drivers/geckodriver_linux"
    DOWNLOAD_PATH   = f"{PATH}/downloads/"

data = {
    "date": "2020-01-27",
    "total": 0,
    "successful": 0,
    "missed": 0,
    "follow_up": 0,
    "coverage": -1
}

# Instantiate and load buffer from file
buffer = Buffer()
buffer.load("./static/Monthly Report.csv") 

@app.before_first_request
def config_driver():
    global driver
    driver = None

    if driver is None:
        print("Driver undefined...")
        driver = build_driver()                     # Builds driver based on config
        scrape(data, driver, buffer, build=True)
        print("Executed start up configurations...")


def do_scrape():
    print("Executing cron...")
    scrape(data, driver, buffer, build=False)

@app.route("/")
def home():
    return render_template("home.html", data=data)

if __name__ == "__main__":
    sched = BackgroundScheduler(daemon=True)
    cron = sched.add_job(do_scrape, 'interval', minutes=2)
    sched.start()
    
    # app.run() will call this script again...?
    if OS == "Windows" or "OSX":
        app.run(host="0.0.0.0", port=5000, debug=True)
    else: 
        app.run(host="0.0.0.0", port=80, debug=True)

