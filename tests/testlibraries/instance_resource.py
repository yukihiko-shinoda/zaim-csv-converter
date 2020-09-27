"""This module implements fixture of instance."""
from pathlib import Path

from tests.testlibraries.database_for_test import FixtureRecord
from zaimcsvconverter.inputcsvformats.amazon import AmazonRowData
from zaimcsvconverter.inputcsvformats.amazon_201911 import Amazon201911RowData
from zaimcsvconverter.inputcsvformats.gold_point_card_plus import GoldPointCardPlusRowData
from zaimcsvconverter.inputcsvformats.gold_point_card_plus_201912 import GoldPointCardPlus201912RowData
from zaimcsvconverter.inputcsvformats.mufg import MufgRowData
from zaimcsvconverter.inputcsvformats.sf_card_viewer import SFCardViewerRowData
from zaimcsvconverter.inputcsvformats.view_card import ViewCardRowData
from zaimcsvconverter.inputcsvformats.waon import WaonRowData
from zaimcsvconverter.models import FileCsvConvertId, ItemRowData, StoreRowData


# Reason: Guarding for the future when it comes to calculating constants
# pylint: disable=too-few-public-methods
class InstanceResource:
    """This class implements fixture of instance."""

    PATH_PROJECT_HOME_DIRECTORY = Path(__file__).parent.parent.parent
    ROW_DATA_WAON_PAYMENT_FAMILY_MART_KABUTOCHOEIDAIDORI = WaonRowData("2018/8/7", "ファミリーマートかぶと町永代", "129円", "支払", "-")
    ROW_DATA_WAON_PAYMENT_ITABASHIMAENOCHO = WaonRowData("2018/8/30", "板橋前野町", "1,489円", "支払", "-")
    ROW_DATA_WAON_UNSUPPORTED_CHARGE_KIND = WaonRowData("2018/8/7", "ファミリーマートかぶと町永代", "129円", "支払", "クレジットカード")
    ROW_DATA_WAON_CHARGE_POINT_ITABASHIMAENOCHO = WaonRowData("2018/10/22", "板橋前野町", "1,504円", "チャージ", "ポイント")
    ROW_DATA_WAON_CHARGE_BANK_ACCOUNT_ITABASHIMAENOCHO = WaonRowData("2018/10/22", "板橋前野町", "10,000円", "チャージ", "銀行口座")
    ROW_DATA_WAON_CHARGE_CASH_ITABASHIMAENOCHO = WaonRowData("2018/10/22", "板橋前野町", "10,000円", "チャージ", "現金")
    ROW_DATA_WAON_AUTO_CHARGE_ITABASHIMAENOCHO = WaonRowData("2018/11/11", "板橋前野町", "5,000円", "オートチャージ", "銀行口座")
    ROW_DATA_WAON_DOWNLOAD_POINT_ITABASHIMAENOCHO = WaonRowData("2018/10/22", "板橋前野町", "0円", "ポイントダウンロード", "-")
    ROW_DATA_WAON_UNSUPPORTED_USE_KIND = WaonRowData("2018/8/7", "ファミリーマートかぶと町永代", "10000円", "入金", "-")
    ROW_DATA_GOLD_POINT_CARD_PLUS_AMAZON_CO_JP = GoldPointCardPlusRowData(
        "2018/7/4", "ＡＭＡＺＯＮ．ＣＯ．ＪＰ", "ご本人", "1回払い", "", "18/8", "3456", "3456", "", "", "", "", ""
    )
    ROW_DATA_GOLD_POINT_CARD_PLUS_TOKYO_ELECTRIC = GoldPointCardPlusRowData(
        "2018/7/3", "東京電力  電気料金等", "ご本人", "1回払い", "", "18/8", "11402", "11402", "", "", "", "", ""
    )
    ROW_DATA_GOLD_POINT_CARD_PLUS_201912_AMAZON_DOWNLOADS = GoldPointCardPlus201912RowData(
        "2019/11/09", "Ａｍａｚｏｎ　Ｄｏｗｎｌｏａｄｓ", "1969", "１", "１", "1969", ""
    )
    ROW_DATA_GOLD_POINT_CARD_PLUS_201912_AWS = GoldPointCardPlus201912RowData(
        "2019/11/03", "AMAZON WEB SERVICES (AWS.AMAZON.CO)", "66", "１", "１", "66", "0.60　USD　110.712　11 03"
    )
    ROW_DATA_GOLD_POINT_CARD_PLUS_201912_TOKYO_ELECTRIC = GoldPointCardPlus201912RowData(
        "2019/11/05", "東京電力  電気料金等", "11905", "１", "１", "11905", ""
    )
    ROW_DATA_GOLD_POINT_CARD_PLUS_201912_YAHOO_JAPAN = GoldPointCardPlus201912RowData(
        "2019/10/31", "ヤフージャパン", "1045", "１", "１", "1045", ""
    )
    ROW_DATA_MUFG_INCOME_CARD = MufgRowData("2018/10/1", "カ−ド", "", "", "10000", "3000000", "", "", "入金")
    ROW_DATA_MUFG_INCOME_NOT_CARD = MufgRowData(
        "2018/10/1", "振込９", "フリコミモト－アカウント", "", "10000", "3000000", "", "", "入金"
    )
    ROW_DATA_MUFG_PAYMENT = MufgRowData("2018/11/5", "カ−ド", "", "9000", "", "4000000", "", "", "支払い")
    ROW_DATA_MUFG_TRANSFER_INCOME_NOT_OWN_ACCOUNT = MufgRowData(
        "2018/8/20", "利息", "スーパーフツウ", "", "20", "2000000", "", "", "振替入金"
    )
    ROW_DATA_MUFG_TRANSFER_INCOME_OWN_ACCOUNT = MufgRowData(
        "2018/10/20", "口座振替３", "リヨウギンコウ０２８８", "", "10000", "1000000", "", "", "振替入金"
    )
    ROW_DATA_MUFG_TRANSFER_PAYMENT_GOLD_POINT_MARKETING = MufgRowData(
        "2018/10/29", "口座振替３", "ＧＰマ−ケテイング", "59260", "", "3000000", "", "", "振替支払い"
    )
    ROW_DATA_MUFG_TRANSFER_PAYMENT_TOKYO_WATERWORKS = MufgRowData(
        "2018/11/28", "水道", "トウキヨウトスイドウ", "3628", "", "5000000", "", "", "振替支払い"
    )
    ROW_DATA_MUFG_UNSUPPORTED_NOTE = MufgRowData("2018/11/28", "水道", "トウキヨウトスイドウ", "3628", "", "5000000", "", "", "")
    ROW_DATA_SF_CARD_VIEWER_TRANSPORTATION_KOHRAKUEN_STATION = SFCardViewerRowData(
        "2018/11/13", "", "メトロ", "六本木一丁目", "", "メトロ", "後楽園", "195", "3601", ""
    )
    ROW_DATA_SF_CARD_VIEWER_SALES_GOODS = SFCardViewerRowData("2018/11/14", "", "", "", "", "", "", "480", "3005", "物販")
    ROW_DATA_SF_CARD_VIEWER_AUTO_CHARGE_AKIHABARA_STATION = SFCardViewerRowData(
        "2018/11/11", "", "JR東", "秋葉原", "", "", "", "-3000", "5022", "ｵｰﾄﾁｬｰｼﾞ"
    )
    ROW_DATA_SF_CARD_VIEWER_EXIT_BY_WINDOW_KITASENJU_STATION = SFCardViewerRowData(
        "2018/11/25", "", "東武", "北千住", "", "東武", "北千住", "0", "2621", "窓出"
    )
    ROW_DATA_SF_CARD_VIEWER_BUS_TRAM = SFCardViewerRowData(
        "2019/01/27", "", "", "", "", "", "", "195", "2896", "ﾊﾞｽ/路面等"
    )
    ROW_DATA_SF_CARD_VIEWER_UNSUPPORTED_NOTE = SFCardViewerRowData(
        "2018/11/25", "", "東武", "北千住", "", "東武", "北千住", "0", "2621", "ﾁｬｰｼﾞ"
    )
    ROW_DATA_AMAZON_ECHO_DOT = AmazonRowData(
        "2018/10/23",
        "123-4567890-1234567",
        "Echo Dot (エコードット) 第2世代 - スマートスピーカー with Alexa、ホワイト",
        "販売： Amazon Japan G.K.  コンディション： 新品",
        "4980",
        "1",
        "6276",
        "6390",
        "ローソン桜塚",
        "2018年10月23日に発送済み",
        "テストアカウント",
        "5952",
        "2018/10/23",
        "5952",
        "Visa（下4けたが1234）",
        "https://www.amazon.co.jp/gp/css/summary/edit.html?ie=UTF8&orderID=123-4567890-1234567",
        "https://www.amazon.co.jp/gp/css/summary/print.html/ref=oh_aui_ajax_dpi" "?ie=UTF8&orderID=123-4567890-1234567",
        "https://www.amazon.co.jp/gp/product/B06ZYTTC4P/ref=od_aui_detailpages01?ie=UTF8&psc=1",
    )
    ROW_DATA_AMAZON_201911_ECHO_DOT = Amazon201911RowData(
        "2019/11/09",
        "234-5678901-2345678",
        "Echo Dot (エコードット) 第2世代 - スマートスピーカー with Alexa、ホワイト",
        "販売： Amazon Japan G.K.  コンディション： 新品",
        "4980",
        "1",
        "6276",
        "6390",
        "ローソン桜塚",
        "2019年11月9日に発送済み",
        "テストアカウント",
        "5952",
        "2019/11/09",
        "5952",
        "Visa（下4けたが1234）",
        "https://www.amazon.co.jp/gp/css/summary/edit.html?ie=UTF8&orderID=234-5678901-2345678",
        "https://www.amazon.co.jp/gp/css/summary/print.html/ref=oh_aui_ajax_dpi" "?ie=UTF8&orderID=234-5678901-2345678",
        "https://www.amazon.co.jp/gp/product/B06ZYTTC4P/ref=od_aui_detailpages01?ie=UTF8&psc=1",
    )
    ROW_DATA_AMAZON_201911_AMAZON_POINT = Amazon201911RowData(
        "2019/11/09",
        "234-5678901-2345678",
        "（Amazon ポイント）",
        "※カード外支払→請求額に反映",
        "",
        "",
        "",
        "-11",
        "",
        "デジタル注文: 2019/11/9",
        "テストアカウント",
        "",
        "",
        "",
        "Visa ****1234",
        "https://www.amazon.co.jp/gp/digital/your-account/order-summary.html/ref=docs_ya_os_i"
        "?ie=UTF8&orderID=234-5678901-2345678",
        "https://www.amazon.co.jp/gp/digital/your-account/order-summary.html/ref=ppx_yo_dt_b_dpi_o00"
        "?ie=UTF8&orderID=234-5678901-2345678&print=1",
        "",
    )
    ROW_DATA_AMAZON_201911_SHIPPING_HANDLING = Amazon201911RowData(
        "2020/4/25",
        "234-5678901-2345678",
        "（配送料・手数料）",
        "※（注文全体）注文合計に反映",
        "",
        "",
        "410",
        "",
        "",
        "",
        "テストアカウント",
        "",
        "",
        "",
        "",
        "https://www.amazon.co.jp/gp/digital/your-account/order-summary.html/ref=docs_ya_os_i"
        "?ie=UTF8&orderID=234-5678901-2345678",
        "https://www.amazon.co.jp/gp/digital/your-account/order-summary.html/ref=ppx_yo_dt_b_dpi_o00"
        "?ie=UTF8&orderID=234-5678901-2345678&print=1",
        "",
    )
    ROW_DATA_AMAZON_201911_HUMMING_FINE = Amazon201911RowData(
        "2019/11/09",
        "234-5678901-2345678",
        "【大容量】ハミングファイン 柔軟剤 リフレッシュグリーンの香り 詰め替え 1200ml",
        "販売： Amazon Japan G.K.  コンディション： 新品",
        "609",
        "1",
        "",
        "",
        "ローソン桜塚",
        "2019年11月10日に発送済み",
        "テストアカウント",
        "",
        "2019/11/09",
        "",
        "Visa ****1234",
        "https://www.amazon.co.jp/gp/css/summary/edit.html?ie=UTF8&orderID=234-5678901-2345678",
        "https://www.amazon.co.jp/gp/css/summary/print.html/ref=oh_aui_ajax_dpi?ie=UTF8&orderID=234-5678901-2345678",
        "https://www.amazon.co.jp/gp/product/B07146XVB5/ref=od_aui_detailpages00?ie=UTF8&psc=1",
    )
    ROW_DATA_AMAZON_201911_MS_Learn_IN_MANGA = Amazon201911RowData(
        "2020/6/6",
        "D01-2345678-9012345",
        "マンガでわかる MS Learn: 無料でAI・クラウド・アプリ開発を学ぼう",
        "[Kindle 版] 湊川あい, 日本マイクロソフト株式会社  販売: Amazon Services International, Inc.",
        "0",
        "1",
        "0",
        "0",
        "",
        "デジタル注文: 2020/6/6",
        "テストアカウント",
        "0",
        "",
        "",
        "",
        "https://www.amazon.co.jp/gp/digital/your-account/order-summary.html"
        "/ref=docs_ya_os_i?ie=UTF8&orderID=D01-2345678-9012345",
        "https://www.amazon.co.jp/gp/digital/your-account/order-summary.html"
        "/ref=ppx_yo_dt_b_dpi_o00?ie=UTF8&orderID=D01-2345678-9012345&print=1",
        "https://www.amazon.co.jp/dp/B089M7LC28/ref=docs-os-doi_0",
    )
    ROW_DATA_VIEW_CARD_ITABASHI_STATION_AUTO_CHARGE = ViewCardRowData(
        "2020/03/21", "板橋駅　オートチャージ", "3000", "", "3000", "１回払", "", "3000", "", "", ""
    )
    ROW_DATA_VIEW_CARD_ANNUAL_FEE = ViewCardRowData(
        "2020/03/31", "カード年会費", "524", "", "524", "１回払", "", "524", "", "", ""
    )
    FIXTURE_RECORD_STORE_WAON_MAKUHARISHINTOSHIN = FixtureRecord(
        FileCsvConvertId.WAON, StoreRowData("幕張新都心", "イオンモール　幕張新都心")
    )
    FIXTURE_RECORD_STORE_WAON_ITABASHIMAENOCHO = FixtureRecord(
        FileCsvConvertId.WAON, StoreRowData("板橋前野町", "イオンスタイル　板橋前野町")
    )
    FIXTURE_RECORD_STORE_WAON_FAMILY_MART_KABUTOCHOEITAIDORI = FixtureRecord(
        FileCsvConvertId.WAON, StoreRowData("ファミリーマートかぶと町永代", "ファミリーマート　かぶと町永代通り店")
    )
    FIXTURE_RECORD_STORE_GOLD_POINT_CARD_PLUS_TOKYO_ELECTRIC = FixtureRecord(
        FileCsvConvertId.GOLD_POINT_CARD_PLUS, StoreRowData("東京電力  電気料金等", "東京電力エナジーパートナー株式会社")
    )
    FIXTURE_RECORD_STORE_GOLD_POINT_CARD_PLUS_AMAZON_CO_JP = FixtureRecord(
        FileCsvConvertId.GOLD_POINT_CARD_PLUS, StoreRowData("ＡＭＡＺＯＮ．ＣＯ．ＪＰ", "Amazon Japan G.K.")
    )
    FIXTURE_RECORD_STORE_GOLD_POINT_CARD_PLUS_AMAZON_DOWNLOADS = FixtureRecord(
        FileCsvConvertId.GOLD_POINT_CARD_PLUS, StoreRowData("Ａｍａｚｏｎ　Ｄｏｗｎｌｏａｄｓ", "Amazon Japan G.K.")
    )
    FIXTURE_RECORD_STORE_GOLD_POINT_CARD_PLUS_AWS = FixtureRecord(
        FileCsvConvertId.GOLD_POINT_CARD_PLUS,
        StoreRowData("AMAZON WEB SERVICES (AWS.AMAZON.CO)", "Amazon Web Services Japan K.K."),
    )
    FIXTURE_RECORD_STORE_MUFG_TOBU_CARD = FixtureRecord(
        FileCsvConvertId.MUFG, StoreRowData("カ）トウブカ－ドビ", "", "", "", "", "東武カード")
    )
    FIXTURE_RECORD_STORE_MUFG_EMPTY = FixtureRecord(FileCsvConvertId.MUFG, StoreRowData("", "", "", "", "", "お財布"))
    FIXTURE_RECORD_STORE_MUFG_MUFG = FixtureRecord(
        FileCsvConvertId.MUFG, StoreRowData("スーパーフツウ", "三菱UFJ銀行", "その他", "その他", "臨時収入", "")
    )
    FIXTURE_RECORD_STORE_MUFG_MUFG_TRUST_AND_BANK = FixtureRecord(
        FileCsvConvertId.MUFG, StoreRowData("リヨウギンコウ０２８８", "", "", "", "", "お財布")
    )
    FIXTURE_RECORD_STORE_MUFG_TOKYO_WATERWORKS = FixtureRecord(
        FileCsvConvertId.MUFG, StoreRowData("トウキヨウトスイドウ", "東京都水道局　経理部管理課", "水道・光熱", "水道料金", "立替金返済", "")
    )
    FIXTURE_RECORD_STORE_MUFG_GOLD_POINT_MARKETING = FixtureRecord(
        FileCsvConvertId.MUFG, StoreRowData("ＧＰマーケテイング", "", "", "", "", "ゴールドポイントカード・プラス")
    )
    FIXTURE_RECORD_STORE_MUFG_OTHER_ACCOUNT = FixtureRecord(
        FileCsvConvertId.MUFG, StoreRowData("フリコミモト－アカウント", "フリコミモト－アカウント", "", "", "臨時収入", "")
    )
    FIXTURE_RECORD_STORE_PASMO_KOHRAKUEN_STATION = FixtureRecord(
        FileCsvConvertId.SF_CARD_VIEWER, StoreRowData("後楽園", "東京地下鉄株式会社　南北線後楽園駅", "交通", "電車")
    )
    FIXTURE_RECORD_STORE_PASMO_KITASENJU_STATION = FixtureRecord(
        FileCsvConvertId.SF_CARD_VIEWER, StoreRowData("北千住", "北千住", "交通", "電車")
    )
    FIXTURE_RECORD_STORE_PASMO_AKIHABARA_STATION = FixtureRecord(
        FileCsvConvertId.SF_CARD_VIEWER, StoreRowData("秋葉原", "秋葉原", "交通", "電車")
    )
    FIXTURE_RECORD_STORE_PASMO_EMPTY = FixtureRecord(FileCsvConvertId.SF_CARD_VIEWER, StoreRowData("", "", "", ""))
    FIXTURE_RECORD_ITEM_AMAZON_ECHO_DOT = FixtureRecord(
        FileCsvConvertId.AMAZON, ItemRowData("Echo Dot (エコードット) 第2世代 - スマートスピーカー with Alexa、ホワイト", "大型出費", "家電")
    )
    FIXTURE_RECORD_ITEM_AMAZON_AMAZON_POINT = FixtureRecord(
        FileCsvConvertId.AMAZON, ItemRowData("（Amazon ポイント）", "通信", "その他")
    )
    FIXTURE_RECORD_STORE_VIEW_CARD_VIEW_CARD = FixtureRecord(
        FileCsvConvertId.VIEW_CARD, StoreRowData("カード年会費", "ビューカード　ビューカードセンター", "通信", "その他")
    )
