import random
import socket
from threading import Thread
import threading
import datetime
import time
from datetime import datetime
# from selenium import webdriver
# from selenium.webdriver.common.by import By
from time import sleep
import pickle
import json
import glob

#
# LIVES_HAVE_EGG = []
ACCOUNTS = []
# EDITABLE_ACCOUNTS = []
# room_participants = input("Số lượng account tham gia room: ")
# country = input("Nhập vùng cần chạy('vn', 'gl', 'ind', 'tr', 'mr'): ")
# chooseLink = input("all - nimoshow - gta5 - lol - pugb - pugbm - csgo - luachua: ")
# defaultLink = ''
# if chooseLink == "all":
#     defaultLink = "https://www.nimo.tv/lives"
# if chooseLink == "nimoshow":
#     defaultLink = "https://www.nimo.tv/game/185"
# if chooseLink == "gta5":
#     defaultLink = "https://www.nimo.tv/game/gta5"
# if chooseLink == "lol":
#     defaultLink = "https://www.nimo.tv/game/lol"
# if chooseLink == "pubg":
#     defaultLink = "https://www.nimo.tv/game/pubg"
# if chooseLink == "pubgm":
#     defaultLink = "https://www.nimo.tv/game/PUBGM"
# if chooseLink == "csgo":
#     defaultLink = "https://www.nimo.tv/game/csgo"
# if chooseLink == "freefire":
#     defaultLink = "https://www.nimo.tv/game/freefire"
# if chooseLink == "":
#     defaultLink = "https://www.nimo.tv/lives"
#
all_cookies = glob.glob("cookies/*")
for index, file in enumerate(all_cookies):
    with open(file, 'r') as f:
        data = json.load(f)
        ACCOUNTS.append({"id": index, "account": data, "quantity": 1})

