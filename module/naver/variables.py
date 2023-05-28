class NaverStoreInfoUrl:
    NAVER_STORE_INFO_URL: str = "https://search.shopping.naver.com/search/all?agency=true&frm=NVSHCHK&origQuery={orig_query}&pagingIndex={paging_index}&pagingSize=20&productSet=checkout&query={orig_query}&sort=rel&timestamp=&viewType=list"


class NaverStoreInfoVariables:
    PRODUCT_MALL_AREA: str = "//div[starts-with(@class, 'product_mall_area')]"
    PRODUCT_INFO_AREA: str = "//div[starts-with(@class, 'product_info_area')]"
    PRODUCT_MALL_GRADE: str = "div[starts-with(@class, 'product_mall_grade')]"
    PRODUCT_MALL_TITLE: str = "div[starts-with(@class, 'product_mall_title')]"
    PRODUCT_INFO_TITLE: str = "div[starts-with(@class, 'product_title')]"


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
    PRODUCT_DEPTH: str = "product_depth__I4SqY"
    PRODUCT_CATEGORY: str = "product_category__l4FWz"
