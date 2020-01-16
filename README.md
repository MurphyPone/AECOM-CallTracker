# AECOM-CallTracker
This project is a twofold effort to provide simple data analysis of a call center team's activity.  The first portion of the project contains a webscraping utility which routinely pulls data from one of the call center's intermediary tracking websites, processes the gathered data, and feeds it into the second portion of the project which displays the data on a simple flask web page. 

# Requirements

Required modules for this project can be installed by running the following command from the command line at the root directory of this project:

`pip install -r requirements.txt`

# Use
Some user-specific information is required to run the script.  Create a file in the root directory of this folder called `config.py` and include the fields below

```
# config.py
URL = "https://teamaecompr.mojohelpdesk.com/login"
USERNAME = "user@email.com"
PASSWORD = "hunter12"
DOWNLOAD_PATH = f"C:\\Users\\user_name\\path\\to\\AECOM-CallTracker\\downloads"
EXECUTABLE_PATH = r'C:\\Users\\user_name\\path\\to\\AECOM-CallTracker\\geckodriver.exe'
```

Once the config has been filled out, the script can be executed by typing:

`python main.py`

in the command line from the root directory.  This will run the build and run scraper utility if it has not already been built, and then it will launch the web page which can be viewed locally at `localhost:5000` or `127.0.0.1:5000`.

# Tips
In case one of the elements on the desired page changes location, CSS attribute name, identifier, etc. the following command can be executed in the web developer console to help identify the new identification solution:


`$x("//*[contains(text(), '<text_of_element>')]")`


# TODO
- Webpage formatting with logos
- Refresh page when calling global scrape method
  - either use a timer, a <meta tag>, or manual refresh
  - ensure duplicate windows are not created
- Make sure the spanish translations match up
