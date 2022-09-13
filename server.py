import random
import socket
from threading import Thread
import threading
import datetime
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import pickle
import json


LIVES_HAVE_EGG = []
ACCOUNTS = []
EDITABLE_ACCOUNTS = []

# read cookies.jon and append to ACCOUNTS + quantity
with open('cookies.json', 'r') as f:
    data = json.load(f)
    for index, acc in enumerate(data):
        ACCOUNTS.append({"id": index, "account": acc, "quantity": 1})


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
    get_site_info(driver)
    readLiveUrl(driver)


def get_site_info(driver):
    print('URL:', driver.current_url)
    print('Title:', driver.title)
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print('thời gian bắt đầu chạy: ' + current_time)


def scrollToEnd(driver):
    breakPoint = 0
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
        if breakPoint == 5:
            break
        breakPoint += 1


def readLiveUrl(driver):
    driver.refresh()
    scrollToEnd(driver)
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
        if i == 2:
            driver.switch_to.window(driver.window_handles[0])
            readLiveUrl(driver)


def checkIfLiveHasEgg(driver, live):
    sleep(7)
    script = '''
            const boxGift = document.querySelector('.nimo-box-gift__box');
            if(boxGift) return true;
    '''

    result = driver.execute_script(script)
    if result:
        if live not in LIVES_HAVE_EGG:
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
            condition = data.split("|")
            if condition[0] == "done":
                if client in busy_client:
                    busy_client.remove(client)
                    ACCOUNTS[int(condition[1])]["quantity"] += 1
    except:
        print("Disconnected connection from: ", address)
        all_clients.remove(client)
    finally:
        with clients_lock:
            clients.remove(client)
            client.close()


clients = set()
clients_lock = threading.Lock()
all_clients = []
busy_client = []
busy_cookies = []


def controlSocket():
    global all_clients
    while True:
        if LIVES_HAVE_EGG:
            for live in LIVES_HAVE_EGG:
                sleep(1)
                if live["quantity"] > 0:
                    while live["quantity"] > 0:
                        for c in all_clients:
                            if c not in busy_client and live["quantity"] > 0:
                                cookie = None
                                for account in ACCOUNTS:
                                    print(account["quantity"], '-----------------------', account["id"])
                                    if account["quantity"] > 0:
                                        cookie = account
                                        account["quantity"] -= 1
                                        break
                                if cookie:
                                    busy_client.append(c)
                                    msg = json.dumps({"id": cookie["id"], "link": live["link"], "account": cookie["account"]})
                                    data_encode = msg.encode('utf-8')
                                    c.send(data_encode)
                                    live["quantity"] -= 1
                                else:
                                    print("i dont know what to do here (:")
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