# def generateRandom():
#     return random.randint(1, 10)
#
#
# def initBrowser():
#     # create a Firefox browser instance object Options
#     profile = webdriver.FirefoxProfile()
#     # disable CSS load
#     profile.set_preference('permissions.default.stylesheet', 2)
#     # disable images loading
#     profile.set_preference('permissions.default.image', 2)
#     # disable flash plug
#     profile.set_preference('allow_scripts_to_close_windows', True)
#     profile.set_preference('dom.allow_scripts_to_close_windows', True)
#     profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', False)
#     profile.set_preference("network.http.pipelining", True)
#     profile.set_preference("network.http.proxy.pipelining", True)
#     profile.set_preference("network.http.pipelining.maxrequests", 8)
#     profile.set_preference("content.notify.interval", 500000)
#     profile.set_preference("content.notify.ontimer", True)
#     profile.set_preference("content.switch.threshold", 250000)
#     profile.set_preference("browser.cache.memory.capacity", 65536)  # Increase the cache capacity.
#     profile.set_preference("browser.startup.homepage", "about:blank")
#     profile.set_preference("reader.parse-on-load.enabled", False)  # Disable reader, we won't need that.
#     profile.set_preference("browser.pocket.enabled", False)  # Duck pocket too!
#     profile.set_preference("loop.enabled", False)
#     profile.set_preference("browser.chrome.toolbar_style", 1)  # Text on Toolbar instead of icons
#     profile.set_preference("browser.display.show_image_placeholders",
#                            False)  # Don't show thumbnails on not loaded images.
#     profile.set_preference("browser.display.use_document_colors", False)  # Don't show document colors.
#     profile.set_preference("browser.display.use_document_fonts", 0)  # Don't load document fonts.
#     profile.set_preference("browser.display.use_system_colors", True)  # Use system colors.
#     profile.set_preference("browser.formfill.enable", False)  # Autofill on forms disabled.
#     profile.set_preference("browser.helperApps.deleteTempFileOnExit", True)  # Delete temprorary files.
#     profile.set_preference("browser.shell.checkDefaultBrowser", False)
#     profile.set_preference("browser.startup.homepage", "about:blank")
#     profile.set_preference("browser.startup.page", 0)  # blank
#     profile.set_preference("browser.tabs.forceHide", True)  # Disable tabs, We won't need that.
#     profile.set_preference("browser.urlbar.autoFill", False)  # Disable autofill on URL bar.
#     profile.set_preference("browser.urlbar.autocomplete.enabled", False)  # Disable autocomplete on URL bar.
#     profile.set_preference("browser.urlbar.showPopup", False)  # Disable list of URLs when typing on URL bar.
#     profile.set_preference("browser.urlbar.showSearch", False)  # Disable search bar.
#     profile.set_preference("extensions.checkCompatibility", False)  # Addon update disabled
#     profile.set_preference("extensions.checkUpdateSecurity", False)
#     profile.set_preference("extensions.update.autoUpdateEnabled", False)
#     profile.set_preference("extensions.update.enabled", False)
#     profile.set_preference("general.startup.browser", False)
#     profile.set_preference("plugin.default_plugin_disabled", False)
#     profile.set_preference("permissions.default.image", 2)  # Image load disabled again
#     # Start the Firefox browser with custom settings
#     driver = webdriver.Firefox(firefox_profile=profile)
#     driver.get("https://www.nimo.tv/lives")
#     Thread(target=reset, args=[driver]).start()
#     print('start browser...')
#     get_site_info(driver)
#     chooseCountry(driver)
#     readLiveUrl(driver)
#
#
# def get_site_info(driver):
#     print('URL:', driver.current_url)
#     print('Title:', driver.title)
#     now = datetime.now()
#     current_time = now.strftime("%H:%M:%S")
#     print('thời gian bắt đầu chạy: ' + current_time)
#
#
# def chooseCountry(driver):
#     driver.maximize_window()
#     sleep(3)
#     chooseCountryButton = driver.find_elements(By.CLASS_NAME, "nimo-header-country-flag")
#     chooseCountryButton[0].click()
#     script = "let listCountry = document.querySelectorAll('.CountryList__item');" \
#              "let c = '" + country + "';"
#     script += "listCountry.forEach(country => {" \
#               "attr = country.getAttribute('title');" \
#               "switch (c) {" \
#               "case 'vn':" \
#               "if ((attr === 'Việt nam') || (attr === 'Vietnam')) {" \
#               " country.click();" \
#               " };" \
#               "break;" \
#               "case 'gl':" \
#               "if ((attr === 'Toàn cầu') || (attr === 'Global')) {" \
#               "country.click();" \
#               " };" \
#               "break;" \
#               "case 'tr':" \
#               "if ((attr === 'Thổ Nhĩ Kỳ') || (attr === 'Turkey')) {" \
#               "country.click();" \
#               " };" \
#               "break;" \
#               "case 'mr':" \
#               "if ((attr === 'Ma-rốc') || (attr === 'Morocco')) {" \
#               "country.click();" \
#               " };" \
#               "case 'ind':" \
#               "if ((attr === 'Indonesia') || (attr === 'Indonesia')) {" \
#               "country.click();" \
#               " };" \
#               "break;" \
#               " };" \
#               "" \
#               "});"
#     driver.execute_script(script)
#     sleep(4)
#
#
# def scrollToEnd(driver):
#     breakPoint = 0
#     while True:
#         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#         breakPoint += 1
#         sleep(2)
#         if breakPoint == 4 + 1:    # replace condition by inpupt ----
#             break
#
#
# def readLiveUrl(driver):
#     driver.get(defaultLink)
#     scrollToEnd(driver)
#     sleep(5)
#     lives = []
#     liveUrls = driver.find_elements(By.CSS_SELECTOR, ".nimo-rc_meta__info .controlZindexMargin")
#     for url in liveUrls:
#         lives.append(url.get_attribute('href'))
#     openNewTab(driver, lives)
#
#
# def openNewTab(driver, lives):
#     i = 0
#     while True:
#         try:
#             if i == len(lives) - 1:
#                 driver.switch_to.window(driver.window_handles[0])
#                 readLiveUrl(driver)
#                 break
#             if len(driver.window_handles) < int(2):
#                 driver.switch_to.window(driver.window_handles[0])
#                 driver.switch_to.new_window('tab')
#                 driver.get(lives[i])
#                 checkIfLiveHasEgg(driver, lives[i])
#                 i += 1
#         except:
#             continue
#
#
# def checkIfLiveHasEgg(driver, live):
#     sleep(7)
#     script = '''
#             const boxGift = document.querySelector('.nimo-box-gift__box');
#             if(boxGift) return true;
#     '''
#
#     result = driver.execute_script(script)
#     if result:
#         r = any(l["link"] == live for l in LIVES_HAVE_EGG)
#         if not r:
#             LIVES_HAVE_EGG.append({"link": live, "quantity": int(room_participants) or 5})
#     driver.close()
#
#
# def reset(driver):
#     reset = input('---------------- Reset Server ??? ----------------: ')
#     global room_participants, country, chooseLink, url
#     if reset:
#         try:
#             print("Server is restarting!!!!!!!!!!!!!!!!!!")
#             driver.quit()
#             room_participants = input("Số lượng account tham gia room: ")
#             country = input("Nhập vùng cần chạy('vn', 'gl', 'ind', 'tr', 'mr'): ")
#             chooseLink = input("all - nimoshow - gta5 - lol - pugb - pugbm - csgo - luachua: ")
#             if chooseLink == "all":
#                 url = "https://www.nimo.tv/lives"
#             if chooseLink == "nimoshow":
#                 url = "https://www.nimo.tv/game/185"
#             if chooseLink == "gta5":
#                 url = "https://www.nimo.tv/game/gta5"
#             if chooseLink == "lol":
#                 url = "https://www.nimo.tv/game/lol"
#             if chooseLink == "pubg":
#                 url = "https://www.nimo.tv/game/pubg"
#             if chooseLink == "pubgm":
#                 url = "https://www.nimo.tv/game/PUBGM"
#             if chooseLink == "csgo":
#                 url = "https://www.nimo.tv/game/csgo"
#             if chooseLink == "freefire":
#                 url = "https://www.nimo.tv/game/freefire"
#             if chooseLink == "":
#                 url = "https://www.nimo.tv/lives"
#             LIVES_HAVE_EGG.clear()
#             ACCOUNTS.clear()
#             busy_client.clear()
#             for index, file in enumerate(all_cookies):
#                 with open(file, 'r') as f:
#                     data = json.load(f)
#                     ACCOUNTS.append({"id": index, "account": data, "quantity": 1})
#             initBrowser()
#
#         except:
#             pass
#
#
#
#
#
#
# Thread(target=initBrowser).start()


