from selenium.webdriver.common.by import By


class JobBase:
  def __init__(self):
    self.url = ''

  def set_driver(self, driver):
      self.driver = driver

  def collect_job(self):
      self.driver.get(self.url)
      root = self.get_root()
      details = self.get_job_details(root)
      for detail in details:
          if (self.filter(detail)):
              continue
          print(detail.title)
          print(detail.type)
          print(detail.location)

  def get_root(self):
        raise NotImplementedError("Subclasses must implement this method")


  def get_job_details(self, root):
        raise NotImplementedError("Subclasses must implement this method")

  def filter(self, detail):
      raise NotImplementedError("Subclasses must implement this method")
