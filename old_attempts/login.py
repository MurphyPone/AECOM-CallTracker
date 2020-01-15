import config
from robobrowser import RoboBrowser
import time

# session = Session()
browser = RoboBrowser(parser='html.parser')     # create RB object to extract HTML from URL
browser.open(config.URL)    # navigate to given URL (for Yesterday's records)

# login
form = browser.get_form()   # get the form from the login page
form['user[email]'].value = config.USERNAME
form['user[password]'].value = config.PASSWORD

browser.submit_form(form)

# from here, not sure how to navigate to the relevant
#   page.  Stuck on html page that says loading.
#   Not sure how to "refresh" page
