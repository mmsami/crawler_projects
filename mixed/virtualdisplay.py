from pyvirtualdisplay import Display
from selenium import webdriver
import time

display = Display(visible=0, size=(800, 600))
display.start()
url = 'http://www.fec.gov/finance/disclosure/ftpdet.shtml'

# now Firefox will run in a virtual display.
# you will not see the browser.
browser = webdriver.Firefox()
browser.get(url)
time.sleep(5)
print browser.page_source
browser.quit()

display.stop()
