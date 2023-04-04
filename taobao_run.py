import argparse
from module.taobao.store_scrapper import TaoBaoInfoScrapper

if __name__ == "__main__":
    ## TaoBao Info Scrapper
    parser = argparse.ArgumentParser()
    parser.add_argument("--wait-int", default=3, help="Set wait limit")
    args = parser.parse_args()

    taobao_info_scrapper = TaoBaoInfoScrapper(wait_int=int(args.wait_int))
    taobao_info_scrapper.get_product_infos()
    taobao_info_scrapper.save_files()
    taobao_info_scrapper.close()
