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
port = 9981  # Production port 9981

s.connect((host, port))
connected = True
print(f'connected to {host}:{port}')


while True:
    # attempt to send and receive wave, otherwise reconnect
    try:
        data = s.recv(20024)
        data = data.decode()
        data = json.loads(data)
        LIVE = data['link']
        print(LIVE)
        print(data["id"])
        COOKIE = data['account']
        loginUsingCookies()
        openLiveInNewTab(LIVE)
        while True:
            if FLAG and len(driver.window_handles) == 1:
                driver.switch_to.window(driver.window_handles[0])
                responseToServer = f'done|{data["id"]}'
                s.send(responseToServer.encode())
                FLAG = False
                break
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
                sleep(4)
s.close()