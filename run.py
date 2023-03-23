import argparse
from module.naver.store_scrapper import NaverStoreInfoScrapper


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", help="Input query")
    parser.add_argument("--page-limit", default=1, help="Set page limit")
    args = parser.parse_args()
    assert args.query is not None, "query is None."
    naver_store_info_scrapper = NaverStoreInfoScrapper()
    store_info_dict = naver_store_info_scrapper.get_store_infos(
        orig_query=args.query,
        paging_index_limit=args.page_limit,
    )
    naver_store_info_scrapper.get_best_products()
    best_products_df = naver_store_info_scrapper.get_best_products_details()
    naver_store_info_scrapper.close()
