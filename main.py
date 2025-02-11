from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from tqdm import tqdm
from colorama import Fore, Style, init
import time
from urllib.parse import quote
import os
import face_recognition
from modules.download_file import download_file
from modules.lsDir import lsDir
from platforms.facebook import facebook

if not os.path.exists("fb_downloads"):
    os.makedirs("fb_downloads")

if not os.path.exists("known"):
    os.makedirs("known")

for x in lsDir("fb_downloads"):
    os.remove(os.path.join("fb_downloads", x))



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

facebook(name, intAmount)
