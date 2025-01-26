from selenium.webdriver.common.by import By
from time import sleep

from JobBase import JobBase
from Position import Position


class JobRbc(JobBase):
  def __init__(self):
    self.url = 'https://jobs.rbc.com/ca/en/rbctech'

  def get_root(self):
      return self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/div/div[3]/section/div/div/div/div[2]/div[2]/ul')

  def filter(self, detail):
      if 'TORONTO' not in detail.location:
          return True
      else:
          return False

  def get_job_details(self, root):
      subs = root.find_elements(By.CLASS_NAME, 'information')
      details = []
      for sub in subs:
          detail = Position()
          detail.title = sub.find_element(By.XPATH, './span').text
          detail.type = sub.find_element(By.XPATH, '//a[@ph-tevent="job_click"]').get_attribute('data-ph-at-job-type-text')
          detail.location = sub.find_element(By.XPATH, '//a[@ph-tevent="job_click"]').get_attribute('data-ph-at-job-location-area-text')
          # detail.p
          details.append(detail)
      return details