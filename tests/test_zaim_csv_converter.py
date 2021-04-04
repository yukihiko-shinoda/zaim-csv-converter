"""Tests for zaim_csv_converter.py"""
import csv
from pathlib import Path
from typing import Optional

import pytest
from fixturefilehandler.file_paths import RelativeDeployFilePath

from tests.testlibraries.instance_resource import InstanceResource
from tests.testlibraries.output_csv_file_checker import ErrorCsvFileChecker, ZaimCsvFileChecker
from tests.testlibraries.row_data import InvalidRowErrorRowData, ZaimRowData
from zaimcsvconverter.exceptions import InvalidInputCsvError
from zaimcsvconverter.zaim_csv_converter import ZaimCsvConverter


def create_relative_deploy_file_path(
    resource_path, directory_name: str, directory_name_resource: Optional[str] = None
) -> RelativeDeployFilePath:
    """This  function creates relative path aggregate instance to deploy."""
    if directory_name_resource is None:
        directory_name_resource = directory_name
    return RelativeDeployFilePath(
        target=Path(directory_name),
        backup=Path(f"{directory_name}_bak"),
        resource=resource_path.parent / Path(directory_name_resource),
        base=InstanceResource.PATH_PROJECT_HOME_DIRECTORY,
    )


class TestZaimCsvConverter:
    """Tests for ZaimCsvConverter."""

    # pylint: disable=too-many-arguments,too-many-locals,unused-argument
    @staticmethod
    def test_success(
        yaml_config_file, directory_csv_convert_table, directory_csv_input, directory_csv_output, database_session
    ):
        """Input CSV files should be converted into Zaim format CSV file."""
        try:
            ZaimCsvConverter.execute()
        except InvalidInputCsvError as error:
            if (directory_csv_output.target / "error_undefined_content.csv").exists():
                TestZaimCsvConverter.debug_csv("error_undefined_content.csv", directory_csv_output)
            TestZaimCsvConverter.debug_csv("error_invalid_row.csv", directory_csv_output)
            raise error
        files = sorted(directory_csv_output.target.rglob("*[!.gitkeep]"))

        assert len(files) == 17
        checker = ZaimCsvFileChecker(directory_csv_output)
        checker.assert_file(
            "waon201807.csv",
            [
                ZaimRowData(
                    "2018-08-07",
                    "payment",
                    "食費",
                    "食料品",
                    "WAON",
                    "",
                    "",
                    "",
                    "ファミリーマート　かぶと町永代通り店",
                    "",
                    "0",
                    "129",
                    "0",
                    "",
                    "",
                    "",
                ),
            ],
        )
        checker.assert_file(
            "waon201808.csv",
            [
                ZaimRowData(
                    "2018-08-30",
                    "payment",
                    "食費",
                    "食料品",
                    "WAON",
                    "",
                    "",
                    "",
                    "イオンスタイル　板橋前野町",
                    "",
                    "0",
                    "1489",
                    "0",
                    "",
                    "",
                    "",
                ),
            ],
        )
        checker.assert_file(
            "waon201810.csv",
            [
                ZaimRowData(
                    "2018-10-22",
                    "income",
                    "その他",
                    "-",
                    "",
                    "WAON",
                    "",
                    "",
                    "イオンスタイル　板橋前野町",
                    "",
                    "1504",
                    "0",
                    "0",
                    "",
                    "",
                    "",
                ),
                ZaimRowData(
                    "2018-10-22", "transfer", "-", "-", "イオン銀行", "WAON", "", "", "", "", "0", "0", "10000", "", "", ""
                ),
            ],
        )
        checker.assert_file(
            "waon201811.csv",
            [
                ZaimRowData(
                    "2018-11-11", "transfer", "-", "-", "イオン銀行", "WAON", "", "", "", "", "0", "0", "5000", "", "", ""
                ),
                ZaimRowData(
                    "2018-11-23",
                    "payment",
                    "食費",
                    "食料品",
                    "WAON",
                    "",
                    "",
                    "",
                    "カルディコーヒーファーム成増店",
                    "",
                    "0",
                    "-2098",
                    "0",
                    "",
                    "",
                    "",
                ),
            ],
        )
        checker.assert_file(
            "gold_point_card_plus201807.csv",
            [
                ZaimRowData(
                    "2018-07-03",
                    "payment",
                    "水道・光熱",
                    "電気料金",
                    "ヨドバシゴールドポイントカード・プラス",
                    "",
                    "",
                    "",
                    "東京電力エナジーパートナー株式会社",
                    "",
                    "0",
                    "11402",
                    "0",
                    "",
                    "",
                    "",
                ),
            ],
        )
        checker.assert_file(
            "gold_point_card_plus_201912_202007.csv",
            [
                ZaimRowData(
                    "2020-07-03",
                    "payment",
                    "水道・光熱",
                    "電気料金",
                    "ヨドバシゴールドポイントカード・プラス",
                    "",
                    "",
                    "",
                    "東京電力エナジーパートナー株式会社",
                    "",
                    "0",
                    "11402",
                    "0",
                    "",
                    "",
                    "",
                ),
                ZaimRowData(
                    "2020-07-03",
                    "payment",
                    "通信",
                    "インターネット関連費",
                    "ヨドバシゴールドポイントカード・プラス",
                    "",
                    "",
                    "",
                    "Amazon Web Services Japan K.K.",
                    "",
                    "0",
                    "66",
                    "0",
                    "",
                    "",
                    "",
                ),
            ],
        )
        checker.assert_file(
            "mufg201808.csv",
            [
                ZaimRowData(
                    "2018-08-20", "income", "その他", "-", "", "三菱UFJ銀行", "", "", "三菱UFJ銀行", "", "20", "0", "0", "", "", ""
                ),
            ],
        )
        checker.assert_file(
            "mufg201810.csv",
            [
                ZaimRowData(
                    "2018-10-01", "transfer", "-", "-", "お財布", "三菱UFJ銀行", "", "", "", "", "0", "0", "10000", "", "", ""
                ),
                ZaimRowData(
                    "2018-10-01",
                    "income",
                    "臨時収入",
                    "-",
                    "",
                    "三菱UFJ銀行",
                    "",
                    "",
                    "フリコミモト－アカウント",
                    "",
                    "10000",
                    "0",
                    "0",
                    "",
                    "",
                    "",
                ),
                ZaimRowData(
                    "2018-10-20", "transfer", "-", "-", "お財布", "三菱UFJ銀行", "", "", "", "", "0", "0", "10000", "", "", ""
                ),
                ZaimRowData(
                    "2018-10-29",
                    "transfer",
                    "-",
                    "-",
                    "三菱UFJ銀行",
                    "ゴールドポイントカード・プラス",
                    "",
                    "",
                    "",
                    "",
                    "0",
                    "0",
                    "59260",
                    "",
                    "",
                    "",
                ),
            ],
        )
        checker.assert_file(
            "mufg201811.csv",
            [
                ZaimRowData(
                    "2018-11-28",
                    "payment",
                    "水道・光熱",
                    "水道料金",
                    "三菱UFJ銀行",
                    "",
                    "",
                    "",
                    "東京都水道局　経理部管理課",
                    "",
                    "0",
                    "3628",
                    "0",
                    "",
                    "",
                    "",
                ),
            ],
        )
        checker.assert_file(
            "pasmo201811.csv",
            [
                ZaimRowData(
                    "2018-11-13",
                    "payment",
                    "交通",
                    "電車",
                    "PASMO",
                    "",
                    "",
                    "メトロ 六本木一丁目 → メトロ 後楽園",
                    "東京地下鉄株式会社　南北線後楽園駅",
                    "",
                    "0",
                    "195",
                    "0",
                    "",
                    "",
                    "",
                ),
                ZaimRowData(
                    "2018-11-11",
                    "transfer",
                    "-",
                    "-",
                    "TOKYU CARD",
                    "PASMO",
                    "",
                    "",
                    "",
                    "",
                    "0",
                    "0",
                    "3000",
                    "",
                    "",
                    "",
                ),
            ],
        )
        checker.assert_file(
            "pasmo201901.csv",
            [
                ZaimRowData(
                    "2019-01-27", "payment", "交通", "バス", "PASMO", "", "", "", "", "", "0", "195", "0", "", "", ""
                ),
            ],
        )
        checker.assert_file(
            "amazon201810.csv",
            [
                ZaimRowData(
                    "2018-10-23",
                    "payment",
                    "大型出費",
                    "家電",
                    "ヨドバシゴールドポイントカード・プラス",
                    "",
                    "Echo Dot (エコードット) 第2世代 - スマートスピーカー with Alexa、ホワイト",
                    "",
                    "Amazon Japan G.K.",
                    "",
                    "0",
                    "4980",
                    "0",
                    "",
                    "",
                    "",
                ),
            ],
        )
        checker.assert_file(
            "amazon_201911_201911.csv",
            [
                ZaimRowData(
                    "2019-11-09",
                    "payment",
                    "教育・教養",
                    "参考書",
                    "ヨドバシゴールドポイントカード・プラス",
                    "",
                    "［第2版］Python機械学習プログラミング 達人データサイエンティストによる理論と実践 impress top gearシリーズ",
                    "",
                    "Amazon Japan G.K.",
                    "",
                    "0",
                    "4000",
                    "0",
                    "",
                    "",
                    "",
                ),
                ZaimRowData(
                    "2019-11-09",
                    "payment",
                    "通信",
                    "その他",
                    "ヨドバシゴールドポイントカード・プラス",
                    "",
                    "（Amazon ポイント）",
                    "",
                    "Amazon Japan G.K.",
                    "",
                    "0",
                    "-11",
                    "0",
                    "",
                    "",
                    "",
                ),
            ],
        )
        checker.assert_file(
            "amazon_201911_202004.csv",
            [
                ZaimRowData(
                    "2020-04-25",
                    "payment",
                    "大型出費",
                    "家電",
                    "ヨドバシゴールドポイントカード・プラス",
                    "",
                    "【日本正規代理店品】 Drobo 5N2 NASケース(3.5インチ×5bay) ギガビットイーサネット×2 PDR-5N2",
                    "",
                    "Amazon Japan G.K.",
                    "",
                    "0",
                    "79482",
                    "0",
                    "",
                    "",
                    "",
                ),
                ZaimRowData(
                    "2020-04-25",
                    "payment",
                    "通信",
                    "宅急便",
                    "ヨドバシゴールドポイントカード・プラス",
                    "",
                    "（配送料・手数料）",
                    "",
                    "Amazon Japan G.K.",
                    "",
                    "0",
                    "410",
                    "0",
                    "",
                    "",
                    "",
                ),
                ZaimRowData(
                    "2020-04-25",
                    "payment",
                    "通信",
                    "その他",
                    "ヨドバシゴールドポイントカード・プラス",
                    "",
                    "（割引）",
                    "",
                    "Amazon Japan G.K.",
                    "",
                    "0",
                    "-410",
                    "0",
                    "",
                    "",
                    "",
                ),
                ZaimRowData(
                    "2020-04-25",
                    "payment",
                    "通信",
                    "その他",
                    "ヨドバシゴールドポイントカード・プラス",
                    "",
                    "（Amazonポイント）",
                    "",
                    "Amazon Japan G.K.",
                    "",
                    "0",
                    "-60",
                    "0",
                    "",
                    "",
                    "",
                ),
            ],
        )
        checker.assert_file(
            "view_card202005.csv",
            [
                ZaimRowData(
                    "2020-03-31",
                    "payment",
                    "通信",
                    "その他",
                    "ビューカード",
                    "",
                    "",
                    "",
                    "ビューカード　ビューカードセンター",
                    "",
                    "0",
                    "524",
                    "0",
                    "",
                    "",
                    "",
                ),
            ],
        )
        checker.assert_file(
            "suica202003.csv",
            [
                ZaimRowData(
                    "2020-03-21",
                    "payment",
                    "交通",
                    "電車",
                    "Suica",
                    "",
                    "",
                    "JR東 越谷レイクタウン → JR東 板橋",
                    "板橋",
                    "",
                    "0",
                    "473",
                    "0",
                    "",
                    "",
                    "",
                ),
                ZaimRowData(
                    "2020-03-21",
                    "payment",
                    "交通",
                    "電車",
                    "Suica",
                    "",
                    "",
                    "JR東 板橋 → JR東 越谷レイクタウン",
                    "越谷レイクタウン",
                    "",
                    "0",
                    "473",
                    "0",
                    "",
                    "",
                    "",
                ),
                ZaimRowData(
                    "2020-03-21", "transfer", "-", "-", "ビューカード", "Suica", "", "", "", "", "0", "0", "3000", "", "", ""
                ),
            ],
        )
        checker.assert_file(
            "pay_pal201810.csv",
            [
                ZaimRowData(
                    "2018-10-11",
                    "payment",
                    "教育・教養",
                    "参考書",
                    "ヨドバシゴールドポイントカード・プラス",
                    "",
                    "プロダクティブ・プログラマ",
                    "",
                    "PayPal",
                    "",
                    "0",
                    "2246",
                    "0",
                    "",
                    "",
                    "",
                ),
                ZaimRowData(
                    "2018-10-11",
                    "payment",
                    "教育・教養",
                    "参考書",
                    "ヨドバシゴールドポイントカード・プラス",
                    "",
                    "プログラマが知るべき97のこと",
                    "",
                    "PayPal",
                    "",
                    "0",
                    "1642",
                    "0",
                    "",
                    "",
                    "",
                ),
                ZaimRowData(
                    "2018-10-22",
                    "payment",
                    "教育・教養",
                    "参考書",
                    "ヨドバシゴールドポイントカード・プラス",
                    "",
                    "退屈なことはPythonにやらせよう",
                    "",
                    "PayPal",
                    "",
                    "0",
                    "3197",
                    "0",
                    "",
                    "",
                    "",
                ),
            ],
        )

    @staticmethod
    def debug_csv(csv_file_name, directory_csv_output):
        with (directory_csv_output.target / csv_file_name).open("r", encoding="UTF-8", newline="\n") as file:
            csv_reader = csv.reader(file)
            for list_row_data in csv_reader:
                print(list_row_data)

    # pylint: disable=unused-argument
    @staticmethod
    def test_fail(
        yaml_config_file, directory_csv_convert_table, directory_csv_input, directory_csv_output, database_session
    ):
        """
        Correct input CSV files should be converted into Zaim format CSV file.
        Incorrect input CSV files should be reported on error_undefined_content.csv.
        """
        with pytest.raises(InvalidInputCsvError) as error:
            ZaimCsvConverter.execute()
        assert str(error.value) == "Some invalid input CSV file exists. Please check error_invalid_row.csv."
        checker = ZaimCsvFileChecker(directory_csv_output)
        checker.assert_file(
            "waon201808.csv",
            [
                ZaimRowData(
                    "2018-08-30",
                    "payment",
                    "食費",
                    "食料品",
                    "WAON",
                    "",
                    "",
                    "",
                    "イオンスタイル　板橋前野町",
                    "",
                    "0",
                    "1489",
                    "0",
                    "",
                    "",
                    "",
                ),
            ],
        )
        checker.assert_file(
            "amazon201810.csv",
            [
                ZaimRowData(
                    "2018-10-23",
                    "payment",
                    "大型出費",
                    "家電",
                    "ヨドバシゴールドポイントカード・プラス",
                    "",
                    "Echo Dot (エコードット) 第2世代 - スマートスピーカー with Alexa、ホワイト",
                    "",
                    "Amazon Japan G.K.",
                    "",
                    "0",
                    "4980",
                    "0",
                    "",
                    "",
                    "",
                ),
            ],
        )
        checker = ErrorCsvFileChecker(directory_csv_output)
        checker.assert_file(
            "error_invalid_row.csv",
            [
                InvalidRowErrorRowData(
                    "gold_point_card_plus_201912_202008.csv",
                    "",
                    "gold_point_card_plus_201912_202008.csv does not contain Footer row. "
                    "Confirm CSV file and footer again. "
                    "Footer = ['^$', '^$', '^$', '^$', '^$', '^\\\\d*$', '^$']",
                ),
                InvalidRowErrorRowData(
                    "mufg201810.csv",
                    "",
                    (
                        "CSV file does not contain header row.Confirm CSV file and header again. "
                        "Header = "
                        "['日付', '摘要', '摘要内容', '支払い金額', '預かり金額', '差引残高', 'メモ', '未資金化区分', '入払区分']"
                    ),
                ),
                InvalidRowErrorRowData(
                    "waon201808.csv",
                    "1",
                    'The value of "Charge kind" has not been defined in this code. Charge kind = クレジットカード',
                ),
            ],
        )
