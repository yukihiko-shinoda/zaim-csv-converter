"""Expected data for integration test."""

from tests.testlibraries.row_data import ZaimRowData


def create_zaim_row_data_waon_201807() -> list[ZaimRowData]:
    """Creates expected zaim row data for WAON 201807."""
    # fmt: off
    zaim_row_data_01 = ZaimRowData(
        "2018-08-07", "payment", "食費", "食料品", "WAON", "", "", "",
        "ファミリーマート　かぶと町永代通り店", "", "0", "129", "0", "", "", "",
    )
    # fmt: on
    return [zaim_row_data_01]


def create_zaim_row_data_waon_201808() -> list[ZaimRowData]:
    """Creates expected zaim row data for WAON 201808."""
    # fmt: off
    zaim_row_data_01 = ZaimRowData(
        "2018-08-30", "payment", "食費", "食料品", "WAON", "", "", "",
        "イオンスタイル　板橋前野町", "", "0", "1489", "0", "", "", "",
    )
    # fmt: on
    return [zaim_row_data_01]


def create_zaim_row_data_waon_201810() -> list[ZaimRowData]:
    """Creates expected zaim row data for WAON 201810."""
    # fmt: off
    zaim_row_data_01 = ZaimRowData(
        "2018-10-22", "income", "その他", "-", "", "WAON", "", "",
        "イオンスタイル　板橋前野町", "", "1504", "0", "0", "", "", "",
    )
    zaim_row_data_02 = ZaimRowData(
        "2018-10-22", "transfer", "-", "-", "イオン銀行", "WAON", "", "", "", "", "0", "0", "10000", "", "", "",
    )
    # fmt: on
    return [zaim_row_data_01, zaim_row_data_02]


def create_zaim_row_data_waon_201811() -> list[ZaimRowData]:
    """Creates expected zaim row data for WAON 201811."""
    # fmt: off
    zaim_row_data_01 = ZaimRowData(
        "2018-11-11", "transfer", "-", "-", "イオン銀行", "WAON", "", "", "", "", "0", "0", "5000", "", "", "",
    )
    zaim_row_data_02 = ZaimRowData(
        "2018-11-23", "payment", "食費", "食料品", "WAON", "", "", "",
        "カルディコーヒーファーム成増店", "", "0", "-2098", "0", "", "", "",
    )
    # fmt: on
    return [zaim_row_data_01, zaim_row_data_02]


def create_zaim_row_data_gold_point_card_plus_201807() -> list[ZaimRowData]:
    """Creates expected zaim row data for GOLD POINT CARD PLUS 201807."""
    # fmt: off
    zaim_row_data_01 = ZaimRowData(
        "2018-07-03", "payment", "水道・光熱", "電気料金", "ヨドバシゴールドポイントカード・プラス", "", "", "",
        "東京電力エナジーパートナー株式会社", "", "0", "11402", "0", "", "", "",
    )
    # fmt: on
    return [zaim_row_data_01]


def create_zaim_row_data_gold_point_card_plus_201912_201807() -> list[ZaimRowData]:
    """Creates expected zaim row data for GOLD POINT CARD PLUS 201912 201807."""
    # fmt: off
    zaim_row_data_01 = ZaimRowData(
        "2020-07-03", "payment", "水道・光熱", "電気料金", "ヨドバシゴールドポイントカード・プラス", "", "", "",
        "東京電力エナジーパートナー株式会社", "", "0", "11402", "0", "", "", "",
    )
    zaim_row_data_02 = ZaimRowData(
        "2020-07-03", "payment", "通信", "インターネット関連費", "ヨドバシゴールドポイントカード・プラス", "", "", "",
        "Amazon Web Services Japan K.K.", "", "0", "66", "0", "", "", "",
    )
    # fmt: on
    return [zaim_row_data_01, zaim_row_data_02]


def create_zaim_row_data_mufg_201808() -> list[ZaimRowData]:
    """Creates expected zaim row data for MUFG 201808."""
    # fmt: off
    zaim_row_data_01 = ZaimRowData(
        "2018-08-20", "income", "その他", "-", "", "三菱UFJ銀行", "", "", "三菱UFJ銀行", "",
        "20", "0", "0", "", "", "",
    )
    # fmt: on
    return [zaim_row_data_01]


