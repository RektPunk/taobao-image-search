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
                    "SmartStoreLink": _title_link.get_attribute("href"),
                    "SmartStoreTitle": _title_link.text,
                    "ProductLink": _product_link.get_attribute("href"),
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

    def _get_best_products_link(
        self,
        _smart_store_link: str,
        wait_int: int = 1,
    ):
        self.driver.implicitly_wait(wait_int)
        self.driver.get(_smart_store_link)
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
        wait_int: int = 1,
    ) -> pd.DataFrame:
        best_products_with_store_info = []
        for store_info in self._store_infos:
            _smart_store_link = store_info["ProductLink"]
            try:
                _best_products = self._get_best_products_link(
                    _smart_store_link=_smart_store_link, wait_int=wait_int
                )
            except:
                continue
            if len(_best_products) == 0:
                continue
            store_info.update({"BestProducts": _best_products})
            best_products_with_store_info.append(store_info)

        best_products_df = pd.DataFrame(best_products_with_store_info).explode(
            "BestProducts"
        )
        self.best_products_df = best_products_df
        return best_products_df
