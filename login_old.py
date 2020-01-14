import config
from robobrowser import RoboBrowser
import time

# session = Session()
browser = RoboBrowser(parser='html.parser')     # create RB object to extract HTML from URL
browser.open(config.URL)    # navigate to given URL (for Yesterday's records)

# login
form = browser.get_form(action="/vocalls/inbound/csv?destination=vocalls/inbound/csv")   # get the form from the login page
form['name'].value = config.USERNAME     # populate relevant fields by HTML ID, note these are subject to change
form['pass'].value = config.PASSWORD
browser.submit_form(form)        # submit the form -> should be on the /

time.sleep(30) # wait 30 seconds to ensure that the CSV has loaded

# repeat this until a get specific tag yields expected results?
browser.follow_link(browser.get_link())

# TODO Current problem:
#   Even when the page gets to 100% loading, the url doesn't update, whereas when
#   manually navigating, once the export finishes, the url changes to something like:
#
#       'https://mybilling.zonatel.com:8082/vocalls/inbound/csv/294841/all?eid=26&token=fh4gi58j7Hb11252Sgmcu2LVTaBIigyoH6pm4YumPJo&return-url=vocalls'
#
#   Where the token is (I'm assuming) a b64 hash including info about our query/user info?
#
#   But from within my bot client, the url remains:
#
#          'https://mybilling.zonatel.com:8082/batch?op=start&id=710#main-content'
#
#          -- #main-content is just used to "refresh" the page
#
#  It gets stuck on the download page
#
#           <div class="percentage pull-right">100%</div>
#           <div class="message">Export is starting up.<br/> <br/></div>
#
#   If possible, simply injecting the download link to that page rather than seamlessly redirecting to a new url ?
#
#   Or, add a link on that page with the new url right before redirecting so I could try to follow it?  Manual users would simply be redirected




# Check for download link
# browser.get_link()


for div in browser.find_all('div', {"class": "percentage pull-right"}):
    progress = str(div)
    start = progress.index(">")
    end = progress.index("</")
    progress = progress[start+1:end:1]
    ## Sooooo... The browser object never updates once it's on this page...
