import socket
import datetime
from datetime import datetime
from selenium import webdriver
from time import sleep
import json

# --- init driver ---

LIVE = None
COOKIE = None
# driver = webdriver.Firefox()
# def initBrowser():
#     driver.get("https://www.nimo.tv/lives")
#     print('start browser...')
#     get_site_info()
#
#
# def get_site_info():
#     print('URL:', driver.current_url)
#     print('Title:', driver.title)
#     now = datetime.now()
#     current_time = now.strftime("%H:%M:%S")
#     print('thời gian bắt đầu chạy: ' + current_time)
#
#
# def loginUsingCookies():
#     driver.delete_all_cookies()
#     for cookie in COOKIE["cookies"]:
#         cookie.pop('sameSite')
#         driver.add_cookie(cookie)
#     driver.refresh()
#
#
# def openLiveInNewTab(url):
#     driver.switch_to.new_window('tab')
#     driver.get(url)
#     collectEggs()
#
#
# def collectEggs():
#     script = "let button = document.querySelector('.pl-icon_danmu_open');" \
#              "if(button) button.click();" \
#              "collectInterval = setInterval(function(){" \
#              "const boxGift = document.querySelector('.nimo-box-gift__box');" \
#              "const collectBtn = document.querySelector('.nimo-box-gift__box__btn');" \
#              "let isBoxGift = document.querySelector('.nimo-room__chatroom__box-gift-item');" \
#              "if(!boxGift) window.close();" \
#              "if(collectBtn) collectBtn.click();" \
#              "if(window.getComputedStyle(isBoxGift).display == 'none') window.close();" \
#              "}, 1);"
#
#     driver.execute_script(script)

#
# # wait for server


# initBrowser()


s = socket.socket()
host = '127.0.0.1' #my server ip
port = 9991
print(f'connected to {host}:{port}')


s.connect((host, port))

while True:
    data = s.recv(10024)
    data = data.decode()
    print(data)
    # sleep(40)
    # rep = 'done'
    # s.send(rep.encode())
    # try:
    #     data = json.loads(data)
    #     LIVE = data['link']
    #     COOKIE = data['account']
    #     if COOKIE and LIVE:
    #         loginUsingCookies()
    #         openLiveInNewTab(LIVE)
    # except:
    #     print(data)


s.close()