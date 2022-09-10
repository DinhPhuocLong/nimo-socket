import random
import socket
from threading import Thread
import threading
import datetime
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import pickle
import json


LIVES_HAVE_EGG = []
ACCOUNTS = []

# read cookies.jon and append to ACCOUNTS + quantity
with open('cookies.json', 'r') as f:
    data = json.load(f)
    for acc in data:
        ACCOUNTS.append({"account": acc, "quantity": 5})


def generateRandom():
    return random.randint(1, 10)


def initBrowser():
    # create a Firefox browser instance object Options
    profile = webdriver.FirefoxProfile()
    # disable CSS load
    profile.set_preference('permissions.default.stylesheet', 2)
    # disable images loading
    profile.set_preference('permissions.default.image', 2)
    # disable flash plug
    profile.set_preference('allow_scripts_to_close_windows', True)
    profile.set_preference('dom.allow_scripts_to_close_windows', True)
    profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', False)
    profile.set_preference("network.http.pipelining", True)
    profile.set_preference("network.http.proxy.pipelining", True)
    profile.set_preference("network.http.pipelining.maxrequests", 8)
    profile.set_preference("content.notify.interval", 500000)
    profile.set_preference("content.notify.ontimer", True)
    profile.set_preference("content.switch.threshold", 250000)
    profile.set_preference("browser.cache.memory.capacity", 65536)  # Increase the cache capacity.
    profile.set_preference("browser.startup.homepage", "about:blank")
    profile.set_preference("reader.parse-on-load.enabled", False)  # Disable reader, we won't need that.
    profile.set_preference("browser.pocket.enabled", False)  # Duck pocket too!
    profile.set_preference("loop.enabled", False)
    profile.set_preference("browser.chrome.toolbar_style", 1)  # Text on Toolbar instead of icons
    profile.set_preference("browser.display.show_image_placeholders",
                           False)  # Don't show thumbnails on not loaded images.
    profile.set_preference("browser.display.use_document_colors", False)  # Don't show document colors.
    profile.set_preference("browser.display.use_document_fonts", 0)  # Don't load document fonts.
    profile.set_preference("browser.display.use_system_colors", True)  # Use system colors.
    profile.set_preference("browser.formfill.enable", False)  # Autofill on forms disabled.
    profile.set_preference("browser.helperApps.deleteTempFileOnExit", True)  # Delete temprorary files.
    profile.set_preference("browser.shell.checkDefaultBrowser", False)
    profile.set_preference("browser.startup.homepage", "about:blank")
    profile.set_preference("browser.startup.page", 0)  # blank
    profile.set_preference("browser.tabs.forceHide", True)  # Disable tabs, We won't need that.
    profile.set_preference("browser.urlbar.autoFill", False)  # Disable autofill on URL bar.
    profile.set_preference("browser.urlbar.autocomplete.enabled", False)  # Disable autocomplete on URL bar.
    profile.set_preference("browser.urlbar.showPopup", False)  # Disable list of URLs when typing on URL bar.
    profile.set_preference("browser.urlbar.showSearch", False)  # Disable search bar.
    profile.set_preference("extensions.checkCompatibility", False)  # Addon update disabled
    profile.set_preference("extensions.checkUpdateSecurity", False)
    profile.set_preference("extensions.update.autoUpdateEnabled", False)
    profile.set_preference("extensions.update.enabled", False)
    profile.set_preference("general.startup.browser", False)
    profile.set_preference("plugin.default_plugin_disabled", False)
    profile.set_preference("permissions.default.image", 2)  # Image load disabled again
    # Start the Firefox browser with custom settings
    driver = webdriver.Firefox(firefox_profile=profile)
    driver.get("https://www.nimo.tv/lives")
    print('start browser...')
    print(ACCOUNTS)
    get_site_info(driver)
    readLiveUrl(driver)


def get_site_info(driver):
    print('URL:', driver.current_url)
    print('Title:', driver.title)
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print('thời gian bắt đầu chạy: ' + current_time)


def readLiveUrl(driver):
    sleep(5)
    lives = []
    liveUrls = driver.find_elements(By.CSS_SELECTOR, ".nimo-rc_meta__info .controlZindexMargin")
    for url in liveUrls:
        lives.append(url.get_attribute('href'))
    openNewTab(driver, lives)


def openNewTab(driver, lives):
    i = 0
    while True:
        driver.switch_to.window(driver.window_handles[0])
        if len(driver.window_handles) < int(2):
            driver.switch_to.new_window('tab')
            driver.get(lives[i])
            checkIfLiveHasEgg(driver, lives[i])
            i += 1
        if len(lives) == i:
            i = 0


def checkIfLiveHasEgg(driver, live):
    WebDriverWait(driver, 4).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "chat-input-wrapper")))
    script = '''
            const boxGift = document.querySelector('.nimo-box-gift__box');
            if(boxGift) return true;
    '''
    result = driver.execute_script(script)
    if result:
        LIVES_HAVE_EGG.append({"link": live, "quantity": 5})

    driver.close()


Thread(target=initBrowser).start()


def listener(client, address):
    print("Accepted connection from: ", address)
    all_clients.append(client)
    with clients_lock:
        clients.add(client)
    try:
        while True:
            data = client.recv(10024)
            data = data.decode()
            print(busy_client)
            if data == 'done':
                busy_client.remove(client)
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
        if LIVES_HAVE_EGG:
            for live in LIVES_HAVE_EGG:
                print(LIVES_HAVE_EGG)
                print(busy_client)
                sleep(4)
                if live["quantity"]:
                    for c in all_clients:
                        try:
                            if c not in busy_client:
                                data = live["link"]
                                c.send(data.encode('utf-8'))
                                busy_client.append(c)
                                live["quantity"] -= 1
                        except:
                            continue
                else:
                    LIVES_HAVE_EGG.remove(live)


Thread(target=controlSocket).start()


host = '127.0.0.1'  # it gets ip of lan
port = 9991

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


