from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import urllib.request as ul 
import time
import json

driver = webdriver.Chrome()

links = []
with open('links.json', 'r') as file:
  file = json.load(file)
  for line in file['links']:
    links.append(line)

images = []
srcSet = []
f = open('imglinks.txt', 'w')

for url in links:
  try:
    driver.get(url)
    time.sleep(1)
    src = driver.page_source
    soup = BeautifulSoup(src, 'html.parser')
  
    div = soup.find('img', class_="FFVAD")
    images.append(div['src'])
    srcSet.append(div['srcset'])
    f.write(div.img['src'] + "\n")
  except Exception:
    pass

driver.quit()

print(images, '\n')

# cnt = 0

# for img in imgFiles:
#   r = requests.get(img)
#   with open(f"./img/img{cnt}.jpg", 'wb') as file:
#     file.write(r.content)
#   cnt += 1
