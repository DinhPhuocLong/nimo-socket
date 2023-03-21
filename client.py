import socket
import datetime
from datetime import datetime
from selenium import webdriver
from time import sleep
import threading
import json
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


driver = webdriver.Chrome('/chromedriver.exe')

# --- init driver ---

LIVE = None
COOKIE = None
FLAG = False

with open("config.json", 'r') as f:
    data = json.load(f)
    port = data["port"]
    server = data["server"]
    loadScript = data["load-script"]
    tabQuantity = data["tab-quantity"]

def initBrowser():
    driver.get("https://www.nimo.tv/lives")
    print('start browser...')
    get_site_info()
    try:
        loginUsingUsernamePassword()
    except:
        sleep(10)
        loginUsingUsernamePassword()


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

def loginUsingUsernamePassword():
    code = ""
    username = ""
    password = ""
    with open("info.json", 'r') as f:
        data = json.load(f)
        if data["code"] == 66:
            code = "Thailand"
        if data["code"] == 84:
            code = "Vietnam"
        username = data["username"]
        password = data["password"]

    sleep(1)
    loginButton = driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div/div[2]/div/div[2]/button")
    loginButton.click()
    sleep(1)
    dropDown = driver.find_element(By.CLASS_NAME, "nimo-area-code")
    dropDown.click()
    sleep(1)
    countryPath = '//div[text()="'+ code +'"]'
    countryCode = driver.find_element(By.XPATH, countryPath)
    countryCode.click()
    sleep(1)
    userName = driver.find_element(By.CLASS_NAME, "phone-number-input")
    userName.click()
    actions = ActionChains(driver)
    actions.send_keys(username)
    actions.send_keys(Keys.TAB)
    actions.send_keys(password)
    actions.send_keys(Keys.ENTER)
    actions.perform()


def openLiveInNewTab(url):
    global FLAG
    FLAG = True
    if len(driver.window_handles) >= int(tabQuantity):
        driver.switch_to.window(driver.window_handles[1])
        driver.close()
    driver.switch_to.window(driver.window_handles[0])
    driver.switch_to.new_window('tab')
    try:
        driver.get(url)
        print('-------------')
        sleep(int(loadScript))
        collectEggs()
    except:
        driver.close()

def collectEggs():
    driver.execute_script("""
        console.log('loaded script===================')
        function collectEgg() {
        const button = document.querySelector('.pl-icon_danmu_open');
        if (button) button.click();
        let flag = true;
        collectInterval = setInterval(function () {
                const collectBtn = document.querySelector('.nimo-box-gift__box__btn');
                const redEgg = document.querySelector('.interactive-gift-entry-box-wrap');
                if (redEgg) redEgg.click();
                let isBoxGift = document.querySelector('.nimo-room__chatroom__box-gift');
                if (collectBtn) collectBtn.click();
                const modal = document.querySelector('.act-interactive-gift-modal');
                const container = document.querySelector('.gift-entries-swiper');
                if (container) {
                    const nodeList = container.querySelectorAll('.nimo-room__chatroom__box-gift-item');
                    const nodeListToArray = [...nodeList];
                    const ifHasBoxgift = nodeListToArray.some(item => {
                        const el = item.querySelector('.nimo-box-gift') || item.querySelector('.interactive-gift-entry-box-wrap');
                        if (el) {
                            return window.getComputedStyle(el).display == 'block' || window.getComputedStyle(el).display == 'flex'
                        }
                    })
                    if (!ifHasBoxgift) window.close();
                }
                if (modal) {
                    const iframe = modal.querySelector('iframe');
                    if (iframe) {
                        let innerDoc = iframe.contentDocument || iframe.contentWindow.document;
                        if (innerDoc && flag == true) {
                            let joinButton = innerDoc.querySelector('.btn');
                            if (joinButton) {
                                joinButton.click();
                                flag = false;
                            }
                            let result = innerDoc.querySelector('.ig-result');
                            console.log('closeing');
                                if (result) {
                                    flag = true;
                                    let close = innerDoc.querySelector('.act-interactive-gift-modal-close');
                                    if (close) {
                                        close.click();
                                    }
                                }
                            }
                        }
                    }

                }, 1);
        }
        collectEgg();
    """)
# wait for server



initBrowser()


s = socket.socket()
host = server #my server ip   103.178.234.58
port = port  # Production port 9981

s.connect((host, port))
connected = True
print(f'connected to {host}:{port}')


while True:
    # attempt to send and receive wave, otherwise reconnect
    try:
        data = s.recv(1024)
        data = data.decode()
        data = json.loads(data)
        LIVE = data['link']
        print(LIVE)
        openLiveInNewTab(LIVE)
    except socket.error:
        # set connection status and recreate socket
        connected = False
        s = socket.socket()
        print("connection lost... reconnecting")
        while not connected:
            # attempt to reconnect, otherwise sleep for 4 seconds
            try:
                s.connect((host, port))
                connected = True
                print("re-connection successful")
            except socket.error:
                print('re-connection failed - sleep 4 seconds')
                sleep(4)
