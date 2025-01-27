from selenium.webdriver.common.by import By
from time import sleep

from JobBase import JobBase
from Position import Position


class JobRbc(JobBase):
  def __init__(self):
    self.url = 'https://jobs.rbc.com/ca/en/rbctech'

  def get_root(self):
      return self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/div/div[3]/section/div/div/div/div[2]/div[2]/ul')

  def get(self, i):
      index = i * 5
      current_url = 'https://jobs.rbc.com/ca/en/rbctech?from=' + str(index) + '&s=1&rk=l-technology'
      self.driver.get(current_url)

  def filter(self, detail):
      if ('TORONTO' in detail.location) and self.has_keyord(detail, 'Java'):
          return False
      else:
          return True

  def get_job_details(self, root):
      subs = root.find_elements(By.CLASS_NAME, 'information')
      details = []
      for sub in subs:
          detail = Position()
          detail.title = sub.find_element(By.XPATH, './span').text
          detail.type = sub.find_element(By.XPATH, './span/a[@ph-tevent="job_click"]').get_attribute('data-ph-at-job-type-text')
          detail.location = sub.find_element(By.XPATH, './span/a[@ph-tevent="job_click"]').get_attribute('data-ph-at-job-location-area-text')
          detail.url = sub.find_element(By.XPATH, './span/a[@ph-tevent="job_click"]').get_attribute('href')
          detail.post_date = sub.find_element(By.XPATH, './span/a[@ph-tevent="job_click"]').get_attribute('data-ph-at-job-post-date-text')
          # detail.p
          details.append(detail)
          # print(sub.get_attribute('outerHTML'))
      return details

  def fill_detail(self, detail):
      detail.deadline = self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div/section/div/div[1]/section[2]/div/div[1]/div/div/div[3]/div[4]/span').text
      detail.platform = self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div/section/div/div[1]/section[2]/div/div[1]/div/div/div[3]/div[1]/span').text

  def has_keyord(self, detail, keyword):
      self.driver.get(detail.url)
      self.fill_detail(detail)
      return keyword in self.driver.find_element(By.XPATH, '/html').text
