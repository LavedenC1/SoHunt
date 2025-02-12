from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from tqdm import tqdm
import face_recognition
from modules.download_file import download_file
from modules.lsDir import lsDir
import time
from colorama import Fore, Style, init

def facebook(driver, name, intAmount):
    for x in lsDir("fb_downloads"):
        os.remove(os.path.join("fb_downloads", x))
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