def listener(client, address):
    print("Accepted connection from: ", address)
    all_clients.append(client)
    with clients_lock:
        clients.add(client)
    try:
        while True:
            data = client.recv(10024)
            data = data.decode()
            condition = data.split("|")
            print(condition)
            if condition[0] == "done":
                if client in busy_client:
                    busy_client.remove(client)
                    ACCOUNTS[int(condition[1])]["quantity"] += 1
    except:
        print("Disconnected connection from: ", address)
        if client in busy_client:
            busy_client.remove(client)
        all_clients.remove(client)
    finally:
        with clients_lock:
            clients.remove(client)
            client.close()


clients = set()
clients_lock = threading.Lock()
all_clients = []
busy_client = []


def controlSocket():
    global all_clients
    while True:
        link = input("Link: ")
        for c in all_clients:
            data = json.dumps({"link": link})
            data_encode = data.encode('utf-8')
            c.send(data_encode)


Thread(target=controlSocket).start()


host = '0.0.0.0' #my server ip   103.178.234.58
port = 9981  # Production port 9981

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((host, port))
s.listen(100)
th = []
print("Server is listening for connections...")
while True:
    client, address = s.accept()
    timestamp = datetime.now().strftime("%b %d %Y,%a, %I:%M:%S %p")
    a = ("Welcome to server " + timestamp).encode()
    th.append(Thread(target=listener, args=(client, address)).start())
s.close()