def create_zaim_row_data_mufg_201810() -> list[ZaimRowData]:
    """Creates expected zaim row data for MUFG 201810."""
    # fmt: off
    zaim_row_data_01 = ZaimRowData(
        "2018-10-01", "transfer", "-", "-", "お財布", "三菱UFJ銀行", "", "", "", "", "0", "0", "10000", "", "", "",
    )
    zaim_row_data_02 = ZaimRowData(
        "2018-10-01", "income", "臨時収入", "-", "", "三菱UFJ銀行", "", "", "フリコミモト－アカウント",  # noqa: RUF001
        "", "10000", "0", "0", "", "", "",
    )
    zaim_row_data_03 = ZaimRowData(
        "2018-10-20", "transfer", "-", "-", "お財布", "三菱UFJ銀行", "", "", "", "", "0", "0", "10000", "", "", "",
    )
    zaim_row_data_04 = ZaimRowData(
        "2018-10-29", "transfer", "-", "-", "三菱UFJ銀行", "ゴールドポイントカード・プラス",
        "", "", "", "", "0", "0", "59260", "", "", "",
    )
    # fmt: on
    return [zaim_row_data_01, zaim_row_data_02, zaim_row_data_03, zaim_row_data_04]


def create_zaim_row_data_mufg_201811() -> list[ZaimRowData]:
    """Creates expected zaim row data for MUFG 201811."""
    # fmt: off
    zaim_row_data_01 = ZaimRowData(
        "2018-11-28", "payment", "水道・光熱", "水道料金", "三菱UFJ銀行", "", "", "",
        "東京都水道局　経理部管理課", "", "0", "3628", "0", "", "", "",
    )
    # fmt: on
    return [zaim_row_data_01]


def create_zaim_row_data_mufg_202304() -> list[ZaimRowData]:
    """Creates expected zaim row data for MUFG 201811."""
    # fmt: off
    zaim_row_data_01 = ZaimRowData(
        "2023-04-22", "transfer", "-", "-", "三菱UFJ銀行", "お財布",
        "", "", "", "", "0", "0", "9000", "", "", "",
    )
    # fmt: on
    return [zaim_row_data_01]


def create_zaim_row_data_pasmo_201811() -> list[ZaimRowData]:
    """Creates expected zaim row data for PASMO 201811."""
    # fmt: off
    zaim_row_data_01 = ZaimRowData(
        "2018-11-13", "payment", "交通", "電車", "PASMO", "", "", "メトロ 六本木一丁目 → メトロ 後楽園",
        "東京地下鉄株式会社　南北線後楽園駅", "", "0", "195", "0", "", "", "",
    )
    zaim_row_data_02 = ZaimRowData(
        "2018-11-11", "transfer", "-", "-", "TOKYU CARD", "PASMO", "", "", "", "", "0", "0", "3000", "", "", "",
    )
    # fmt: on
    return [zaim_row_data_01, zaim_row_data_02]


def create_zaim_row_data_pasmo_201901() -> list[ZaimRowData]:
    """Creates expected zaim row data for PASMO 201901."""
    # fmt: off
    zaim_row_data_01 = ZaimRowData(
        "2019-01-27", "payment", "交通", "バス", "PASMO", "", "", "", "", "", "0", "195", "0", "", "", "",
    )
    # fmt: on
    return [zaim_row_data_01]


def create_zaim_row_data_amazon_201810() -> list[ZaimRowData]:
    """Creates expected zaim row data for Amazon 201810."""
    # fmt: off
    zaim_row_data_01 = ZaimRowData(
        "2018-10-23", "payment", "大型出費", "家電", "ヨドバシゴールドポイントカード・プラス", "",
        "Echo Dot (エコードット) 第2世代 - スマートスピーカー with Alexa、ホワイト", "", "Amazon Japan G.K.", "", "0",
        "4980", "0", "", "", "",
    )
    # fmt: on
    return [zaim_row_data_01]


def create_zaim_row_data_amazon_201911_201911() -> list[ZaimRowData]:
    """Creates expected zaim row data for Amazon 201911 201911."""
    # fmt: off
    zaim_row_data_01 = ZaimRowData(
        "2019-11-09", "payment", "教育・教養", "参考書", "ヨドバシゴールドポイントカード・プラス", "",
        (
            "［第2版］Python機械学習プログラミング "  # noqa: RUF001
            "達人データサイエンティストによる理論と実践 impress top gearシリーズ"
        ),
        "",
        "Amazon Japan G.K.", "", "0", "4000", "0", "", "", "",
    )
    zaim_row_data_02 = ZaimRowData(
        "2019-11-09", "payment", "通信", "その他", "ヨドバシゴールドポイントカード・プラス", "",
        "（Amazon ポイント）", "",  # noqa: RUF001
        "Amazon Japan G.K.", "", "0", "-11", "0", "", "", "",
    )
    # fmt: on
    return [zaim_row_data_01, zaim_row_data_02]


