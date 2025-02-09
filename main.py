from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from tqdm import tqdm
from colorama import Fore, Style, init
import time
from urllib.parse import quote
import requests
import os
import face_recognition

import os

if not os.path.exists("fb_downloads"):
    os.makedirs("fb_downloads")

if not os.path.exists("known"):
    os.makedirs("known")

import os

def lsDir(folder_path):
  try:
    files = os.listdir(folder_path)
    return [f for f in files if os.path.isfile(os.path.join(folder_path, f))]
  except FileNotFoundError:
    return []
  except Exception as e:
      print(f"An error occurred: {e}")
      return []
for x in lsDir("fb_downloads"):
    os.remove(os.path.join("fb_downloads", x))

def download_file(url, filename):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(filename, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
    except requests.exceptions.RequestException as e:
        print(f"Error downloading file: {e}")
    except IOError as e:
        print(f"Error writing to file: {e}")


init(autoreset=False)

logo = f"""
███████╗ ██████╗ ██╗  ██╗██╗   ██╗███╗   ██╗████████╗
██╔════╝██╔═══██╗██║  ██║██║   ██║████╗  ██║╚══██╔══╝
███████╗██║   ██║███████║██║   ██║██╔██╗ ██║   ██║   
╚════██║██║   ██║██╔══██║██║   ██║██║╚██╗██║   ██║   
███████║╚██████╔╝██║  ██║╚██████╔╝██║ ╚████║   ██║   
╚══════╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   
-------------------- By Laveden --------------------
"""
for x in range(len(logo)):
    print(f"{Fore.RED}{logo[x]}{Style.RESET_ALL}",end="")
    time.sleep(0.001)

name = quote(input(f"Enter the person's name: {Fore.RED}"))
intAmount = int(input(f"{Style.RESET_ALL}Profile Intensity (0-20 recommended): {Fore.RED}"))
print(f"{Style.RESET_ALL}-"*40)

print(f"[*] Starting WebDriver")
options = Options()
options.add_argument('-headless')
service = Service(GeckoDriverManager().install())
driver = webdriver.Firefox(options=options, service=service)


print(f"[*] Opening Facebook...")
driver.get(f"https://facebook.com/public/{name}")
time.sleep(3)

print(f"[*] Scrolling down...")
for _ in tqdm(range(intAmount)):
    ActionChains(driver).scroll_by_amount(0, 10000).perform()
    time.sleep(1)

print(f"[*] Gathering profile photos...")
profiles = driver.find_elements(By.CLASS_NAME, "_6phc")
profile_photos = []
for profile in tqdm(profiles,desc="Gathering Photos"):
    profile_photos.append(profile.get_attribute("src"))

print(f"[*] Gathering links...")
links = driver.find_elements(By.CLASS_NAME, "_32mo")
profile_links = []
for link in tqdm(links, desc="Gathering Links"):
    profile_links.append(link.get_attribute("href"))

print(f"[*] Downloading profile photos...")
for i in tqdm(range(len(profile_photos)), desc="Downloading Photos"):
    download_file(profile_photos[i], f"fb_downloads/{i}.jpg")


known_pics = lsDir("known")

print("[*] Starting face recognition")
for known_pic in known_pics:
    picResults = []
    try:
        recPic = face_recognition.load_image_file("known/" + known_pic)
        recPicEncocing = face_recognition.face_encodings(recPic)[0]
    except:
        print("No Face Detected")
        break
    files = sorted(lsDir("fb_downloads"), key=lambda x: int(x.split(".")[0]))
    for propic in tqdm(files, desc="Recognizing"):
        try:
            recUnk = face_recognition.load_image_file("fb_downloads/" + propic)
            recUnkEncoding = face_recognition.face_encodings(recUnk)[0]
            results = face_recognition.compare_faces([recPicEncocing], recUnkEncoding)
            if results[0] == True:
                picResults.append(propic)
            else:
                picResults.append("X")
                continue
        except:
            print("No Face Detected")
            picResults.append("X")
    print("-" * 40)
    print(f"{Fore.RED}{Style.BRIGHT}Potential Results:{Style.RESET_ALL}")
    c = 0
    for i in picResults:
        if i != "X":
            print("-" * 40)
            print(f"{Fore.GREEN}" + profile_links[c] + f"{Style.RESET_ALL}")
        c += 1
    print("-" * 40)


driver.quit()

