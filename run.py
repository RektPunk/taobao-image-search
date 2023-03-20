# %%
from module.naver.store_scrapper import NaverStoreInfoScrapper


naver_store_info_scrapper = NaverStoreInfoScrapper()
naver_store_info_scrapper.init_naver(
    orig_query="접이식 의자 원룸",
    paging_index=1,
)
naver_store_info_scrapper.get_infos()
