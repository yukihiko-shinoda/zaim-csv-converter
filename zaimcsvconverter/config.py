"""This module implements configuration."""
from __future__ import annotations

from dataclasses import dataclass, field

from dataclasses_json import DataClassJsonMixin
from yamldataclassconfig.config import YamlDataClassConfig


@dataclass
class WaonConfig(DataClassJsonMixin):
    """This class implements configuration for WAON."""

    account_name: str
    auto_charge_source: str


@dataclass
class GoldPointCardPlusConfig(DataClassJsonMixin):
    """This class implements configuration for GOLD POINT CARD+."""

    account_name: str
    skip_amazon_row: bool
    skip_pay_pal_row: bool
    skip_kyash_row: bool


@dataclass
class MufgConfig(DataClassJsonMixin):
    """This class implements configuration for MUFG bank."""

    account_name: str
    transfer_account_name: str


@dataclass
class SFCardViewerConfig(DataClassJsonMixin):
    """This class implements configuration for SF Card Viewer."""

    account_name: str
    auto_charge_source: str
    skip_sales_goods_row: bool


@dataclass
class PasmoConfig(SFCardViewerConfig):
    """This class implements configuration for PASMO."""


@dataclass
class AmazonConfig(DataClassJsonMixin):
    """This class implements configuration for Amazon.co.jp."""

    store_name_zaim: str
    payment_account_name: str


@dataclass
class ViewCardConfig(DataClassJsonMixin):
    """This class implements configuration for View Card."""

    account_name: str
    skip_suica_row: bool


@dataclass
class SuicaConfig(SFCardViewerConfig):
    """This class implements configuration for PASMO."""


@dataclass
class PayPalConfig(DataClassJsonMixin):
    """This class implements configuration for PayPal."""

    store_name_zaim: str
    payment_account_name: str


@dataclass
class SBISumishinNetBankConfig(DataClassJsonMixin):
    """This class implements configuration for SBI Sumishin Net Bank."""

    account_name: str
    transfer_account_name: str


@dataclass
class PayPayCardConfig(DataClassJsonMixin):
    """This class implements configuration for PayPay Card."""

    account_name: str


@dataclass
# Reason: Specification. pylint: disable=too-many-instance-attributes
class Config(YamlDataClassConfig):
    """This class implements configuration wrapping."""

    waon: WaonConfig = field(default=None, metadata={"dataclasses_json": {"mm_field": WaonConfig}})  # type: ignore
    gold_point_card_plus: GoldPointCardPlusConfig = field(  # type: ignore
        default=None,
        metadata={"dataclasses_json": {"mm_field": GoldPointCardPlusConfig}},
    )
    mufg: MufgConfig = field(default=None, metadata={"dataclasses_json": {"mm_field": MufgConfig}})  # type: ignore
    pasmo: PasmoConfig = field(default=None, metadata={"dataclasses_json": {"mm_field": PasmoConfig}})  # type: ignore
    amazon: AmazonConfig = field(  # type: ignore
        default=None,
        metadata={"dataclasses_json": {"mm_field": AmazonConfig}},
    )
    view_card: ViewCardConfig = field(  # type: ignore
        default=None,
        metadata={"dataclasses_json": {"mm_field": ViewCardConfig}},
    )
    suica: PasmoConfig = field(default=None, metadata={"dataclasses_json": {"mm_field": SuicaConfig}})  # type: ignore
    pay_pal: PayPalConfig = field(  # type: ignore
        default=None,
        metadata={"dataclasses_json": {"mm_field": PayPalConfig}},
    )
    sbi_sumishin_net_bank: SBISumishinNetBankConfig = field(  # type: ignore
        default=None,
        metadata={"dataclasses_json": {"mm_field": SBISumishinNetBankConfig}},
    )
    pay_pay_card: PayPayCardConfig = field(  # type: ignore
        default=None,
        metadata={"dataclasses_json": {"mm_field": PayPayCardConfig}},
    )
