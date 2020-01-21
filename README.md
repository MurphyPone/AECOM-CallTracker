# AECOM-CallTracker
This project is a twofold effort to provide simple data analysis of a call center team's activity.  The first portion of the project contains a webscraping utility which routinely pulls data from one of the call center's intermediary tracking websites, processes the gathered data, and feeds it into the second portion of the project which displays the data on a simple flask web page.

# Requirements

Required modules for this project can be installed by running the following command from the command line at the root directory of this project:

`pip install -r requirements.txt`

FireFox is also necessary to execute this project.  The WebDrivers associated with the version of this project are included in this repository as under `drivers/geckodriver...`

# Use
Some user-specific information is required to run the script.  Create a file in the root directory of this folder called `config.py` and include the fields below

```
# config.py
URL = "https://teamaecompr.mojohelpdesk.com/login"
USERNAME = "user@email.com"
PASSWORD = "hunter12"
OS = "Windows"          # Options include "Windows", "OSX", "Linux"
```

Once the config has been filled out, the script can be executed by typing:

`python main.py`

in the command line from the root directory.  This will run the build and run scraper utility if it has not already been built, and then it will launch the web page which can be viewed locally at `localhost:5000` or `127.0.0.1:5000`.

# Tips
In case one of the elements on the desired page changes location, CSS attribute name, identifier, etc. the following command can be executed in the web developer console to help identify the new identification solution:


`$x("//*[contains(text(), '<text_of_element>')]")`


# TODO
- [x] Webpage formatting with logos
- [ ] Refresh page when calling global scrape method
  - [x] either use a timer, a `<meta http-equiv="refresh" content="60">` tag, or manual refresh
  - [ ] ensure duplicate windows are not created -- suspect that `app.run(debug=True)` in `main.py` is source of issue
- [ ] Make sure the spanish translations match up
- [ ] Add try/Catch statements around each element query
    - [ ] Click each previous filter in filter box rather than "clear" button...
- [x] Add OSX support
- [ ] Add Linux support for hosting on an AWS instance
- [ ] Resolve `selenium.common.exceptions.WebDriverException: Message: Failed to decode response from marionette` 

# Known Bugs
- Filter clear button index changes occasionally depending on how many active elements are on screen
- Per [the geckodriver repo](https://github.com/mozilla/geckodriver/releases):
    > macOS 10.15 (Catalina):
    >
    >Due to the recent requirement from Apple that all programs must
    be notarized, geckodriver will not work on Catalina if you manually
    download it through another notarized program, such as Firefox.
    >
    >Whilst we are working on a repackaging fix for this problem, you
    can find more details on how to work around this issue in the
    macOS notarization section of the documentation.

    but this script _should_ work for older releases of macOS version <= 10.14 (Mojave)

