from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from PIL import Image
from io import BytesIO
import win32clipboard
import os
import datetime
import pandas as pd
from module.taobao.variables import TaoBaoInfoVariables


# 기능 구현 완료 format 맞추기 필요
class TaoBaoInfoScrapper:
    def __init__(self, wait_int: int = 5):
        self.driver = webdriver.Chrome("../driver/chromedriver")
        self.wait_int = wait_int
        self.driver.implicitly_wait(self.wait_int)
        self.today = datetime.date.today().strftime("%Y%m%d")
        self.image_folder = "images"
        self.file_path = "files/" + self.today + "_item.csv"
        self.image_count = 0

    def __call__(self):
        return self.driver

    def close(self):
        self.driver.close()

    def _send_to_clipboard(self, clip_type, data):
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(clip_type, data)
        win32clipboard.CloseClipboard()

    def _copy_to_clipboard(self, image_path: str):
        image = Image.open(image_path)

        output = BytesIO()
        image.convert("RGB").save(output, "BMP")
        data = output.getvalue()[14:]
        output.close()
        self._send_to_clipboard(win32clipboard.CF_DIB, data)

    def _write_url_file(self, data, file_path):
        with open(file_path, mode="a", newline="") as file:
            df = pd.DataFrame(data)
            df.to_csv(file, index=False, header=not file.tell())

    def _search_taobao_images(
        self,
        image_path: str,
        file_path: str,
    ):
        # WEB URL
        self.driver.get(TaoBaoInfoVariables.TAOBAO_URL)

        # 파일 업로드를 위한 input 요소 클릭
        upload_element = self.driver.find_element(
            by=By.XPATH, value=TaoBaoInfoVariables.SEARCHBAR_INPUT_AREA
        )
        upload_element.click()
        ActionChains(self.driver).key_down(Keys.CONTROL).send_keys("v").key_up(
            Keys.CONTROL
        ).perform()

        # submit button 요소 클릭
        submit_element = self.driver.find_element(
            by=By.XPATH, value=TaoBaoInfoVariables.COMPONENT_PREVIEW_BUTTON
        )
        submit_element.click()

        # 새창 핸들로 변경
        self.image_count += 1
        self.driver.switch_to.window(self.driver.window_handles[self.image_count])

        # XPath로 요소 찾기
        element = self.driver.find_element(
            by=By.XPATH, value=TaoBaoInfoVariables.FIRST_ITEM
        )
        url_path = element.get_attribute("href")

        data = [{"image_path": image_path, "url_path": url_path}]
        self._write_url_file(data, file_path)

    def get_store_infos(self):
        for image in os.listdir(self.image_folder):
            if image.endswith(("jpg", "jpeg", "png")):
                image_path = self.image_folder + "/" + image
                self._copy_to_clipboard(image_path)
                self._search_taobao_images(image_path, self.file_path)
            else:
                pass
