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

# read cookies.jon and append to ACCOUNTS + quantity
with open('cookies.json', 'r') as f:
    data = json.load(f)
    for acc in data:
        ACCOUNTS.append({"account": acc, "quantity": 5})


def generateRandom():
    return random.randint(1, 10)


def initBrowser():
    driver = webdriver.Firefox()
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
            driver.close()
            i += 1
        if len(lives) == i:
            i = 0


def checkIfLiveHasEgg(driver, live):
    sleep(2)
    script = '''
            const boxGift = document.querySelector('.nimo-box-gift__box');
            if(boxGift) return true;
    '''
    result = driver.execute_script(script)
    if result:
        LIVES_HAVE_EGG.append({"link": live, "quantity": 5})
    return result


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


