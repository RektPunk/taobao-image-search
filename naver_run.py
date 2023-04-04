import yaml
import argparse
from module.naver.store_scrapper import NaverStoreInfoScrapper
from module.taobao.store_scrapper import TaoBaoInfoScrapper

if __name__ == "__main__":
    ## Naver Store Info Scrapper
    parser = argparse.ArgumentParser()
    parser.add_argument("--wait-int", default=3, help="Set wait limit")
    args = parser.parse_args()
    with open("input_querys.yaml", "r", encoding="utf-8") as input_querys_yaml:
        input_querys = yaml.load(input_querys_yaml, Loader=yaml.FullLoader)
    naver_store_info_scrapper = NaverStoreInfoScrapper(wait_int=int(args.wait_int))
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

    ## TaoBao Info Scrapper
    taobao_info_scrapper = TaoBaoInfoScrapper()
    taobao_info_scrapper.get_store_infos()
    taobao_info_scrapper.close()
