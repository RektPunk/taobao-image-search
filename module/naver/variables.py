class NaverStoreInfoVariables:
    BASICLIST_MALL_AREA: str = "//div[starts-with(@class, 'basicList_mall_area')]"
    BASICLIST_INFO_AREA: str = "//div[starts-with(@class, 'basicList_info_area')]"
    BASICLIST_MALL_GRADE: str = "div[starts-with(@class, 'basicList_mall_grade')]"
    BASICLIST_MALL_TITLE: str = "div[starts-with(@class, 'basicList_mall_title')]"
    BASICLIST_INFO_TITLE: str = "div[starts-with(@class, 'basicList_title')]"


class NaverBestProductVariables:
    LI_ROLE_PRESENTATION: str = "li[role='presentation']"
    A_CLASS_LINKANCHOR: str = "a[class$='linkAnchor']"
