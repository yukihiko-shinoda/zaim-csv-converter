"""The account context that provides the necessary configuration for converting CSV files to Zaim rows."""

from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from typing import TYPE_CHECKING
from typing import Generic

from godslayer import GodSlayerFactory

from zaimcsvconverter.inputtooutput.datasources.csvfile.data import TypeVarInputRowData
from zaimcsvconverter.inputtooutput.datasources.csvfile.records import TypeVarInputRow

if TYPE_CHECKING:
    from zaimcsvconverter.inputtooutput.converters.recordtozaim import CsvRecordToZaimRowConverterFactory
    from zaimcsvconverter.inputtooutput.datasources.csvfile.converters import InputRowFactory


@dataclass
# pylint: disable=too-many-instance-attributes
class AccountContext(Generic[TypeVarInputRowData, TypeVarInputRow]):
    """This class implements recipe for converting steps for WAON CSV."""

    # pylint: disable=invalid-name
    # fmt: off
    GOD_SLAYER_FACTORY_SF_CARD_VIEWER: GodSlayerFactory = field(
        default=GodSlayerFactory(
            header=["利用年月日", "定期", "鉄道会社名", "入場駅/事業者名", "定期", "鉄道会社名", "出場駅/降車場所", "利用額(円)", "残額(円)", "メモ"],  # pylint: disable=line-too-long
            encoding="shift_jis_2004",
        ),
        init=False,
    )
    # pylint: disable=invalid-name
    GOD_SLAYER_FACTORY_AMAZON: GodSlayerFactory = field(
        default=GodSlayerFactory(
            header=[
                "注文日", "注文番号", "商品名", "付帯情報", "価格", "個数", "商品小計", "注文合計", "お届け先", "状態", "請求先", "請求額", "クレカ請求日",  # pylint: disable=line-too-long
                "クレカ請求額", "クレカ種類", "注文概要URL", "領収書URL", "商品URL",
            ],
            partition=[
                r"\d{4}/\d{1,2}/\d{1,2}", r".*", "（注文全体）", "", "", "", "", r"\d*", "", "", r".*", r"\d*", "", "",  # noqa: RUF001,RUF100 pylint: disable=line-too-long
                r".*", r".*", r".*", "",
            ],
            encoding="utf-8-sig",
        ),
        init=False,
    )
    # fmt: on
    regex_csv_file_name: str
    god_slayer_factory: GodSlayerFactory
    input_row_data_class: type[TypeVarInputRowData]
    input_row_factory: InputRowFactory[TypeVarInputRowData, TypeVarInputRow]
    zaim_row_converter_factory: CsvRecordToZaimRowConverterFactory[TypeVarInputRow, TypeVarInputRowData]
