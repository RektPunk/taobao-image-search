import yaml
from module.naver.store_scrapper import NaverStoreInfoScrapper


if __name__ == "__main__":
    with open("input_querys.yaml", "r", encoding="utf-8") as input_querys_yaml:
        input_querys = yaml.load(input_querys_yaml, Loader=yaml.FullLoader)

    naver_store_info_scrapper = NaverStoreInfoScrapper()
    for input_query in input_querys:
        _query = input_query.get("query")
        _page_limit = input_query.get("page_limit")
        if _page_limit is None:
            _page_limit = 3  ## Default

        naver_store_info_scrapper.get_store_infos(
            orig_query=_query,
            paging_index_limit=int(_page_limit),
        )

    naver_store_info_scrapper.get_best_products()
    naver_store_info_scrapper.get_best_products_details()
    naver_store_info_scrapper.get_category_name()
    naver_store_info_scrapper.save_files()
    naver_store_info_scrapper.close()
