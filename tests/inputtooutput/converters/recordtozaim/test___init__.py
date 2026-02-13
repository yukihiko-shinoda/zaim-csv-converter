"""Tests for __init__.py."""

import pytest

from tests.conftest import create_zaim_row_converter
from tests.testlibraries.instance_resource import InstanceResource
from zaimcsvconverter.accounts.enum import Account
from zaimcsvconverter.inputtooutput.converters.recordtozaim import ZaimPaymentRowConverter
from zaimcsvconverter.inputtooutput.converters.recordtozaim.amazon import AmazonZaimPaymentRowConverter
from zaimcsvconverter.inputtooutput.converters.recordtozaim.amazon_201911 import (
    Amazon201911DiscountZaimPaymentRowConverter,  # noqa: H301
)
from zaimcsvconverter.inputtooutput.converters.recordtozaim.amazon_201911 import (
    Amazon201911PaymentZaimPaymentRowConverter,  # noqa: H301
)
from zaimcsvconverter.inputtooutput.converters.recordtozaim.gold_point_card_plus import (
    GoldPointCardPlusZaimPaymentRowConverter,  # noqa: H301
)
from zaimcsvconverter.inputtooutput.converters.recordtozaim.gold_point_card_plus_201912 import (
    GoldPointCardPlus201912ZaimPaymentRowConverter,  # noqa: H301
)
from zaimcsvconverter.inputtooutput.converters.recordtozaim.gold_point_card_plus_201912 import (
    GoldPointCardPlus201912ZaimTransferRowConverter,  # noqa: H301
)
from zaimcsvconverter.inputtooutput.converters.recordtozaim.mufg import MufgIncomeZaimTransferRowConverter
from zaimcsvconverter.inputtooutput.converters.recordtozaim.mufg import MufgPaymentZaimTransferRowConverter
from zaimcsvconverter.inputtooutput.converters.recordtozaim.mufg import MufgTransferIncomeZaimTransferRowConverter
from zaimcsvconverter.inputtooutput.converters.recordtozaim.mufg import MufgTransferPaymentZaimTransferRowConverter
from zaimcsvconverter.inputtooutput.converters.recordtozaim.mufg import MufgZaimIncomeRowConverter
from zaimcsvconverter.inputtooutput.converters.recordtozaim.mufg import MufgZaimPaymentRowConverter
from zaimcsvconverter.inputtooutput.converters.recordtozaim.sf_card_viewer import (
    SFCardViewerZaimPaymentOnSomewhereRowConverter,  # noqa: H301
)
from zaimcsvconverter.inputtooutput.converters.recordtozaim.sf_card_viewer import (
    SFCardViewerZaimPaymentOnStationRowConverter,  # noqa: H301
)
from zaimcsvconverter.inputtooutput.converters.recordtozaim.sf_card_viewer import SFCardViewerZaimTransferRowConverter
from zaimcsvconverter.inputtooutput.converters.recordtozaim.view_card import ViewCardZaimPaymentRowConverter
from zaimcsvconverter.inputtooutput.converters.recordtozaim.waon import WaonZaimIncomeRowConverter
from zaimcsvconverter.inputtooutput.converters.recordtozaim.waon import WaonZaimPaymentRowConverter
from zaimcsvconverter.inputtooutput.converters.recordtozaim.waon import WaonZaimTransferRowConverter
from zaimcsvconverter.inputtooutput.datasources.csvfile.data import InputRowData
from zaimcsvconverter.inputtooutput.datasources.csvfile.records import InputRow


