from typing import Dict
from urllib import parse
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

from module.naver.variables import NaverStoreInfoVariables, NaverBestProductVariables


class _NaverStoreInfoUrl:
    NAVER_STORE_INFO_URL: str = "https://search.shopping.naver.com/search/all?agency=true&frm=NVSHCHK&origQuery={orig_query}&pagingIndex={paging_index}&pagingSize=20&productSet=checkout&query={orig_query}&sort=rel&timestamp=&viewType=list"


def _generate_url(orig_query: str, paging_index: int) -> str:
    encoded_orig_query = parse.quote(orig_query)
    return _NaverStoreInfoUrl.NAVER_STORE_INFO_URL.format(
        orig_query=encoded_orig_query,
        paging_index=paging_index,
    )


class NaverStoreInfoScrapper:
    def __init__(self, wait_int: int = 10):
        self.driver = webdriver.Chrome("../driver/chromedriver")
        self.driver.implicitly_wait(wait_int)

    def __call__(self):
        return self.driver

    def close(self):
        self.driver.close()

    def _init_naver(
        self,
        orig_query: str,
        paging_index: int,
    ):
        _url = _generate_url(orig_query=orig_query, paging_index=paging_index)
        self._url = _url
        self.driver.get(_url)
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def _get_store_infos_for_each_page(
        self,
    ) -> Dict[str, str]:
        malls = self.driver.find_elements(
            by=By.XPATH, value=NaverStoreInfoVariables.BASICLIST_MALL_AREA
        )
        smart_store_info = []
        for mall in malls:
            _mall_grade = mall.find_element(
                by=By.XPATH, value=NaverStoreInfoVariables.BASICLIST_MALL_GRADE
            ).text
            if _mall_grade != "":
                continue
            _title_link = mall.find_element(
                by=By.XPATH, value=NaverStoreInfoVariables.BASICLIST_MALL_TITLE
            ).find_element(by=By.CSS_SELECTOR, value="a")
            smart_store_info.append(
                {
                    "SmartStoreLink": _title_link.get_attribute("href"),
                    "SmartStoreTitle": _title_link.text,
                }
            )
        return smart_store_info

    def get_store_infos(
        self,
        orig_query: str,
        paging_index_limit: int,
    ) -> Dict[str, str]:
        _store_infos = []
        for paging_index in range(1, paging_index_limit + 1):
            self._init_naver(orig_query=orig_query, paging_index=paging_index)
            _store_infos_paging_index = self._get_store_infos_for_each_page()
            _store_infos = _store_infos + _store_infos_paging_index

        _deduplicated_store_infos = [
            dict(_store_info_tuple)
            for _store_info_tuple in {
                tuple(_store_info.items()) for _store_info in _store_infos
            }
        ]
        self._store_infos = _deduplicated_store_infos
        return _deduplicated_store_infos

    def get_best_products(
        self,
        wait_int: int = 1,
    ) -> pd.DataFrame:
        best_products_with_store_info = []
        for store_info in self._store_infos:
            _smart_store_link = store_info["SmartStoreLink"]
            self.driver.implicitly_wait(wait_int)
            self.driver.get(_smart_store_link)
            best_products_widget = self.driver.find_element(
                by=By.ID, value=NaverBestProductVariables.PC_BEST_PRODUCT_WIDGET
            )
            if best_products_widget.text == "":
                continue
            best_products = best_products_widget.find_elements(
                by=By.CSS_SELECTOR, value=NaverBestProductVariables.LI
            )
            best_product_link = [
                best_product.find_element(
                    by=By.CSS_SELECTOR, value=NaverBestProductVariables.A
                ).get_attribute("href")
                for best_product in best_products
            ]
            store_info.update({"BestProducts": best_product_link})
            best_products_with_store_info.append(store_info)

        best_products_df = pd.DataFrame(best_products_with_store_info).explode(
            "BestProducts"
        )
        self.best_products_df = best_products_df
        return best_products_df
