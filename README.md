# AECOM-CallTracker
Simple automated analysis of customer service calls

# Requirements

`pip install selenium pandas`

# Use
Some user-specific information is required to run the script.  Create a file in the root directory of this folder called `config.py` and include the fields below

```
# config.py
URL = "https://teamaecompr.mojohelpdesk.com/login"
USERNAME = "user@email.com"
PASSWORD = "hunter12"
DOWNLOAD_PATH = f"C:\\Users\\user_name\\path\\to\\AECOM-CallTracker\\downloads"
EXECUTABLE_PATH = r'"C:\\Users\\user_name\\path\\to\\AECOM-CallTracker\\geckodriver.exe'
```

# Tips
In
web debugging: `$x("//*[contains(text(), 'Follow Up Calls_f')]")`


# TODO
- Webpage formatting with logos
- Refresh page when calling global scrape method
  - either use a timer, a <meta tag>, or manual refresh
  - ensure duplicate windows are not created
- Make sure the spanish translations match up
