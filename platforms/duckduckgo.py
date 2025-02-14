from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from tqdm import tqdm
import face_recognition
from modules.download_file import download_file
from modules.lsDir import lsDir
import time
from colorama import Fore, Style, init
import os
import base64
from urllib.parse import *
import urllib.parse

def duckduckgo(driver, name, intAmount):
    for x in lsDir("ddg_downloads"):
        os.remove(os.path.join("ddg_downloads", x))

    print(f"[*] Opening DuckDuckGo...")
    driver.get(f"https://duckduckgo.com/?t=h_&iax=images&ia=images&q={name}")
    time.sleep(3)

    print(f"[*] Scrolling down...")
    for _ in tqdm(range(intAmount)):
        ActionChains(driver).scroll_by_amount(0, 10000).perform()
        time.sleep(1)

    print(f"[*] Gathering profile photos...")
    image_elements = driver.find_elements(By.XPATH, '//*[@id="zci-images"]/div/div[2]/div[2]/div/div[1]/span/img')
    images = []
    for profile in tqdm(image_elements,desc="Gathering Photos"):
        text = profile.get_attribute("src")
        phrase = "/?u="
        index = text.find(phrase)
        url = urllib.parse.unquote(text[index + len(phrase):])
        images.append(url)

    print(f"[*] Gathering links...")
    links = driver.find_elements(By.XPATH, '//*[@id="zci-images"]/div[1]/div[2]/div[2]/div/a') 
    image_links = []
    for link in tqdm(links, desc="Gathering Links"):
        image_links.append(link.get_attribute("href"))
    
    print(f"[*] Downloading profile photos...")
    for i in tqdm(range(len(images)), desc="Downloading Photos"):
        download_file(images[i], f"ddg_downloads/{i}.jpeg")


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
        files = sorted(lsDir("ddg_downloads"), key=lambda x: int(x.split(".")[0]))
        for propic in tqdm(files, desc="Recognizing"):
            try:
                recUnk = face_recognition.load_image_file("ddg_downloads/" + propic)
                recUnkEncoding = face_recognition.face_encodings(recUnk)[0]
                results = face_recognition.compare_faces([recPicEncocing], recUnkEncoding)
                if results[0] == True:
                    picResults.append(propic)
                else:
                    picResults.append("X")
                    continue
            except:
                picResults.append("X")
        print("-" * 40)
        print(f"{Fore.RED}{Style.BRIGHT}Potential Results:{Style.RESET_ALL}")
        c = 0
        for i in picResults:
            if i != "X":
                print("-" * 40)
                print(f"{Fore.GREEN}" + image_links[c] + f"{Style.RESET_ALL}")
            c += 1
        print("-" * 40)