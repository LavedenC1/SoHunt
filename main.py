from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from colorama import Fore, Style, init
import time
from urllib.parse import quote
import os
from modules.download_file import download_file
from modules.lsDir import lsDir
from platforms.facebook import facebook
from platforms.google_images import google_images
from platforms.duckduckgo import *
from modules.options import *
import sys
if os.name != "nt":
    import readline

if not os.path.exists("fb_downloads"):
    os.makedirs("fb_downloads")

if not os.path.exists("gg_downloads"):
    os.makedirs("gg_downloads")

if not os.path.exists("ddg_downloads"):
    os.makedirs("ddg_downloads")

if not os.path.exists("known"):
    print("Put your target's pictures in the 'known' folder.")
    os.makedirs("known")

for x in lsDir("fb_downloads"):
    os.remove(os.path.join("fb_downloads", x))

for x in lsDir("gg_downloads"):
    os.remove(os.path.join("gg_downloads", x))

for x in lsDir("ddg_downloads"):
    os.remove(os.path.join("ddg_downloads", x))

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

target = targetOptions()
platform = platformOptions()
settings = settingsOptions()

while True:
    try:
        cmd = input(f"{Fore.RED}${Style.RESET_ALL} ").split()
        if len(cmd) == 0:
            continue
        elif cmd[0] == "help":
            print(f"{Fore.RED}Welcome to SoHunt!{Style.RESET_ALL}")
            print("Available commands:")
            print(f"{Style.BRIGHT}help{Style.RESET_ALL} - Display this help message")
            print(f"{Style.BRIGHT}get <group>.<key>{Style.RESET_ALL} - Get a configuration value (run `options` for groups and keys)")
            print(f"{Style.BRIGHT}set <group>.<key> <value>{Style.RESET_ALL} - Set a configuration value (run `options` for groups and keys)")
            print(f"{Style.BRIGHT}options{Style.RESET_ALL} - Display available configuration options")
            print(f"{Style.BRIGHT}clean{Style.RESET_ALL} - Remove all downloaded files")
            print(f"{Style.BRIGHT}start{Style.RESET_ALL} - Start searching for profiles")
        elif cmd[0] == "options":
            print(f"{Fore.RED}Available configuration options:{Style.RESET_ALL}")
            print(f"Group: {Style.BRIGHT}target{Style.RESET_ALL}")
            print(f"\t{Style.BRIGHT}name{Style.RESET_ALL} - Name of target")
            print(f"\t{Style.BRIGHT}number{Style.RESET_ALL} - Phone number of target")
            print(f"\t{Style.BRIGHT}continent{Style.RESET_ALL} - Continent of target (2 Letters, e.g., 'US', 'EU', 'AS', etc.)")
            print(f"Group: {Style.BRIGHT}platform{Style.RESET_ALL}")
            print(f"\t{Style.BRIGHT}facebook{Style.RESET_ALL} - Should we use facebook? (True/False)")
            print(f"\t{Style.BRIGHT}google_images{Style.RESET_ALL} - Should we use Google Images? (True/False)")
            print(f"\t{Style.BRIGHT}duckduckgo{Style.RESET_ALL} - Should we use DuckDuckGo? (True/False)")
            print(f"Group: {Style.BRIGHT}settings{Style.RESET_ALL}")
            print(f"\t{Style.BRIGHT}scroll_time{Style.RESET_ALL} - Amount of seconds to scroll (0-20 recommended)")
            print(f"\t{Style.BRIGHT}headless{Style.RESET_ALL} - Run browser in headless mode (True/False)")
        elif cmd[0] == "get":
            try:
                if len(cmd) < 2:
                    print(f"{Fore.RED}Invalid usage. Use `get <group>.<key>`{Style.RESET_ALL}")
                else:
                    group, key = cmd[1].split(".")
                    if group == "target":
                        if key == "name":
                            print(f"{Fore.RED}Name: {Style.RESET_ALL}{target.name}")
                        elif key == "number":
                            print(f"{Fore.RED}Phone number: {Style.RESET_ALL}{target.number}")
                        elif key == "continent":
                            print(f"{Fore.RED}Continent: {Style.RESET_ALL}{target.continent}")
                        else:
                            print(f"{Fore.RED}Invalid key. Use `options` for available keys in the 'target' group.{Style.RESET_ALL}")
                    elif group == "platform":
                        if key == "facebook":
                            print(f"{Fore.RED} Use Facebook: {Style.RESET_ALL}{platform.facebook}")
                        elif key == "google_images":
                            print(f"{Fore.RED}Use Google Images: {Style.RESET_ALL}{platform.google_images}")
                        elif key == "duckduckgo":
                            print(f"{Fore.RED}Use DuckDuckGo: {Style.RESET_ALL}{platform.duckduckgo}")
                        else:
                            print(f"{Fore.RED}Invalid key. Use `options` for available keys in the 'target' group.{Style.RESET_ALL}")
                    elif group == "settings":
                        if key == "scroll_time":
                            print(f"{Fore.RED}Scroll time: {Style.RESET_ALL}{settings.scroll_time}")
                        elif key == "headless":
                            print(f"{Fore.RED}Headless: {Style.RESET_ALL}{settings.headless}")
                        else:
                            print(f"{Fore.RED}Invalid key. Use `options` for available keys in the 'target' group.{Style.RESET_ALL}")
            except:
                print(f"{Fore.RED}Invalid group or key. Use `options` for available groups and keys.{Style.RESET_ALL}")
        elif cmd[0] == "set":
            try:
                if len(cmd) < 3:
                    print(f"{Fore.RED}Invalid usage. Use `set <group>.<key> <value>`{Style.RESET_ALL}")
                else:
                    group, key = cmd[1].split(".")
                    value = " ".join(cmd[2:])
                    if group == "target":
                        if key == "name":
                            target.name = value
                        elif key == "number":
                            target.number = value
                        elif key == "continent":
                            target.continent = value
                        else:
                            print(f"{Fore.RED}Invalid key. Use `options` for available keys in the 'target' group.{Style.RESET_ALL}")
                    elif group == "platform":
                        if key == "facebook":
                            platform.facebook = True if value.lower() == "true" else False
                        elif key == "google_images":
                            platform.google_images = True if value.lower() == "true" else False
                        elif key == "duckduckgo":
                            platform.duckduckgo = True if value.lower() == "true" else False
                        else:
                            print(f"{Fore.RED}Invalid key. Use `options` for available keys in the 'target' group.{Style.RESET_ALL}")
                    elif group == "settings":
                        if key == "scroll_time":
                            settings.scroll_time = int(value)
                        elif key == "headless":
                            settings.headless = True if value.lower() == "true" else False
                        else:
                            print(f"{Fore.RED}Invalid key. Use `options` for available keys in the 'target' group.{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.RED}Invalid group. Use `options` for available groups.{Style.RESET_ALL}")
            except:
                print(f"{Fore.RED}Invalid value. Use `options` for available keys and values.{Style.RESET_ALL}")
        elif cmd[0] == "start":
            print(f"{Style.RESET_ALL}-"*40)
            print(f"[*] Starting WebDriver")
            options = Options()
            if settings.headless:
                options.add_argument('-headless')
            service = Service(GeckoDriverManager().install())
            driver = webdriver.Firefox(options=options, service=service)
            if platform.facebook:
                print(f"------ {Fore.BLUE}Facebook{Style.RESET_ALL} ------")
                facebook(driver, target.name, settings.scroll_time)
            if platform.google_images:
                print(f"------ {Fore.BLUE}G{Fore.RED}o{Fore.YELLOW}o{Fore.BLUE}g{Fore.GREEN}l{Fore.RED}e{Style.RESET_ALL} ------")
                google_images(driver, target.name, settings.scroll_time)
            if platform.duckduckgo:
                print(f"------ {Fore.YELLOW}DuckDuckGo{Style.RESET_ALL} ------")
                duckduckgo(driver, target.name, settings.scroll_time)
            driver.quit()
        elif cmd[0] == "clear":
            os.system('cls' if os.name == 'nt' else 'clear')
        elif cmd[0] == "exit" or cmd[0] == "quit":
            print(f"{Fore.RED}Exiting SoHunt...{Style.RESET_ALL}")
            sys.exit(0)
        elif cmd[0] == "clean":
            for x in lsDir("fb_downloads"):
                os.remove(os.path.join("fb_downloads", x))

            for x in lsDir("gg_downloads"):
                os.remove(os.path.join("gg_downloads", x))

            for x in lsDir("ddg_downloads"):
                os.remove(os.path.join("ddg_downloads", x))
        else:
            print(f"{Fore.RED}Invalid command. Use `help` for available commands.{Style.RESET_ALL}")
    except KeyboardInterrupt:
        print("")
        continue
    except EOFError:
        sys.exit(0)