def create_zaim_row_data_amazon_201911_202004() -> list[ZaimRowData]:
    """Creates expected zaim row data for Amazon 201911 202004."""
    # fmt: off
    zaim_row_data_01 = ZaimRowData(
        "2020-04-25", "payment", "大型出費", "家電", "ヨドバシゴールドポイントカード・プラス", "",
        "【日本正規代理店品】 Drobo 5N2 NASケース(3.5インチ×5bay) ギガビットイーサネット×2 PDR-5N2",  # noqa: RUF001
        "", "Amazon Japan G.K.",
        "", "0", "79482", "0", "", "", "",
    )
    zaim_row_data_02 = ZaimRowData(
        "2020-04-25", "payment", "通信", "宅急便", "ヨドバシゴールドポイントカード・プラス", "",
        "（配送料・手数料）", "",  # noqa: RUF001
        "Amazon Japan G.K.", "", "0", "410", "0", "", "", "",
    )
    zaim_row_data_03 = ZaimRowData(
        "2020-04-25", "payment", "通信", "その他", "ヨドバシゴールドポイントカード・プラス", "",
        "（割引）", "",  # noqa: RUF001
        "Amazon Japan G.K.", "", "0", "-410", "0", "", "", "",
    )
    zaim_row_data_04 = ZaimRowData(
        "2020-04-25", "payment", "通信", "その他", "ヨドバシゴールドポイントカード・プラス", "",
        "（Amazonポイント）", "",  # noqa: RUF001
        "Amazon Japan G.K.", "", "0", "-60", "0", "", "", "",
    )
    # fmt: on
    return [
        zaim_row_data_01,
        zaim_row_data_02,
        zaim_row_data_03,
        zaim_row_data_04,
    ]


def create_zaim_row_data_amazon_201911_202006() -> list[ZaimRowData]:
    """Creates expected zaim row data for Amazon 201911 202006."""
    return []


def create_zaim_row_data_amazon_201911_202012() -> list[ZaimRowData]:
    """Creates expected zaim row data for Amazon 201911 202006."""
    # fmt: off
    zaim_row_data_01 = ZaimRowData(
        "2020-12-01", "payment", "大型出費", "家電", "ヨドバシゴールドポイントカード・プラス", "",
        "Yubico - YubiKey 5C - USB-C - 認証キー - ブラック", "", "Amazon Japan G.K.",
        "", "0", "7500", "0", "", "", "",
    )
    zaim_row_data_02 = ZaimRowData(
        "2020-12-01", "payment", "通信", "宅急便", "ヨドバシゴールドポイントカード・プラス", "",
        "（配送料・手数料）", "",  # noqa: RUF001
        "Amazon Japan G.K.", "", "0", "410", "0", "", "", "",
    )
    zaim_row_data_03 = ZaimRowData(
        "2020-12-01", "payment", "通信", "その他", "ヨドバシゴールドポイントカード・プラス", "",
        "（割引）", "",  # noqa: RUF001
        "Amazon Japan G.K.", "", "0", "-410", "0", "", "", "",
    )
    # fmt: on
    return [
        zaim_row_data_01,
        zaim_row_data_02,
        zaim_row_data_03,
    ]


def create_zaim_row_data_view_card_202005() -> list[ZaimRowData]:
    """Creates expected zaim row data for VIEW CARD 202005."""
    # fmt: off
    zaim_row_data_view_card_01 = ZaimRowData(
        "2020-03-31", "payment", "通信", "その他", "ビューカード", "", "", "",
        "ビューカード　ビューカードセンター", "", "0",
        "524", "0", "", "", "",
    )
    # fmt: on
    return [zaim_row_data_view_card_01]


def create_zaim_row_data_suica_202003() -> list[ZaimRowData]:
    """Creates expected zaim row data for Suica 202003."""
    # fmt: off
    zaim_row_suica_20200301 = ZaimRowData(
        "2020-03-21", "payment", "交通", "電車", "Suica", "", "", "JR東 越谷レイクタウン → JR東 板橋", "板橋", "", "0",
        "473", "0", "", "", "",
    )
    zaim_row_suica_20200302 = ZaimRowData(
        "2020-03-21", "payment", "交通", "電車", "Suica", "", "",
        "JR東 板橋 → JR東 越谷レイクタウン", "越谷レイクタウン",
        "", "0", "473", "0", "", "", "",
    )
    zaim_row_suica_20200303 = ZaimRowData(
        "2020-03-21", "transfer", "-", "-", "ビューカード", "Suica", "", "", "", "", "0", "0", "3000", "", "", "",
    )
    # fmt: on
    return [zaim_row_suica_20200301, zaim_row_suica_20200302, zaim_row_suica_20200303]


