from flask import Flask, render_template
from utils import *
from datetime import datetime
import atexit
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

data = {
    "total": 0,
    "successful": 0,
    "missed": 0,
    "follow_up": 0,
    "coverage": 90
}

# @app.before_first_request
# def on_start():
#     extract_from_csv(data)
#     global driver
#     driver = build_driver()         # Builds driver based on config
#     scrape(data, driver, build=True)
#     sched = BackgroundScheduler(daemon=True)
#     cron = sched.add_job(do_scrape, 'interval', minutes=2)
#     sched.start()
#     print("Executed start up configurations...")

def do_scrape():
    print("Executing cron...")
    scrape(data, driver, build=False)

@app.route("/")
def home():
    return render_template("home.html", data=data)


if __name__ == "__main__":
    extract_from_csv(data)
    global driver
    driver = build_driver()         # Builds driver based on config
    scrape(data, driver, build=True)
    sched = BackgroundScheduler(daemon=True)
    cron = sched.add_job(do_scrape, 'interval', minutes=2)
    sched.start()
    print("Executed start up configurations...")

    app.run(debug=True)
