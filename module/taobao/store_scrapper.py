import os
from datetime import datetime
from time import sleep
from io import BytesIO
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from PIL import Image
import pandas as pd
import win32clipboard
from module.taobao.variables import TaoBaoInfoVariables


def _get_product_dfs() -> pd.DataFrame:
    folder_names = [
        _folder_name
        for _folder_name in os.listdir("images")
        if ".py" not in _folder_name
    ]
    _product_dfs = [
        pd.read_csv(
            f"files/{folder_name}.tsv",
            sep="\t",
        )
        for folder_name in folder_names
    ]
    _product_dfs = pd.concat(_product_dfs, axis=0)
    return _product_dfs


# 기능 구현 완료 format 맞추기 필요
class TaoBaoInfoScrapper:
    def __init__(self, wait_int: int, implicitly_wait_int: int = 5):
        self.driver = webdriver.Chrome("../driver/chromedriver")
        self.wait_int: int = wait_int
        self.implicitly_wait_int: int = implicitly_wait_int
        self.driver.implicitly_wait(self.wait_int)
        self.product_df = _get_product_dfs()
        self._now: str = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

    def _get_page(
        self,
        url: str,
    ):
        self.driver.get(url)
        sleep(self.wait_int)
        self.driver.implicitly_wait(self.implicitly_wait_int)
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def _close_tab(
        self,
    ):
        _current_window_handle = self.driver.current_window_handle
        for window_handle in self.driver.window_handles:
            self.driver.switch_to.window(window_handle)
            if window_handle != _current_window_handle:
                self.driver.close()
        self.driver.switch_to.window(_current_window_handle)

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

    def _search_taobao_images(
        self,
    ) -> str:
        # WEB URL
        self._get_page(TaoBaoInfoVariables.TAOBAO_URL)

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
        self.driver.switch_to.window(self.driver.window_handles[-1])

        # XPath로 요소 찾기
        element = self.driver.find_element(
            by=By.XPATH, value=TaoBaoInfoVariables.FIRST_ITEM
        )
        url_path = element.get_attribute("href")
        return url_path

    def get_product_infos(self):
        _col_name = [
            "smart_store_title",
            "smart_store_link",
            "best_product_link",
            "taobao_link",
            "product_title",
            "product_price",
            "product_total_price",
            "tag_names",
            "image_path",
            "category_names",
        ]
        best_product_urls = []
        for _, row in self.product_df.iterrows():
            _image_path = row["image_path"]
            self._copy_to_clipboard(_image_path)
            try:
                best_product_url = self._search_taobao_images()
            except:
                best_product_url = ""
            best_product_urls.append(best_product_url)
            self._close_tab()

        self.product_df = self.product_df.assign(
            taobao_link=best_product_urls,
        )
        self.product_df = self.product_df[_col_name]

    def save_files(
        self,
    ):
        _product_df = pd.DataFrame(self.product_df)
        tsv_path = os.path.join("files", f"taobao_{self._now}.tsv")
        _product_df.to_csv(tsv_path, sep="\t", index=False)

    def close(self):
        self.driver.close()
