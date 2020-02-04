# AECOM-CallTracker
This project is a twofold effort to provide simple data analysis of a call center team's activity.  The first portion of the project contains a webscraping utility which routinely pulls data from one of the call center's intermediary tracking websites, processes the gathered data, and feeds it into the second portion of the project which displays the data on a simple flask web page.

# Requirements

Required modules for this project can be installed by running the following command from the command line at the root directory of this project:

`pip install -r requirements.txt`

FireFox is also necessary to execute this project.  The WebDrivers associated with the version of this project are included in this repository as under `drivers/geckodriver...`

Additional installation steps are necessary for this project to run in an AWS EC2 instace, see the section labled **AWS EC2 Installation** for more information

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
- [x] Refresh page when calling global scrape method
  - [x] either use a timer, a `<meta http-equiv="refresh" content="60">` tag, or manual refresh
- [x] Add try/Catch statements around each element query
    - [x] Click each previous filter in filter box rather than "clear" button...
    - [x] Parse .csv files by filter tags rather than filename
- [ ] Additional support:
    - [x] Add OSX support
    - [x] Add Linux support for hosting on an AWS instance
- [ ] Localize images
- [ ] rollover totals by new day
- [x] Ensure duplicate windows are not created -- suspect that `app.run(debug=True)` in `main.py` is source of issue
- [ ] Figure out how to invoke a request on startup so that the window is created without needing to refresh the `localhost:5000` page
    - [x] Ensure that the page is actually auto-updating
- [ ] Track month long data in a csv matrix with day columns and row value
    - [ ] Use a buffer dequeue buffer of len(30) that saves each update
- [ ] Make sure the spanish translations match up
- [ ] Resolve `selenium.common.exceptions.WebDriverException: Message: Failed to decode response from marionette` 
- [ ] Tweak the execution time
- [ ] Duplicate downloads 
- [ ] Must refresh before cron executes otherwise it will try to scrape with no driver

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

# AWS EC2 Installation
1. Connect to the EC2 instance:
    - Generate a new key-pair or request access to the private key for secure shh access by filing an issue on this repo
    - Modify the local permissions of the file via `sudo chmod 400 private_key.pem`
    - Execute the command `ssh -i private_key.pem ec2-user@ec2-3-134-98-107.us-east-2.compute.amazonaws.com` 
        - Note that the Public (IPv4) DNS address (the portion following the `@` in the above command), may be different 
2. Install git on the container if it is not already: `sudo yum update -y`, `sudo yum install git`
3. Install Python 3.7.1 as well as it's dependencies following [this tutorial](https://tecadmin.net/install-python-3-7-amazon-linux/) 
    - Note that unless aliased in the `~/.bashrc` or `~/.bash_profile`, the command `python` will invoke version 2.7.x.  Instead we will use the command `python3.7` to explicitly specify which version we want to use
    - Further note that you can verify your python installation with `sudo python3.7 -V`.  **It is important to make sure that Python 3.7 is installed as root because we need to call the script as root in order to serve the Flask webpage to port 80.
4. This is a hacky workaround for using Python 3.7 as root which specifies which version to use and temporarily appends it to the root path (which is different than the ec2-user's path): `sudo env "PATH=$PATH" /usr/local/bin/pip3.7 install --user -r requirements.txt`, similarly we can specify Python 3.7 with: `sudo env "PATH=$PATH" /usr/local/bin/python3.7 main.py`
5. Install `lszma` for pandas: `yum install -y xz-devel`
    - Also fixed issues on Ubuntu where _bz2 was not found. Resolved by manually downloading bzip-2, reconfiguring and recompiling python
6. ONLY FOR AMI Install GTK+ to our Firefox installation as it is not enabled by default by following [this article](https://joekiller.com/2012/06/03/install-firefox-on-amazon-linux-x86_64-compiling-gtk/)
    - Alternatively on Ubuntu, use: `sudo apt-get install dbus-x11` and `sudo apt install xvfb` for a virtual frame buffer
        - To use the Xvfb: `export DISPLAY=:10 && sudo Xvfb :10 -screen scrn 1200x800x24 &` 
7. Finally, we can execute the script using the workaround mentioned above: `sudo env "PATH=$PATH" python3.7 main.py` 

