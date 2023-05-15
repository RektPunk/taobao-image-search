import yaml
import argparse
from module.naver.store_scrapper import NaverStoreInfoScrapper

if __name__ == "__main__":
    ## Naver Store Info Scrapper
    parser = argparse.ArgumentParser()
    parser.add_argument("--wait-int", default=3, help="Set wait limit")
    parser.add_argument("--min-price", default=0, help="Set min price")
    parser.add_argument("--max-price", default=1000000, help="Set max price")
    args = parser.parse_args()
    with open("input_querys.yaml", "r", encoding="utf-8") as input_querys_yaml:
        input_querys = yaml.load(input_querys_yaml, Loader=yaml.FullLoader)
    naver_store_info_scrapper = NaverStoreInfoScrapper(
        wait_int=int(args.wait_int),
        min_price=int(args.min_price),
        max_price=int(args.max_price),
    )
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
    naver_store_info_scrapper.save_images()
    naver_store_info_scrapper.save_files()
    naver_store_info_scrapper.close()
