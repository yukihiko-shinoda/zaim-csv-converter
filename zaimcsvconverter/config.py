"""This module implements configuration."""
from __future__ import annotations

from enum import Enum
from pathlib import Path

from dataclasses import dataclass, field

from dataclasses_json import DataClassJsonMixin
from yamldataclassconfig import create_file_path_field
from yamldataclassconfig.config import YamlDataClassConfig


class AccountKey(Enum):
    """This class implements constant of account key for config.yml."""
    WAON: str = 'waon'
    GOLD_POINT_CARD_PLUS: str = 'gold_point_card_plus'
    MUFG: str = 'mufg'
    PASMO: str = 'pasmo'
    AMAZON: str = 'amazon'


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
class Config(YamlDataClassConfig):
    """This class implements configuration wrapping."""
    waon: WaonConfig = field(  # type: ignore
        default=None,
        metadata={'dataclasses_json': {'mm_field': WaonConfig}}
    )
    gold_point_card_plus: GoldPointCardPlusConfig = field(  # type: ignore
        default=None,
        metadata={'dataclasses_json': {'mm_field': GoldPointCardPlusConfig}}
    )
    mufg: MufgConfig = field(  # type: ignore
        default=None,
        metadata={'dataclasses_json': {'mm_field': MufgConfig}}
    )
    pasmo: PasmoConfig = field(  # type: ignore
        default=None,
        metadata={'dataclasses_json': {'mm_field': PasmoConfig}}
    )
    amazon: AmazonConfig = field(  # type: ignore
        default=None,
        metadata={'dataclasses_json': {'mm_field': AmazonConfig}}
    )
    FILE_PATH: Path = create_file_path_field(Path(__file__).parent.parent / 'config.yml')
