from module.taobao.store_scrapper import TaoBaoInfoScrapper

if __name__ == "__main__":
    ## TaoBao Info Scrapper
    taobao_info_scrapper = TaoBaoInfoScrapper()
    taobao_info_scrapper.get_store_infos()
    taobao_info_scrapper.close()
