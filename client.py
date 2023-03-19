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

# --- init driver ---

LIVE = None
COOKIE = None
FLAG = False

from selenium import webdriver

# Khởi tạo driver
driver = webdriver.Chrome('/chromedriver.exe')

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
    if len(driver.window_handles) >= 3:
        driver.switch_to.window(driver.window_handles[1])
        driver.close()
    driver.switch_to.window(driver.window_handles[0])
    driver.switch_to.new_window('tab')
    driver.get(url)
    sleep(8)
    collectEggs()


def collectEggs():
    driver.execute_script("""
        var script = document.createElement('script');
script.type = "text/javascript";
script.integrity = "sha256-/xUj+3OJU5yExlq6GSYGSHk7tPXikynS7ogEvDej/m4=";
script.crossOrigin = "anonymous";
script.src = "https://code.jquery.com/jquery-3.6.0.min.js";
document.head.appendChild(script);


//
// Global variable
//
var clicked = 0;
var hasSchedule = false;
var clickingInterval = 0;
var y = -1;

function isLastEgg(jqueryObject) {
    var openedEgg = y("img[src='https://img.nimo.tv/o/banner/CA1F83CD61A6CBB290299AB8B9448A9_kelingqu.png/w152_l0/img.png']");
    var eggHasOpened = false;
    if (openedEgg && openedEgg.length > 0) {
        eggHasOpened = true;
    }

    var remainingEggCount = jqueryObject("sup[class='nimo-scroll-number nimo-badge-count nimo-badge-multiple-words']");
    if (remainingEggCount && remainingEggCount.length > 0) {
        return false;
    }

    return eggHasOpened;
}

setTimeout(function () {
    y = $;

    var x = setInterval(function () {
        var remainingTime = y("div[class='nimo-box-gift__box__cd n-as-fs12']");
        if (remainingTime.length !== 0 && !hasSchedule) {
            var innerText = remainingTime[0].innerText;
            var parts = innerText.split(":");
            var minutePart = parseInt(parts[0]);
            var secondPart = parseInt(parts[1]);
            var totalSeconds = minutePart * 60 + secondPart;

            hasSchedule = true;
            console.log("setting up schedule");
            setTimeout(function () {
                clickingInterval = setInterval(function () {
                    var egg = y("img[src='https://img.nimo.tv/o/banner/FA594DC3E0032D815464AD133760E769_daojishi.png/w152_l0/img.png']");
                    var openedEgg = y("img[src='https://img.nimo.tv/o/banner/CA1F83CD61A6CBB290299AB8B9448A9_kelingqu.png/w152_l0/img.png']");

                    if (openedEgg.length !== 0) {
                        openedEgg[0].click();
                        clicked += 1;
                    }
                    else if (egg.length !== 0) {
                        egg[0].click();
                        clicked += 1;
                    }

                    var button = y("button[class='nimo-btn nimo-btn-secondary nimo-btn-lg']");
                    if (button.length !== 0) {
                        button[0].click();
                    }

                    if (clicked > 15) {
                        clearInterval(clickingInterval);
                        clickingInterval = 0;
                        clicked = 0;
                        hasSchedule = false;
                    }
                }, 200);
            }, totalSeconds * 1000 - 800);
        }

        // Try to click opened egg
        var openedEgg = y("img[src='https://img.nimo.tv/o/banner/CA1F83CD61A6CBB290299AB8B9448A9_kelingqu.png/w152_l0/img.png']");
        if (openedEgg && openedEgg.length !== 0) {
            openedEgg.click();
        }
    }, 1000);
}, 5000);
    """)
# wait for server



initBrowser()


s = socket.socket()
host = '103.21.52.123' #my server ip   103.178.234.58
port = 9981  # Production port 9981

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
s.close()