class TestZaimRowConverterFactory:
    """Tests for ZaimRowConverterFactory."""

    # pylint: disable=unused-argument
    @staticmethod
    @pytest.mark.parametrize(
        ("database_session_with_schema", "account", "input_row_data", "expected"),
        [
            # Case when WAON payment
            (
                [InstanceResource.FIXTURE_RECORD_STORE_WAON_FAMILY_MART_KABUTOCHOEITAIDORI],
                Account.WAON,
                InstanceResource.ROW_DATA_WAON_PAYMENT_FAMILY_MART_KABUTOCHOEIDAIDORI,
                WaonZaimPaymentRowConverter,
            ),
            # Case when WAON charge from point
            (
                [InstanceResource.FIXTURE_RECORD_STORE_WAON_ITABASHIMAENOCHO],
                Account.WAON,
                InstanceResource.ROW_DATA_WAON_CHARGE_POINT_ITABASHIMAENOCHO,
                WaonZaimIncomeRowConverter,
            ),
            # Case when WAON charge from bank account
            (
                [InstanceResource.FIXTURE_RECORD_STORE_WAON_ITABASHIMAENOCHO],
                Account.WAON,
                InstanceResource.ROW_DATA_WAON_CHARGE_BANK_ACCOUNT_ITABASHIMAENOCHO,
                WaonZaimTransferRowConverter,
            ),
            # Case when WAON auto charge
            (
                [InstanceResource.FIXTURE_RECORD_STORE_WAON_ITABASHIMAENOCHO],
                Account.WAON,
                InstanceResource.ROW_DATA_WAON_AUTO_CHARGE_ITABASHIMAENOCHO,
                WaonZaimTransferRowConverter,
            ),
            # Case when WAON charge by cash
            (
                [InstanceResource.FIXTURE_RECORD_STORE_WAON_ITABASHIMAENOCHO],
                Account.WAON,
                InstanceResource.ROW_DATA_WAON_CHARGE_CASH_ITABASHIMAENOCHO,
                WaonZaimTransferRowConverter,
            ),
            # Case when WAON charge by value download
            (
                [InstanceResource.FIXTURE_RECORD_STORE_WAON_ITABASHIMAENOCHO],
                Account.WAON,
                InstanceResource.ROW_DATA_WAON_CHARGE_DOWNLOAD_VALUE_ITABASHIMAENOCHO,
                WaonZaimIncomeRowConverter,
            ),
            # Case when Gold Point Card Plus payment
            (
                [InstanceResource.FIXTURE_RECORD_STORE_GOLD_POINT_CARD_PLUS_AMAZON_CO_JP],
                Account.GOLD_POINT_CARD_PLUS,
                InstanceResource.ROW_DATA_GOLD_POINT_CARD_PLUS_AMAZON_CO_JP,
                GoldPointCardPlusZaimPaymentRowConverter,
            ),
            # Case when Gold Point Card Plus payment
            (
                [InstanceResource.FIXTURE_RECORD_STORE_GOLD_POINT_CARD_PLUS_AMAZON_DOWNLOADS],
                Account.GOLD_POINT_CARD_PLUS_201912,
                InstanceResource.ROW_DATA_GOLD_POINT_CARD_PLUS_201912_AMAZON_DOWNLOADS,
                GoldPointCardPlus201912ZaimPaymentRowConverter,
            ),
            # Case when Gold Point Card Plus transfer
            (
                [InstanceResource.FIXTURE_RECORD_STORE_GOLD_POINT_CARD_PLUS_KYASH],
                Account.GOLD_POINT_CARD_PLUS_201912,
                InstanceResource.ROW_DATA_GOLD_POINT_CARD_PLUS_201912_KYASH,
                GoldPointCardPlus201912ZaimTransferRowConverter,
            ),
            # Case when MUFG income by card
            (
                [InstanceResource.FIXTURE_RECORD_STORE_MUFG_EMPTY],
                Account.MUFG,
                InstanceResource.ROW_DATA_MUFG_INCOME_CARD,
                MufgIncomeZaimTransferRowConverter,
            ),
            # Case when MUFG income not by card
            (
                [InstanceResource.FIXTURE_RECORD_STORE_MUFG_OTHER_ACCOUNT],
                Account.MUFG,
                InstanceResource.ROW_DATA_MUFG_INCOME_NOT_CARD,
                MufgZaimIncomeRowConverter,
            ),
            # Case when MUFG payment
            (
                [InstanceResource.FIXTURE_RECORD_STORE_MUFG_EMPTY],
                Account.MUFG,
                InstanceResource.ROW_DATA_MUFG_PAYMENT,
                MufgPaymentZaimTransferRowConverter,
            ),
            # Case when MUFG transfer income which transfer_target doesn't exist
            (
                [InstanceResource.FIXTURE_RECORD_STORE_MUFG_MUFG],
                Account.MUFG,
                InstanceResource.ROW_DATA_MUFG_TRANSFER_INCOME_NOT_OWN_ACCOUNT,
                MufgZaimIncomeRowConverter,
            ),
            # Case when MUFG transfer income which transfer_target exists
            (
                [InstanceResource.FIXTURE_RECORD_STORE_MUFG_MUFG_TRUST_AND_BANK],
                Account.MUFG,
                InstanceResource.ROW_DATA_MUFG_TRANSFER_INCOME_OWN_ACCOUNT,
                MufgTransferIncomeZaimTransferRowConverter,
            ),
            # Case when MUFG transfer payment which transfer_target doesn't exist
            (
                [InstanceResource.FIXTURE_RECORD_STORE_MUFG_TOKYO_WATERWORKS],
                Account.MUFG,
                InstanceResource.ROW_DATA_MUFG_TRANSFER_PAYMENT_TOKYO_WATERWORKS,
                MufgZaimPaymentRowConverter,
            ),
            # Case when MUFG transfer payment transfer_target exists
            (
                [InstanceResource.FIXTURE_RECORD_STORE_MUFG_GOLD_POINT_MARKETING],
                Account.MUFG,
                InstanceResource.ROW_DATA_MUFG_TRANSFER_PAYMENT_GOLD_POINT_MARKETING,
                MufgTransferPaymentZaimTransferRowConverter,
            ),
            # Case when SF Card Viewer transportation
            (
                [InstanceResource.FIXTURE_RECORD_STORE_PASMO_KOHRAKUEN_STATION],
                Account.PASMO,
                InstanceResource.ROW_DATA_SF_CARD_VIEWER_TRANSPORTATION_KOHRAKUEN_STATION,
                SFCardViewerZaimPaymentOnStationRowConverter,
            ),
            # Case when SF Card Viewer sales goods
            (
                [InstanceResource.FIXTURE_RECORD_STORE_PASMO_EMPTY],
                Account.PASMO,
                InstanceResource.ROW_DATA_SF_CARD_VIEWER_SALES_GOODS,
                SFCardViewerZaimPaymentOnSomewhereRowConverter,
            ),
            # Case when SF Card Viewer auto charge
            (
                [InstanceResource.FIXTURE_RECORD_STORE_PASMO_EMPTY],
                Account.PASMO,
                InstanceResource.ROW_DATA_SF_CARD_VIEWER_AUTO_CHARGE_AKIHABARA_STATION,
                SFCardViewerZaimTransferRowConverter,
            ),
            # Case when SF Card Viewer exit by window
            (
                [InstanceResource.FIXTURE_RECORD_STORE_PASMO_KITASENJU_STATION],
                Account.PASMO,
                InstanceResource.ROW_DATA_SF_CARD_VIEWER_EXIT_BY_WINDOW_KITASENJU_STATION,
                SFCardViewerZaimPaymentOnStationRowConverter,
            ),
            # Case when SF Card Viewer bus tram
            (
                [InstanceResource.FIXTURE_RECORD_STORE_PASMO_EMPTY],
                Account.PASMO,
                InstanceResource.ROW_DATA_SF_CARD_VIEWER_BUS_TRAM,
                SFCardViewerZaimPaymentOnSomewhereRowConverter,
            ),
            # Case when Amazon payment
            (
                [InstanceResource.FIXTURE_RECORD_ITEM_AMAZON_ECHO_DOT],
                Account.AMAZON,
                InstanceResource.ROW_DATA_AMAZON_ECHO_DOT,
                AmazonZaimPaymentRowConverter,
            ),
            # Case when Amazon payment
            (
                [InstanceResource.FIXTURE_RECORD_ITEM_AMAZON_ECHO_DOT],
                Account.AMAZON_201911,
                InstanceResource.ROW_DATA_AMAZON_201911_ECHO_DOT,
                Amazon201911PaymentZaimPaymentRowConverter,
            ),
            # Case when Amazon discount
            (
                [InstanceResource.FIXTURE_RECORD_ITEM_AMAZON_AMAZON_POINT],
                Account.AMAZON_201911,
                InstanceResource.ROW_DATA_AMAZON_201911_AMAZON_POINT,
                Amazon201911DiscountZaimPaymentRowConverter,
            ),
            # Case when Gold Point Card Plus payment
            (
                [InstanceResource.FIXTURE_RECORD_STORE_VIEW_CARD_VIEW_CARD],
                Account.VIEW_CARD,
                InstanceResource.ROW_DATA_VIEW_CARD_ANNUAL_FEE,
                ViewCardZaimPaymentRowConverter,
            ),
        ],
        indirect=["database_session_with_schema"],
    )
    @pytest.mark.usefixtures("_yaml_config_load", "database_session_with_schema")
    def test_select_factory(
        account: Account,
        input_row_data: InputRowData,
        expected: type[ZaimPaymentRowConverter[InputRow[InputRowData], InputRowData]],
    ) -> None:
        """Input row should convert to suitable ZaimRow by transfer target."""
        assert isinstance(create_zaim_row_converter(account.value, input_row_data), expected)
