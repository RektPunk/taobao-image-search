import os
from time import sleep
from typing import Dict, List
from datetime import datetime
import requests
from urllib import parse
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from module.naver.variables import (
    NaverStoreInfoUrl,
    NaverStoreInfoVariables,
    NaverBestProductVariables,
    NaverBestProductDetailVariables,
    NaverCategoryInfoVariables,
)


def _generate_url(
    orig_query: str,
    paging_index: int,
    min_price: int,
    max_price: int,
) -> str:
    encoded_orig_query = parse.quote(orig_query)
    return NaverStoreInfoUrl.NAVER_STORE_INFO_URL.format(
        min_price=min_price,
        max_price=max_price,
        orig_query=encoded_orig_query,
        paging_index=paging_index,
    )


class NaverStoreInfoScrapper:
    def __init__(
        self,
        wait_int: int,
        min_price: int,
        max_price: int,
        implicitly_wait_int: int = 5,
    ):
        self.driver = webdriver.Chrome("../driver/chromedriver")
        self.wait_int: int = wait_int
        self.implicitly_wait_int: int = implicitly_wait_int
        self.driver.implicitly_wait(self.implicitly_wait_int)
        self._now: str = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        self.store_infos: List = []
        self.best_product_details: List = []
        self.min_price = min_price
        self.max_price = max_price

    def _get_page(
        self,
        url: str,
    ):
        self.driver.get(url)
        sleep(self.wait_int)
        self.driver.implicitly_wait(self.implicitly_wait_int)
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def _get_store_infos_for_each_page(
        self,
    ) -> Dict[str, str]:
        malls = self.driver.find_elements(
            by=By.XPATH, value=NaverStoreInfoVariables.BASICLIST_MALL_AREA
        )
        product_infos = self.driver.find_elements(
            by=By.XPATH, value=NaverStoreInfoVariables.BASICLIST_INFO_AREA
        )
        smart_store_info = []
        for mall, product_info in zip(malls, product_infos):
            _mall_grade = mall.find_element(
                by=By.XPATH, value=NaverStoreInfoVariables.BASICLIST_MALL_GRADE
            ).text

            if _mall_grade != "":
                continue

            _title_link = mall.find_element(
                by=By.XPATH, value=NaverStoreInfoVariables.BASICLIST_MALL_TITLE
            ).find_element(by=By.CSS_SELECTOR, value="a")

            _product_link = product_info.find_element(
                by=By.XPATH, value=NaverStoreInfoVariables.BASICLIST_INFO_TITLE
            ).find_element(by=By.CSS_SELECTOR, value="a")
            smart_store_info.append(
                {
                    "smart_store_link": _title_link.get_attribute("href"),
                    "smart_store_title": _title_link.text,
                    "product_link": _product_link.get_attribute("href"),
                }
            )
        return smart_store_info

    def get_store_infos(
        self,
        orig_query: str,
        paging_index_limit: int,
    ) -> Dict[str, str]:
        self.orig_query = orig_query
        _store_infos = []
        for paging_index in range(1, paging_index_limit + 1):
            _url = _generate_url(
                min_price=self.min_price,
                max_price=self.max_price,
                orig_query=orig_query,
                paging_index=paging_index,
            )
            self._get_page(_url)
            _store_infos_paging_index = self._get_store_infos_for_each_page()
            _store_infos = _store_infos + _store_infos_paging_index

        _deduplicated_store_infos_target = self.store_infos + _store_infos
        _deduplicated_store_infos = [
            dict(_store_info_tuple)
            for _store_info_tuple in {
                tuple(_store_info.items())
                for _store_info in _deduplicated_store_infos_target
            }
        ]
        self.store_infos = _deduplicated_store_infos

    def _get_best_products_link(
        self,
        _smart_store_link: str,
    ):
        self._get_page(_smart_store_link)
        elements_role_presentation = self.driver.find_elements(
            by=By.CSS_SELECTOR, value=NaverBestProductVariables.LI_ROLE_PRESENTATION
        )
        product_links = []
        for element in elements_role_presentation:
            if "찜하기" not in element.text:
                pass
            if "상세정보" in element.text:
                break
            product_link = element.find_element(
                by=By.CSS_SELECTOR,
                value=NaverBestProductVariables.A_CLASS_LINKANCHOR,
            ).get_attribute("href")
            product_links.append(product_link)
        return product_links

    def get_best_products(
        self,
    ):
        _key_cols = [
            "smart_store_title",
            "smart_store_link",
            "best_product_link",
        ]
        best_products_with_store_info = []
        for store_info in self.store_infos:
            _smart_store_link = store_info["product_link"]
            try:
                _best_products = self._get_best_products_link(
                    _smart_store_link=_smart_store_link,
                )
            except:
                continue
            if len(_best_products) == 0:
                continue
            store_info.update({"best_product_link": _best_products})
            best_products_with_store_info.append(store_info)

        if len(best_products_with_store_info) != 0:
            best_products_df = pd.DataFrame(best_products_with_store_info).explode(
                "best_product_link"
            )
            best_products_df = (
                best_products_df[_key_cols]
                .drop_duplicates("best_product_link")
                .reset_index(drop=True)
            )
            self.best_products_df = best_products_df
        else:
            self.best_products_df = None

    def get_best_products_details(
        self,
    ):
        if self.best_products_df is None:
            return
        for _, best_product in self.best_products_df.iterrows():
            try:
                _smart_store_title = best_product["smart_store_title"]
                _smart_store_link = best_product["smart_store_link"]
                _best_product_link = best_product["best_product_link"]
                self._get_page(
                    _best_product_link,
                )
                product_title = self.driver.find_element(
                    by=By.CLASS_NAME,
                    value=NaverBestProductDetailVariables.PRODUCT_TITLE,
                ).text
                product_price_element = self.driver.find_element(
                    by=By.CLASS_NAME,
                    value=NaverBestProductDetailVariables.PRODUCT_PRICE_ELEMENT,
                )
                product_price = product_price_element.find_element(
                    by=By.CLASS_NAME,
                    value=NaverBestProductDetailVariables.PRODUCT_PRICE,
                ).text.replace(",", "")
                product_price = int(product_price)
                product_shipping_price_elements = self.driver.find_elements(
                    by=By.CLASS_NAME,
                    value=NaverBestProductDetailVariables.PRODUCT_SHIPPING_PRICE_ELEMENT,
                )
                if "무료배송" in [
                    product_shipping_price_element.text
                    for product_shipping_price_element in product_shipping_price_elements
                ]:
                    product_shipping_price = 0
                else:
                    product_shipping_price_elements = self.driver.find_elements(
                        by=By.CLASS_NAME,
                        value=NaverBestProductDetailVariables.PRODUCT_SHIPPING_PRICE,
                    )
                    product_shipping_price = int(
                        [_.text for _ in product_shipping_price_elements][0].replace(
                            ",", ""
                        )
                    )
                product_total_price = product_price + product_shipping_price
                if (
                    product_total_price < self.min_price
                    or product_total_price > self.max_price
                ):
                    continue
                tag_names = self.driver.find_elements(
                    by=By.CLASS_NAME, value=NaverBestProductDetailVariables.TAG_NAME
                )
                tag_names = ",".join(
                    [tag_name.text.replace("#", "") for tag_name in tag_names]
                )

                image_element = self.driver.find_element(
                    by=By.CLASS_NAME,
                    value=NaverBestProductDetailVariables.IMAGE_ELEMENT,
                )
                image_url = image_element.get_attribute("src")
                best_product_detail = {
                    "smart_store_title": _smart_store_title,
                    "smart_store_link": _smart_store_link,
                    "best_product_link": _best_product_link,
                    "product_title": product_title,
                    "product_price": product_price,
                    "product_total_price": product_total_price,
                    "tag_names": tag_names,
                    "image_url": image_url,
                }
                self.best_product_details.append(best_product_detail)
            except:
                print(_best_product_link)
                continue

    def get_category_name(
        self,
    ):
        for best_product_detail in self.best_product_details:
            _smart_store_title = best_product_detail["product_title"]
            _url = _generate_url(
                min_price=self.min_price,
                max_price=self.max_price,
                orig_query=_smart_store_title,
                paging_index=1,
            )
            self._get_page(_url)
            try:
                category_names = " > ".join(
                    [
                        category_name.text
                        for category_name in self.driver.find_element(
                            by=By.CLASS_NAME,
                            value=NaverCategoryInfoVariables.BASICLIST_DEPTH,
                        ).find_elements(
                            by=By.CLASS_NAME, value=NaverCategoryInfoVariables.SPAN
                        )
                    ]
                )
            except:
                category_names = ""
            finally:
                best_product_detail.update(
                    {
                        "category_names": category_names,
                    }
                )

    def save_images(
        self,
    ):
        image_folder_path = os.path.join("images", f"{self._now}")
        os.makedirs(image_folder_path, exist_ok=True)
        for best_product_detail in self.best_product_details:
            image_url = best_product_detail.get("image_url")
            _smart_store_title = best_product_detail.get("smart_store_title")
            product_title = best_product_detail.get("product_title")
            img_data = requests.get(image_url).content
            image_path = os.path.join(
                image_folder_path,
                f"{_smart_store_title}_{product_title}.png",
            )
            with open(image_path, "wb") as handler:
                handler.write(img_data)
            best_product_detail.update({"image_path": image_path})

    def save_files(
        self,
    ):
        best_product_details_df = pd.DataFrame(self.best_product_details)
        if len(best_product_details_df) == 0:
            return
        best_product_details_df = best_product_details_df.assign(
            image_path=[
                f"{_idx}_{_image_path}"
                for _idx, _image_path in zip(
                    best_product_details_df.index, best_product_details_df["image_path"]
                )
            ]
        )
        tsv_path = os.path.join("files", f"{self._now}.tsv")
        best_product_details_df.to_csv(tsv_path, sep="\t", index=False)

    def close(self):
        self.driver.close()
