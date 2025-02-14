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
from urllib.parse import urlparse


def google_images(driver, name, intAmount):
    for x in lsDir("gg_downloads"):
        os.remove(os.path.join("gg_downloads", x))

    print(f"[*] Opening Google...")
    driver.get(f"https://www.google.com/search?sclient=img&udm=2&q={name}")
    time.sleep(3)

    print(f"[*] Scrolling down...")
    for _ in tqdm(range(intAmount)):
        ActionChains(driver).scroll_by_amount(0, 10000).perform()
        time.sleep(1)

    print(f"[*] Gathering profile photos...")
    image_elements = driver.find_elements(By.CSS_SELECTOR, "div.eA0Zlc img")
    images = []
    for profile in tqdm(image_elements,desc="Gathering Photos"):
        images.append(profile.get_attribute("src"))
    images = images[::2]

    print(f"[*] Gathering links...")
    links = driver.find_elements(By.XPATH, "/html/body/div[3]/div/div[14]/div/div[2]/div[2]/div/div/div/div/div[1]/div/div/div/div[2]/h3/a") 
    image_links = []
    for link in tqdm(links, desc="Gathering Links"):
        image_links.append(link.get_attribute("href"))
    print(f"[*] Downloading profile photos...")
    for i, image_url in tqdm(enumerate(images), desc="Downloading Photos", total=len(images)):
        try:
            if image_url.startswith('data:'):
                # Handle data URL
                header, encoded = image_url.split(",", 1)
                content_type = header.split(":")[1].split(";")[0]
                file_extension = content_type.split("/")[-1]
                
                # Decode base64 content
                image_data = base64.b64decode(encoded)
                
                # Save the file
                with open(f"gg_downloads/{i}.{file_extension}", "wb") as f:
                    f.write(image_data)
            else:
                # Handle regular URL
                parsed_url = urlparse(image_url)
                file_extension = os.path.splitext(parsed_url.path)[1]
                if not file_extension:
                    file_extension = '.jpg'  # Default to .jpg if no extension found
                
                download_file(image_url, f"gg_downloads/{i}{file_extension}")
        except Exception as e:
            print(f"Error downloading image {i}: {str(e)}")


    # known_pics = lsDir("known")

    # print("[*] Starting face recognition")
    # for known_pic in known_pics:
    #     picResults = []
    #     try:
    #         recPic = face_recognition.load_image_file("known/" + known_pic)
    #         recPicEncocing = face_recognition.face_encodings(recPic)[0]
    #     except:
    #         print("No Face Detected")
    #         break
    #     files = sorted(lsDir("fb_downloads"), key=lambda x: int(x.split(".")[0]))
    #     for propic in tqdm(files, desc="Recognizing"):
    #         try:
    #             recUnk = face_recognition.load_image_file("fb_downloads/" + propic)
    #             recUnkEncoding = face_recognition.face_encodings(recUnk)[0]
    #             results = face_recognition.compare_faces([recPicEncocing], recUnkEncoding)
    #             if results[0] == True:
    #                 picResults.append(propic)
    #             else:
    #                 picResults.append("X")
    #                 continue
    #         except:
    #             print("No Face Detected")
    #             picResults.append("X")
    #     print("-" * 40)
    #     print(f"{Fore.RED}{Style.BRIGHT}Potential Results:{Style.RESET_ALL}")
    #     c = 0
    #     for i in picResults:
    #         if i != "X":
    #             print("-" * 40)
    #             print(f"{Fore.GREEN}" + profile_links[c] + f"{Style.RESET_ALL}")
    #         c += 1
    #     print("-" * 40)