from playwright.sync_api import sync_playwright
import time
import pandas as pd
import pyautogui



def search_tags():
    def like_tags():
        page.click(f'//*[@id="mount_0_0_3Z"]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/main/article/div[2]/div/div[1]/div[{1}]')
        url = page.url + 'liked_by/'
        page.goto(url)
        for e in range(12):
            page.click(f'//*[@id="mount_0_0_p1"]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/main/div[1]/div/div[{e}]/div/div/div/div[3]/div/button')

    for tag in tags:
        page.goto(f"https://www.instagram.com/explore/tags/{tag}/")

def post_carrusel(page):
    path = "C:/Users/ignac/Documents/Documentos/Football/Futty Data/Automation Code/Template/Code/"
    page.click('//html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[1]/div/div/div/div/div[2]/div[7]/div/span/div/a/div')
    time.sleep(0.88)
    page.click('//html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[1]/div/div/div/div/div[2]/div[7]/div/span/div/div/div/div[1]/a[1]')
    time.sleep(0.5)
    with page.expect_file_chooser() as fc_info:
        page.locator('//html/body/div[6]/div[1]/div/div[3]/div/div/div/div/div/div/div/div[2]/div[1]/div/div/div[2]/div/button').click()
    file_chooser = fc_info.value
    file_chooser.set_files([path+'Ig post 1.png',path+'Ig post 2.png',path+'Ig post 3.png'])
    time.sleep(2)
    page.click('//html/body/div[6]/div[1]/div/div[3]/div/div/div/div/div/div/div/div[1]/div/div/div/div[3]/div/div')
    time.sleep(1.5333)
    page.click('//html/body/div[6]/div[1]/div/div[3]/div/div/div/div/div/div/div/div[1]/div/div/div/div[3]/div/div')
    time.sleep(1)
    page.click('//html/body/div[6]/div[1]/div/div[3]/div/div/div/div/div/div/div/div[2]/div[2]/div/div/div/div[1]/div[2]/div/div[1]/div[1]/p')
    time.sleep(2)
    page.type('//html/body/div[6]/div[1]/div/div[3]/div/div/div/div/div/div/div/div[2]/div[2]/div/div/div/div[1]/div[2]/div/div[1]/div[1]/p','#Hello')
    time.sleep(4)

with sync_playwright() as p:
        #browser = p.chromium.launch()
        browser = p.chromium.launch(headless=False, slow_mo=500)
        page = browser.new_page()
        page.goto("https://instagram.com")
        time.sleep(4)
        for e in range(2):
            page.keyboard.press("Shift+Tab")
        page.keyboard.press("Enter")
        page.fill('//*[@id="loginForm"]/div/div[1]/div/label/input', username)
        page.fill('//*[@id="loginForm"]/div/div[2]/div/label/input', password)
        page.click('//*[@id="loginForm"]/div/div[3]/button')

        #page.click('//*[@id="mount_0_0_7W"]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div/div/div/div')
        #time.sleep(2)
        #page.click('//*[@id="mount_0_0_pY"]/div/div/div[3]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/button[2]')
        post_carrusel(page)

    