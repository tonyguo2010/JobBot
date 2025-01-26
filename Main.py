import sys

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from time import sleep


# Set options for not prompting DevTools information
from JobRbc import JobRbc

options = Options()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_argument("--start-maximized")

driver = webdriver.Chrome(options=options)

jobs = []
jobs.append(JobRbc())
# driver.get("http://www.google.ca")
for job in jobs:
    job.set_driver(driver)
    job.collect_job();

# Close the driver
driver.quit()
