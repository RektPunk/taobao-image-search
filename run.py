from module.naver.store_scrapper import NaverStoreInfoScrapper


naver_store_info_scrapper = NaverStoreInfoScrapper()
store_info_dict = naver_store_info_scrapper.get_store_infos(
    orig_query="접이식 의자 원룸",
    paging_index_limit=4,
)
best_products_df = naver_store_info_scrapper.get_best_products()
best_products_df.to_csv("test.csv")
