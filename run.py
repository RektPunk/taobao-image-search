from module.naver.store_scrapper import NaverStoreInfoScrapper

naver_store_info_scrapper = NaverStoreInfoScrapper()
store_info_dict = naver_store_info_scrapper.get_store_infos(
    orig_query="접이식 바텐더 의자",
    paging_index_limit=4,
)
naver_store_info_scrapper.get_best_products()
best_products_df = naver_store_info_scrapper.get_best_products_details()
naver_store_info_scrapper.close()
