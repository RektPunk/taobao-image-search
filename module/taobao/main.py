from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from PIL import Image
from io import BytesIO
import win32clipboard
import pandas as pd
import os
import datetime

def send_to_clipboard(clip_type, data):
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(clip_type, data)
    win32clipboard.CloseClipboard()

def copy_to_clipboard(image_path):
    
    image = Image.open(image_path)

    output = BytesIO()
    image.convert("RGB").save(output, "BMP")
    data = output.getvalue()[14:]
    output.close()

    send_to_clipboard(win32clipboard.CF_DIB, data)


def search_taobao_images(image_path, file_path):
    # web url
    web_url = 'https://world.taobao.com/'

    driver = webdriver.Chrome('./driver/chromedriver')
    driver.implicitly_wait(5)
    driver.get(web_url)

    # 파일 업로드를 위한 input 요소 클릭
    upload_element = driver.find_element(
        by=By.XPATH,
        value="//div[@class='rax-view searchbar-input-wrap']//input"
    )
    upload_element.click()
    ActionChains(driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()

    submit_element = driver.find_element(
        by=By.XPATH,
        value="//div[@class='component-preview-button']"
    )
    submit_element.click()
    
    # 새창 핸들로 변경
    driver.switch_to.window(driver.window_handles[1])
    print(driver.title)

    # XPath로 요소 찾기
    element = driver.find_element(by=By.XPATH, value="//div[contains(@class, 'rax-view-v2')][contains(@class, 'list--')]//a")
    url_path = element.get_attribute("href")
    
    data = [
        {"image_path": image_path, "url_path": url_path}
    ]
    write_url_file(data, file_path)
    

def write_url_file(data, file_path):
    with open(file_path, mode="a", newline="") as file:
        df = pd.DataFrame(data)
        df.to_csv(file, index=False, header=not file.tell())


if __name__ == "__main__":
    # 파일 경로 입력
    today = datetime.date.today().strftime('%Y%m%d')
    image_folder = "images"
    file_path = "files/"+today+"_item.csv"
    for image in os.listdir(image_folder):
        image_path = image_folder + "/" + image
        copy_to_clipboard(image_path)
        search_taobao_images(image_path, file_path)