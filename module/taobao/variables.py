class TaoBaoInfoVariables:
    SEARCHBAR_INPUT_AREA: str = "//div[@class='rax-view searchbar-input-wrap']//input"
    COMPONENT_PREVIEW_BUTTON: str = "//div[@class='component-preview-button']"
    FIRST_ITEM: str = (
        "//div[contains(@class, 'rax-view-v2')][contains(@class, 'list--')]//a"
    )


class TaoBaoUrls:
    TAOBAO_URL: str = "https://world.taobao.com/"
    TAOBAO_DIRECT_URL = (
        "https://item.taobao.com/item.htm?id={item_id}&&ttid={ttid}&sid={sid}"
    )
