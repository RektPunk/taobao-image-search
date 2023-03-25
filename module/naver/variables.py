class NaverStoreInfoUrl:
    NAVER_STORE_INFO_URL: str = "https://search.shopping.naver.com/search/all?agency=true&frm=NVSHCHK&origQuery={orig_query}&pagingIndex={paging_index}&pagingSize=20&productSet=checkout&query={orig_query}&sort=rel&timestamp=&viewType=list"


class NaverStoreInfoVariables:
    BASICLIST_MALL_AREA: str = "//div[starts-with(@class, 'basicList_mall_area')]"
    BASICLIST_INFO_AREA: str = "//div[starts-with(@class, 'basicList_info_area')]"
    BASICLIST_MALL_GRADE: str = "div[starts-with(@class, 'basicList_mall_grade')]"
    BASICLIST_MALL_TITLE: str = "div[starts-with(@class, 'basicList_mall_title')]"
    BASICLIST_INFO_TITLE: str = "div[starts-with(@class, 'basicList_title')]"


class NaverBestProductVariables:
    LI_ROLE_PRESENTATION: str = "li[role='presentation']"
    A_CLASS_LINKANCHOR: str = "a[class$='linkAnchor']"


class NaverBestProductDetailVariables:
    CATEGORY: str = "_3bYOrjr_7d"
    PRODUCT_TITLE: str = "_22kNQuEXmb"
    PRODUCT_PRICE_ELEMENT: str = "aICRqgP9zw"
    PRODUCT_PRICE: str = "_1LY7DqCnwR"
    PRODUCT_SHIPPING_PRICE_ELEMENT: str = "bd_ChMMo"
    PRODUCT_SHIPPING_PRICE: str = "bd_3uare"
    TAG_NAME: str = "_3SMi-TrYq2"
    IMAGE_ELEMENT: str = "_2RYeHZAP_4"


class NaverCategoryInfoVariables:
    BASICLIST_DEPTH: str = "basicList_depth__SbZWF"
    SPAN: str = "basicList_category__cXUaZ"
