from selenium import webdriver
from bs4 import BeautifulSoup
from PIL import Image
import requests
from io import BytesIO
import geckodriver_autoinstaller
import time
import shutil

def get_images():
  geckodriver_autoinstaller.install() 
  driver = webdriver.Firefox()
  base_url = 'https://www.archdaily.com/search/projects/categories/residential-architecture?page='
  counter = 3231
  for i in range(322,900):
      requested_url = base_url + str(i)
      driver.get(requested_url)
      time.sleep(5)
      soup = BeautifulSoup(driver.page_source, 'html.parser')
      images = soup.findAll('img', {'class': 'swiper-lazy-loaded'})

      for image in images:
          image_link = image['src']
          try:
              image_value = Image.open(BytesIO(requests.get(image_link).content)).convert('RGB')
              width, height = image_value.size
              if width >= 512 and height >= 512:
                  if height % 2 == 0:
                      top = (height - 512) / 2 - 1
                      bottom = top + 512
                  else:
                      top = (height - 513) / 2 - 1
                      bottom = top + 512
                  if width % 2 == 0:
                      left = (width - 512) / 2 - 1
                      right = left + 512
                  else:
                      top = (width - 513) / 2 - 1
                      bottom = top + 512
                  cropped_image = image_value.crop((left, top, right, bottom))
                  saved_image = cropped_image.save('trainingImages/' + str(counter) + '.jpg')
                  counter += 1
          except:
              pass

  driver.close()
  shutil.make_archive('trainingImages', 'zip', 'trainingImages')
  
  
 
