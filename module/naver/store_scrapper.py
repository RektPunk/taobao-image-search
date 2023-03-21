from typing import Dict
from urllib import parse
from selenium import webdriver
from selenium.webdriver.common.by import By

from module.naver.variables import NaverStoreInfoXpath


class _NaverStoreInfoUrl:
    NAVER_STORE_INFO_URL: str = "https://search.shopping.naver.com/search/all?agency=true&frm=NVSHCHK&origQuery={orig_query}&pagingIndex={paging_index}&pagingSize=20&productSet=checkout&query={orig_query}&sort=rel&timestamp=&viewType=list"


def _generate_url(orig_query: str, paging_index: int) -> str:
    encoded_orig_query = parse.quote(orig_query)
    return _NaverStoreInfoUrl.NAVER_STORE_INFO_URL.format(
        orig_query=encoded_orig_query,
        paging_index=paging_index,
    )


class NaverStoreInfoScrapper:
    def __init__(self):
        self.driver = webdriver.Chrome("../driver/chromedriver")
        self.driver.implicitly_wait(10)

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

    def _get_infos(
        self,
    ) -> Dict[str, str]:
        malls = self.driver.find_elements(
            by=By.XPATH, value=NaverStoreInfoXpath.BASICLIST_MALL_AREA
        )
        smart_store_info = []
        for mall in malls:
            _mall_grade = mall.find_element(
                by=By.XPATH, value=NaverStoreInfoXpath.BASICLIST_MALL_GRADE
            ).text
            if _mall_grade != "":
                continue
            _title_link = mall.find_element(
                by=By.XPATH, value=NaverStoreInfoXpath.BASICLIST_MALL_TITLE
            ).find_element(by=By.CSS_SELECTOR, value="a")
            smart_store_info.append(
                {
                    "SmartStoreLink": _title_link.get_attribute("href"),
                    "SmartStoreTitle": _title_link.text,
                }
            )
        return smart_store_info

    def get_infos(
        self,
        orig_query: str,
        paging_index_limit: int,
    ) -> Dict[str, str]:
        _store_infos = []
        for paging_index in range(1, paging_index_limit + 1):
            self._init_naver(orig_query=orig_query, paging_index=paging_index)
            _store_infos_paging_index = self._get_infos()
            _store_infos = _store_infos + _store_infos_paging_index

        _deduplicated_store_infos = [
            dict(_store_info_tuple)
            for _store_info_tuple in {
                tuple(_store_info.items()) for _store_info in _store_infos
            }
        ]
        return _deduplicated_store_infos
