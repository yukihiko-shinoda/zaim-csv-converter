#!/usr/bin/env python
"""This module implements fixture of instance."""
from zaimcsvconverter.inputcsvformats.amazon import AmazonRowData


class InstanceFixture:
    """This class implements fixture of instance."""
    ROW_DATA_AMAZON = AmazonRowData(
        '2018/10/23', '123-4567890-1234567', 'Echo Dot (エコードット) 第2世代 - スマートスピーカー with Alexa、ホワイト',
        '販売： Amazon Japan G.K.  コンディション： 新品', '4980', '1', '6276', '6390', 'ローソン桜塚',
        '2018年10月23日に発送済み', 'テストアカウント', '5952', '2018/10/23', '5952', 'Visa（下4けたが1234）',
        'https://www.amazon.co.jp/gp/css/summary/edit.html?ie=UTF8&orderID=123-4567890-1234567',
        'https://www.amazon.co.jp/gp/css/summary/print.html/'
        + 'ref=oh_aui_ajax_dpi?ie=UTF8&orderID=123-4567890-1234567',
        'https://www.amazon.co.jp/gp/product/B06ZYTTC4P/ref=od_aui_detailpages01?ie=UTF8&psc=1')
