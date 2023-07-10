# 📥Zaim CSV Converter📤

[![Test](https://github.com/yukihiko-shinoda/zaim-csv-converter/workflows/Test/badge.svg)](https://github.com/yukihiko-shinoda/zaim-csv-converter/actions?query=workflow%3ATest)
[![Test Coverage](https://api.codeclimate.com/v1/badges/d420cae61c02b01316ca/test_coverage)](https://codeclimate.com/github/yukihiko-shinoda/zaim-csv-converter/test_coverage)
[![Maintainability](https://api.codeclimate.com/v1/badges/d420cae61c02b01316ca/maintainability)](https://codeclimate.com/github/yukihiko-shinoda/zaim-csv-converter/maintainability)
[![Twitter URL](https://img.shields.io/twitter/url?style=social&url=https%3A%2F%2Fgithub.com%2Fyukihiko-shinoda%2Fzaim-csv-converter)](http://twitter.com/share?text=Zaim%20CSV%20Converter&url=https://github.com/yukihiko-shinoda/zaim-csv-converter&hashtags=python,zaim)

各口座の WEB サイト等で出力できる CSV を
Zaim のフォーマットに変換する Python 製のコンバーターです。

Zaim で口座連携をするために
口座のアカウント情報をクラウドに預けるのが心配な方は
ぜひご利用ください。

現在は以下の口座の CSV に対応しています。

- WAON
- ヨドバシゴールドポイントカード・プラス
- 三菱 UFJ 銀行
- PASMO
- Amazon.co.jp
- ビューカード
- Suica・モバイル Suica
- PayPal (experimental)
- 住信 SBI ネット銀行 (experimental)
- PayPay カード

※ [対応口座追加のための開発手順](docs/CONTRIBUTING.md)をまとめました、プルリクエストをお待ちしています。

## 動作確認環境

Python 3.9.17 以上

## 初回のみ行う利用準備

### 1. プロジェクトをダウンロードします

```console
git clone https://github.com/yukihiko-shinoda/zaim-csv-converter.git
```

### 2. 設定ファイルを準備します

config.yml.dist をコピーして config.yml を作成し、
Zaim の利用状態に合わせて config.yml を編集します。

各項目の意味は config.yml.dist を参照してください。

### 3. 変換用テーブルのCSVを準備します

各口座の WEB サイト等から出力した CSV に含まれるお店の名前を、
Zaim 上で登録しているお店の名前に変換する必要があります。
この、変換前と変換後のお店の名前、デフォルトのカテゴリーを定義する CSV を
 csvconverttable/ ディレクトリー配下に準備します。

CSV の作成方法は[変換用テーブルの CSV のつくり方](#変換用テーブルの-CSV-のつくり方)を参照してください。

各口座毎に、以下のファイル名と形式で準備します。

口座|ファイル名|形式
---|---|---
WAON|waon.csv|お店単位
ヨドバシゴールドポイントカード・プラス|gold_point_card_plus.csv|お店単位
三菱 UFJ 銀行|mufg.csv|お店単位
Suica,PASMO|sf_card_viewer.csv|お店単位
モバイル Suica|mobile_suica.csb|お店単位
Amazon.co.jp|amazon.csv|品目単位
ビューカード|view_card.csv|お店単位
PayPal|pay_pal_store.csv, pay_pal_item.csv|お店単位、品目単位
住信 SBI ネット銀行|sbi_sumishin_net_bank.csv|お店単位
PayPay カード|pay_pay_card.csv|お店単位

※ 文字コードは UTF-8 で準備してください。

### 4. Python プロジェクト実行用の仮想環境を作成します

```console
pipenv install
```

## 利用方法

### 1. 変換対象の CSV を準備します

変換対象の各口座の CSV ファイルを csvinput/ ディレクトリ―配下に配置します。

複数のファイルを一度に処理できます。

各CSVファイルをどの口座のものとして処理するかの判定は
ファイル名に以下の文字列が含まれているかどうかで判定を行います。

口座|ファイル名に含まれるべき文字列
---|---
WAON|waon
ヨドバシゴールドポイントカード・プラス 2019 年 11 月以前の形式|gold_point_card_plus
ヨドバシゴールドポイントカード・プラス 2019 年 12 月～2020 年 8 月時点の形式|gold_point_card_plus_201912
ヨドバシゴールドポイントカード・プラス 2020 年 9 月以降の形式|gold_point_card_plus_202009
三菱 UFJ 銀行|mufg
PASMO|pasmo
Amazon.co.jp 2019 年 11 月以前の形式|amazon
Amazon.co.jp 2019 年 12 月以降の形式|amazon_201911
ビューカード|view_card
Suica|suica
モバイル Suica|mobile_suica + 西暦年を表す半角数字 4 ~ 6 桁 (後述)
PayPal|pay_pal_store, pay_pal_item
住信 SBI ネット銀行|sbi_sumishin_net_bank
PayPay カード|pay_pay_card

変換対象CSVの準備方法の詳細は[変換対象 CSV の準備方法](#変換対象-CSV-の準備方法)を参照してください。

### 2. 実行します

```console
pipenv run start
```

### 3. 実行結果の確認を行います

実行後、
 csvoutput/ に csvinput/ と同名のファイルが作成されます。
 出力された CSV が意図通りになっているか、入力 CSV と出力 CSV を目視で確認することをおすすめします。

ここでエラーメッセージが表示された場合は、
エラーの内容に従い CSV ファイルの確認等を行ってから、再度実行します。

代表的な例として:

```console
InvalidInputCsvError: 'Some invalid input CSV file exists. Please check error_invalid_row.csv and error_undefined_content.csv.'
```

上記のエラーが表示された場合は、
csvoutput/error_invalid_row.csv にエラーの一覧が、
csvoutput/error_undefined_content.csv に
変換用テーブルの CSV に未定義のお店の名前、品目名の一覧が出力されます。
csvoutput/error_invalid_row.csv と入力 CSV の内容を確認して、入力 CSV に修正を行います。
csvoutput/error_undefined_content.csv が出力された場合は、
変換テーブルの CSV に変換の定義を追加します。

### 4. Zaim にインポートします

ブラウザーで [WEB 版の Zaim](https://zaim.net/) にログインし、
画面右上の

[設定] -> [ファイル入出力] -> [Zaim の出力ファイルをアップロード]

から csvoutput/ ディレクトリーに出力された CSV をアップロードします。

### 5. アップロードされた情報を確認します

Zaim側 のアップデートに伴う仕様変更等で、予期しない登録が発生する可能性を考慮し、
Zaim の履歴画面で、 csvoutput/ ディレクトリーの CSV と Zaim 上の登録内容の比較を目視で行います。

また、この段階で、カテゴリが変換用テーブルのCSVで指定したデフォルトのカテゴリと異なる履歴を
Zaim上で修正します。

## 変換用テーブルの CSV のつくり方

### お店単位

左から順に以下の情報を各列に定義していきます。

- 口座の WEB サイト等からダウンロードした CSV に含まれるお店の名前
- Zaim 上で登録しているお店の名前
- このお店での履歴が支出履歴の場合のデフォルトのカテゴリ
- このお店での履歴が支出履歴の場合のデフォルトのカテゴリ内訳
- このお店での履歴が収入履歴の場合のデフォルトのカテゴリ(例えば、WAON のポイントダウンロード等)
- このお店での履歴が振替履歴の場合の振替対象口座名(例えば、銀行口座のクレジット引き落とし等)

例えば、三菱 UFJ 銀行向け mufg.csv の場合：

```csv
,,,,,お財布
トウキヨウガス,東京ガス（株）,水道・光熱,ガス料金,,
ＧＰマーケテイング,,,,,ゴールドポイントカード・プラス
```

### 品目単位

左から順に以下の情報を各列に定義していきます。

- 品目
- デフォルトの支出カテゴリ
- デフォルトの支出カテゴリ内訳

例えば、Amazon.co.jp 向けの amazon.csv の場合：

```csv
（Amazon ポイント）,通信,その他
（Amazonポイント）,通信,その他
（割引）,通信,その他
（配送料・手数料）,通信,宅配便
【大容量】ハミングファイン 柔軟剤 リフレッシュグリーンの香り 詰め替え 1200ml,日用雑貨,消耗品
Echo Dot (エコードット) 第2世代 - スマートスピーカー with Alexa、ホワイト,大型出費,家電
Ishow ランドリーバスケット 洗濯かご二段 キャスター付き収納ボックス 防水 オックスフォード 折り畳み式 仕切り 蓋付き 大容量 洗濯袋 ランドリーポーチ ランドリー収納 (50×36×60cm),住まい,家具
LITTLE TREEチェアマット 120×90cm厚1.5mm 床を保護 机の擦り傷防止滑り止め カート可能 透明大型デスク足元マット フローリング/畳/床暖房対応 (120×90cm),住まい,家具
Transcend USBメモリ 32GB USB3.1 & USB 3.0 キャップレス シルバー 耐衝撃 防滴 防塵 TS32GJF710S,大型出費,家電
WD HDD 内蔵ハードディスク 3.5インチ 8TB WD Red NAS用 WD80EFAX 5400rpm 3年保証,大型出費,家電
WD HDD 内蔵ハードディスク 3.5インチ 8TB WD Red NAS用 WD80EFZX 5400rpm 3年保証,大型出費,家電
パナソニック エネループ 急速充電器セット 単4形充電池 2本付き スタンダードモデル K-KJ23MCC02,日用雑貨,消耗品
```

## 変換対象 CSV の準備方法

### WAON

1\.

[www.waon.com](https://www.waon.com/wmUseHistoryInq/init.do) にログインします。

2\.

ログイン後のページ下部、◯月分利用履歴の明細から
該当月の HTML テーブルを Google スプレッドシートにコピーします。
※ 10 件ずつしか表示されていないので、[次の10件→]が表示されなくなるまで
　[次の10件→]でページをめくり、全件コピーします。

Chrome の場合は [Table Capture](https://chrome.google.com/webstore/detail/table-capture/iebpjdmgckacbodjpijphcplhebcmeop) という拡張機能を使います。

3\.

該当月のスプレッドシートを開いた状態で [ファイル] -> [形式を指定してダウンロード] -> [カンマ区切りの値(.csv、現在のシート)]

### ヨドバシゴールドポイントカード・プラス

1\.

[GOLD POINT CARD+](https://secure.goldpoint.co.jp/gpm/authentication/index.html) にログインします。

2\.

[メンバーメニュー] -> [クレジットカードサービス] -> [ご利用明細照会] をクリック

3\.

画面下部で [お支払い月] を選択し、[照会] ボタンをクリック

4\.

[CSV 形式で保存する] ボタンをクリック

### 三菱 UFJ 銀行

1\.

[三菱 UFJ ダイレクト](https://entry11.bk.mufg.jp/ibg/dfw/APLIN/loginib/login?_TRANID=AA000_001)にログインします。

2\.

[入出金明細をみる] をクリック

3\.

[照会期間] を選択し [照会] ボタンをクリック

4\.

[明細をダウンロード] ボタンをクリック

### Suica, PASMO

1\.

Windows コンピューターと「NFC ポート/パソリ」を準備し、 SFCard Viewer 2 をインストールします。

Windows コンピューターと「NFC ポート/パソリ」の要件は[こちら](https://www.sony.co.jp/Products/felica/consumer/download/sfcardviewer2.html)を確認します。

※作者は、Windows コンピューターは Windows 10 Home 64ビット(x64) を使っています。

※作者は、「NFC ポート/パソリ」は [RC-S380/S](https://www.amazon.co.jp/%E3%82%BD%E3%83%8B%E3%83%BC-NFC%E9%80%9A%E4%BF%A1%E3%83%AA%E3%83%BC%E3%83%80%E3%83%BC-PaSoRi-RC-S380-S/dp/B00VR1WARC) を使っています。

2\.

SFCard Viewer 2 を起動し、「NFC ポート/パソリ」に Suica, PASMO をタッチします。

3\.

[メニュー] -> [フィアルに保存]をクリック

※ Suica, PASMO には 20 件までしか履歴が残らないので、
　 定期的に CSV を取得し続ける必要があります。

### モバイル Suica

1\.

[www.mobilesuica.com](https://www.mobilesuica.com/) にログインします。

2\.

[SF (電子マネー) 利用履歴] をクリック

3\.

履歴から該当月の HTML テーブルを Google スプレッドシートにコピーします。

Chrome の場合は [Table Capture](https://chrome.google.com/webstore/detail/table-capture/iebpjdmgckacbodjpijphcplhebcmeop) という拡張機能を使います。

4\.

該当月のスプレッドシートを開いた状態で [ファイル] -> [形式を指定してダウンロード] -> [カンマ区切りの値(.csv、現在のシート)]

モバイル Suica の履歴は日付の情報が年を含まないので、履歴の日付に年の情報を付加するために、
用意したファイル名には西暦年を表す 4 ~ 6 桁の半角数字を含めます。

例: mobile_suica_202210.csv

ファイル名の中で、最後に半角数字が 4 ~ 6 桁並んでいる部分の内、最初の 4 桁を西暦年として扱います。
(5 ~ 6 桁の場合の最後の 2 桁は、月別にファイルを分けることを想定して、月が付与できるようにしています。)

上記のファイル名の例の場合、西暦年は `2022` となります。
この西暦年と CSV の履歴の日付から Zaim 形式の CSV の履歴の日付を計算します。

### Amazon

1\.

Chrome 拡張の[アマゾン注文履歴フィルタ](https://chrome.google.com/webstore/detail/%E3%82%A2%E3%83%9E%E3%82%BE%E3%83%B3%E6%B3%A8%E6%96%87%E5%B1%A5%E6%AD%B4%E3%83%95%E3%82%A3%E3%83%AB%E3%82%BF/jaikhcpoplnhinlglnkmihfdlbamhgig)をインストールします。

2\.

[Amazon.co.jp](https://www.amazon.co.jp/) にログインします。

3\.

[アカウント&リスト] -> [注文履歴] をクリック

4\.

[対象月選択] を選択し、[領収書印刷用画面] ボタンをクリック

5\.

ログイン画面が表示されるのでログインします。

6\.

[注文履歴CSV(参考用)ダウンロード] ボタンをクリックします。

### ビューカード

1\.

[ビューカード](https://www.jreast.co.jp/card/index.html/) にログインします。

2\.

[ご利用明細照会 (お支払方法の変更)] をクリック

3\.

明細を取得する月のボタンをクリックします。

4\.

[明細 CSV ダウンロード] ボタンをクリック

### PayPal

1\.

[PayPal](https://www.paypal.com/signin) にログインします。

2\.

[レポート] をクリック

3\.

[取引履歴のダウンロード] をクリック

4\.

フォームに次の内容を入力して [レポートを作成] ボタンをクリックします。

入力項目|入力する内容
---|---
[取引タイプ]|「すべての取引」
[日付範囲]|該当月の初日から末日
[形式]|「CSV」

5\.

「取引レポートをダウンロードできるようになりました」というメールが届いたら
[ダウンロード] リンクをクリック

### 住信 SBI ネット銀行

「代表口座」と「SBI ハイブリッド預金」がそれぞれダウンロードできます。両方ダウンロードして変換し、両方 Zaim にインポートします。

1\.

[住信 SBI ネット銀行](https://www.netbk.co.jp/contents/pages/wpl010101/i010101CT/DI01010210) にログインします。

2\.

画面右上 [入出金明細] をクリック

3\.

フォームに次の内容を入力して [表示] ボタンをクリックします。

入力項目|入力する内容
---|---
[表示口座]|「代表口座」または「SBI ハイブリッド預金」
[期間]|「前月」

4\.

[CSV でダウンロード] ボタンをクリックします。

### PayPay カード

1\.

[PayPay カード](https://www.paypay-card.co.jp/member) にログインします。

2\.

画面上部 [利用明細] をクリック

3\.

該当月の [◯月] をクリック

4\.

画面を下にスクロールしていくとある [CSVダウンロード] ボタンをクリック
