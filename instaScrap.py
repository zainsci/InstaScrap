from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time, re, json, os


# Setting Driver
chrome_options =Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(chrome_options=chrome_options)

# Url For InstaPage
username = ""
url = f"https://www.instagram.com/{username}/"

# Scrolling Down The Page To Get More Results
ht = 1080
webPage = driver.get(url)
for i in range(3):
  driver.execute_script(f"window.scrollTo(0, {ht})")
  time.sleep(2)
  ht += 1080

time.sleep(5)
# Getting Page Source And Parsing HTMlL
page = driver.page_source 
soup = BeautifulSoup(page, 'html.parser')

# Gettings Images Links
imgLinks = []
both = re.compile("v1Nh3\s+kIKUG\s+_bz0w", re.I)
name = soup.find_all('div', class_=both)
for nm in name:
  imgLinks.append("https://www.instagram.com" + nm.a['href'])

# Printing No Of Links Collected
print("No Of Links Collected: " + str(len(imgLinks)))

# Converting To Dict and Storing in JSON File
data = {"links": imgLinks}
with open('links.json', 'w', encoding='utf-8') as file:
  json.dump(data, file, ensure_ascii=False, indent=2)

# Gettings Images Links
images = []
with open('imgSrc.json', 'w') as file:
  for url in imgLinks:
    try:
      driver.get(url)
      time.sleep(0.5)
      src = driver.page_source
      soup = BeautifulSoup(src, 'html.parser')
    
      div = soup.find('img', class_="FFVAD")
      images.append(div['src'])
    except Exception:
      pass
  data = {"links": images}
  json.dump(data, file, ensure_ascii=False, indent=2)

# Printing No Of Image Sources Collected
print("No Of Image Sources Collected: " + str(len(images)))

# Closing Window
driver.quit()

# Downloading Images
cnt = 0
for link in images:
  with open(f"./img/itsyourjapan/Japan{cnt}.jpg", 'wb') as file:
    r = requests.get(link)
    file.write(r.content)
    print(f"Downloaded Image No {cnt}")
    cnt += 1

