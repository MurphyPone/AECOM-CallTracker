from flask import Flask, render_template
from utils import *
from datetime import datetime

app = Flask(__name__)

data = {
    "total": 0,
    "successful": 0,
    "missed": 0,
    "follow_up": 0
}
extract_from_csv(data)

driver = build_driver()         # Builds driver based on config
scrape(data, driver, build=True)

@app.route("/")
def home():
    minute = datetime.now().minute
    print(minute)
    if minute % 5 == 0:
        scrape(data, driver)

    return render_template("home.html", data=data)


if __name__ == "__main__":
    app.run(debug=True)