def create_zaim_row_data_pay_pal_201810() -> list[ZaimRowData]:
    """Creates expected zaim row data for PayPal 201810."""
    # fmt: off
    zaim_row_data_01 = ZaimRowData(
        "2018-10-11", "payment", "教育・教養", "参考書", "ヨドバシゴールドポイントカード・プラス", "",
        "プロダクティブ・プログラマ", "", "PayPal", "", "0", "2246", "0", "", "", "",
    )
    zaim_row_data_02 = ZaimRowData(
        "2018-10-11", "payment", "教育・教養", "参考書", "ヨドバシゴールドポイントカード・プラス", "",
        "プログラマが知るべき97のこと", "", "PayPal", "", "0", "1642", "0", "", "", "",
    )
    zaim_row_data_03 = ZaimRowData(
        "2018-10-22", "payment", "教育・教養", "参考書", "ヨドバシゴールドポイントカード・プラス", "",
        "退屈なことはPythonにやらせよう", "", "PayPal", "", "0", "3197", "0", "", "", "",
    )
    # fmt: on
    return [zaim_row_data_01, zaim_row_data_02, zaim_row_data_03]


def create_zaim_row_data_sbi_sumishin_net_bank_202201() -> list[ZaimRowData]:
    """Creates expected zaim row data for SBI Sumishin net bank 202201."""
    # fmt: off
    zaim_row_data_01 = ZaimRowData(
        "2022-01-16", "income", "その他", "-", "", "住信 SBI ネット銀行", "", "",
        "住信 SBI ネット銀行", "", "1", "0", "0", "", "", "",
    )
    zaim_row_data_02 = ZaimRowData(
        "2022-01-05", "transfer", "-", "-", "住信 SBI ネット銀行", "SBI 証券",
        "", "", "", "", "0", "0", "10000", "", "", "",
    )
    zaim_row_data_03 = ZaimRowData(
        "2021-12-30", "transfer", "-", "-", "お財布", "住信 SBI ネット銀行",
        "", "", "", "", "0", "0", "200000", "", "", "",
    )
    # fmt: on
    return [zaim_row_data_01, zaim_row_data_02, zaim_row_data_03]


def create_zaim_row_data_pay_pay_card_202208() -> list[ZaimRowData]:
    """Creates expected zaim row data for PayPay Card 202208."""
    # fmt: off
    zaim_row_data_01 = ZaimRowData(
        "2022-07-29", "transfer", "-", "-", "PayPay カード", "PayPay", "", "",
        "", "", "0", "0", "3000", "", "", "",
    )
    zaim_row_data_02 = ZaimRowData(
        "2022-07-03", "payment", "食費", "食料品", "PayPay カード", "", "", "",
        "ビッグ・エー", "", "0", "292", "0", "", "", "",
    )
    # fmt: on
    return [zaim_row_data_01, zaim_row_data_02]


def create_zaim_row_data_mobile_suica_202210() -> list[ZaimRowData]:
    """Creates expected zaim row data for Mobile Suica 202210."""
    # fmt: off
    zaim_row_data_01 = ZaimRowData(
        "2022-10-28", "transfer", "-", "-", "ビューカード", "Suica", "", "", "", "", "0", "0", "10000", "", "", "",
    )
    zaim_row_data_02 = ZaimRowData(
        "2022-10-28", "payment", "交通", "電車", "Suica", "", "",
        "板橋 → 恵比寿", "恵比寿", "", "0", "220", "0", "", "", "",
    )
    zaim_row_data_03 = ZaimRowData(
        "2022-10-23", "transfer", "-", "-", "ビューカード", "Suica", "", "", "", "", "0", "0", "1000", "", "", "",
    )
    # fmt: on
    return [zaim_row_data_01, zaim_row_data_02, zaim_row_data_03]


def create_zaim_row_data_mobile_suica_202211() -> list[ZaimRowData]:
    """Creates expected zaim row data for Mobile Suica 202211."""
    # fmt: off
    zaim_row_data_01 = ZaimRowData(
        "2022-11-03", "payment", "", "", "Suica", "", "", "", "", "", "0", "-1019", "0", "", "", "",
    )
    # fmt: on
    return [zaim_row_data_01]


def create_zaim_row_data_mobile_suica_202212() -> list[ZaimRowData]:
    """Creates expected zaim row data for Mobile Suica 202212."""
    # fmt: off
    zaim_row_data_01 = ZaimRowData(
        "2022-12-25", "payment", "交通", "電車", "Suica", "",
        "", "地日比谷 → 地東銀座", "東京地下鉄株式会社　日比谷線東銀座駅", "", "0", "46", "0", "", "", "",
    )
    # fmt: on
    return [zaim_row_data_01]


def create_zaim_row_data_mobile_suica_202301() -> list[ZaimRowData]:
    """Creates expected zaim row data for Mobile Suica 202212."""
    # fmt: off
    zaim_row_data_01 = ZaimRowData(
        "2023-01-29", "payment", "交通", "バス", "Suica", "",
        "", "", "都営バス", "", "0", "210", "0", "", "", "",
    )
    # fmt: on
    return [zaim_row_data_01]
