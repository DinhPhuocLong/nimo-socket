import socket
import datetime
from datetime import datetime
from selenium import webdriver
from time import sleep
import threading
import json

# --- init driver ---

LIVE = None
COOKIE = None
FLAG = False
driver = webdriver.Firefox()
def initBrowser():
    driver.get("https://www.nimo.tv/lives")
    print('start browser...')
    get_site_info()


def get_site_info():
    print('URL:', driver.current_url)
    print('Title:', driver.title)
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print('thời gian bắt đầu chạy: ' + current_time)


def loginUsingCookies():
    driver.delete_all_cookies()
    for cookie in COOKIE["cookies"]:
        cookie.pop('sameSite')
        driver.add_cookie(cookie)
    driver.refresh()


def openLiveInNewTab(url):
    global FLAG
    FLAG = True
    driver.switch_to.new_window('tab')
    driver.get(url)
    sleep(4)
    collectEggs()


def collectEggs():
    driver.execute_script("""
        function collectEgg() {
            const button = document.querySelector('.pl-icon_danmu_open');
            if(button) button.click();
            collectInterval = setInterval(function(){
                const boxGift = document.querySelector('.nimo-box-gift__box');      
                const collectBtn = document.querySelector('.nimo-box-gift__box__btn');
                let isBoxGift = document.querySelector('.nimo-room__chatroom__box-gift-item');
                if(!boxGift) window.close();
                if(collectBtn) collectBtn.click();
                if(window.getComputedStyle(isBoxGift).display == 'none') window.close();
            }, 1);
        }
        collectEgg();
    """)
# wait for server


initBrowser()


s = socket.socket()
host = '127.0.0.1' #my server ip   103.178.234.58
port = 9661
print(f'connected to {host}:{port}')


s.connect((host, port))

while True:
    data = s.recv(20024)
    data = data.decode()
    data = json.loads(data)
    print(data)
    LIVE = data['link']
    print(LIVE)
    COOKIE = data['account']
    loginUsingCookies()
    openLiveInNewTab(LIVE)
    while True:
        if FLAG and len(driver.window_handles) == 1:
            driver.switch_to.window(driver.window_handles[0])
            print("bủ bủ lmao")
            responseToServer = f'done|{data["id"]}'
            s.send(responseToServer.encode())
            FLAG = False
            break

s.close()