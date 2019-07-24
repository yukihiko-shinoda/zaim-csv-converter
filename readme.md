# zaim-csv-converter

各口座のWEBサイト等で出力できるCSVを
Zaimのフォーマットに変換するPython製のコンバーターです。

Zaimで口座連携をするために
口座のアカウント情報をクラウドに預けるのが心配な方は
ぜひご利用ください。

現在は以下の口座のCSVに対応しています。

- WAON
- ヨドバシゴールドポイントカード・プラス
- 三菱UFJ銀行
- PASMO
- Amazon.co.jp

※↓対応口座追加のための開発手順をまとめました、プルリクエストをお待ちしています。

[zaim-csv-converter の対応口座追加開発手順](extension.md)

## 動作確認環境

- Windows 10 home 64bit
- Python 3.7.4
- Pipenv 2018.11.26

※上記より新しければ動作するものと思われます。

## 初回のみ行う利用準備

### 1. プロジェクトをダウンロードします

```bash
git clone https://github.com/yukihiko-shinoda/zaim-csv-converter.git
```

### 2. 設定ファイルを準備します

config.yml.distをコピーしてconfig.ymlを作成し、
Zaimの利用状態に合わせてconfig.ymlを編集します。

各項目の意味はconfig.yml.distを参照してください。

### 3. 変換用テーブルのCSVを準備します

各口座のWEBサイト等から出力したCSVに含まれるお店の名前を、
Zaim上で登録しているお店の名前に変換する必要があります。
この、変換前と変換後のお店の名前、デフォルトのカテゴリーを定義するCSVを
 csvconverttable/ ディレクトリー配下に準備します。

CSVの作成方法は[変換用テーブルのCSVのつくり方](#変換用テーブルのCSVのつくり方)を参照してください。

各口座毎に、以下のファイル名と形式で準備します。

口座|ファイル名|形式
---|---|---
WAON|waon.csv|お店単位
ヨドバシゴールドポイントカード・プラス|gold_point_card_plus.csv|お店単位
三菱UFJ銀行|mufg.csv|お店単位
PASMO|sf_card_viewer.csv|お店単位
Amazon.co.jp|amazon.csv|品目単位

※ 文字コードはUTF-8で準備してください。


### 4. Pythonプロジェクト実行用の仮想環境を作成します

```bash
pipenv install
```


## 利用方法

### 1. 変換対象のCSVを準備します

変換対象の各口座のCSVファイルを csvinput/ ディレクトリ―配下に配置します。

複数のファイルを一度に処理できます。

各CSVファイルをどの口座のものとして処理するかの判定は
ファイル名に以下の文字列が含まれているかどうかで判定を行います。

口座|ファイル名に含まれるべき文字列
---|---
WAON|waon
ヨドバシゴールドポイントカード・プラス|gold_point_card_plus
三菱UFJ銀行|mufg
PASMO|sf_card_viewer
Amazon.co.jp|amazon

変換対象CSVの準備方法の詳細は[変換対象CSVの準備方法](#変換対象CSVの準備方法)を参照してください。


### 2. 実行します

```bash
pipenv run start
```

### 3. 実行結果の確認を行います

実行後、
 csvoutput/ に csvinput/ と同名のファイルが作成されます。
 出力されたCSVが意図通りになっているか、入力CSVと出力CSVを目視で確認することをおすすめします。

ここでエラーメッセージが表示された場合は、
エラーの内容に従いCSVファイルの確認等を行ってから、再度実行します。

代表的な例として:

```bash
KeyError: 'Undefined store name in convert table CSV exists. Please check error.csv.'
```

上記のエラーが表示された場合は、 csvoutput/error.csv に
変換用テーブルのCSVに未定義のお店の名前、品目名の一覧が出力されますので、
変換テーブルのCSVに変換の定義を追加してから、再度実行します。

### 4. Zaimにインポートします

ブラウザーでWEB版のZaim: https://zaim.net/ にログインし、
画面右上の

[設定] -> [ファイル入出力] -> [Zaim の出力ファイルをアップロード]

から csvoutput/ ディレクトリーに出力されたCSVをアップロードします。

### 5. アップロードされた情報を確認します

Zaim側のアップデートに伴う仕様変更等で、予期しない登録が発生する可能性を考慮し、
Zaimの履歴画面で、 csvoutput/ ディレクトリーのCSVとZaim上の登録内容の比較を目視で行います。

また、この段階で、カテゴリが変換用テーブルのCSVで指定したデフォルトのカテゴリと異なる履歴を
Zaim上で修正します。

## 変換用テーブルのCSVのつくり方

### お店単位

左から順に以下の情報を各列に定義していきます。

- 口座のWEBサイト等からダウンロードしたCSVに含まれるお店の名前
- Zaim上で登録しているお店の名前
- このお店での履歴が支出履歴の場合のデフォルトのカテゴリ
- このお店での履歴が支出履歴の場合のデフォルトのカテゴリ内訳
- このお店での履歴が収入履歴の場合のデフォルトのカテゴリ(例えば、WAONのポイントダウンロード等)
- このお店での履歴が振替履歴の場合の振替対象口座名(例えば、銀行口座のクレジット引き落とし等)

例えば、三菱UFJ銀行向けmufg.csvの場合：

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

例えば、Amazon.co.jp向けのamazon.csvの場合：

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


## 変換対象CSVの準備方法

### WAON

1.
www.waon.com にログインします。

https://www.waon.com/wmUseHistoryInq/init.do

2.
ログイン後のページ下部、◯月分利用履歴の明細から
該当月のHTMLテーブルをGoogleスプレッドシートにコピーします。
※10件ずつしか表示されていないので、[次の10件→]が表示されなくなるまで
　[次の10件→]でページをめくり、全件コピーします。

Chromeの場合はTable Captureという拡張機能を使います。

https://chrome.google.com/webstore/detail/table-capture/iebpjdmgckacbodjpijphcplhebcmeop

3.
該当月のスプレッドシートを開いた状態で[ファイル] -> [形式を指定してダウンロード] -> [カンマ区切りの値(.csv、現在のシート)]

4.
Open Officeでダウンロードしたcsvファイルを以下の設定で開きます。
文字コード: UTF-8
区切り文字: コンマ
テキストの区切り記号: “(ダブルクォート)


### GOLD POINT CARD+

1.
GOLD POINT CARD+にログインします。

https://secure.goldpoint.co.jp/gpm/authentication/index.html

2.
[メンバーメニュー] -> [クレジットカードサービス] -> [ご利用明細照会]をクリック

3.
画面下部で[お支払い月]を選択し、[照会]ボタンをクリック

4.
[CSV形式で保存する]ボタンをクリック


### 三菱UFJ銀行

1.
三菱UFJダイレクトにログインします。

https://entry11.bk.mufg.jp/ibg/dfw/APLIN/loginib/login?_TRANID=AA000_001

2.
[入出金明細をみる]をクリック

3.
[照会期間]を選択し[照会]ボタンをクリック

4.
[明細をダウンロード]ボタンをクリック


### PASMO

1.
Windowsコンピューターと「NFCポート/パソリ」を準備し、
SFCard Viewer 2をインストールします。

↓Windowsコンピューターと「NFCポート/パソリ」の要件はこちらを確認します。

https://www.sony.co.jp/Products/felica/consumer/download/sfcardviewer2.html

※作者は、Windowsコンピューターは Windows10 Home 64ビット(x64) を使っています。

※作者は、「NFCポート/パソリ」は RC-S380/S を使っています。

https://www.amazon.co.jp/%E3%82%BD%E3%83%8B%E3%83%BC-NFC%E9%80%9A%E4%BF%A1%E3%83%AA%E3%83%BC%E3%83%80%E3%83%BC-PaSoRi-RC-S380-S/dp/B00VR1WARC

2.
SFCard Viewer 2を起動し、「NFCポート/パソリ」にPASMOをタッチします。

3.
[メニュー] -> [フィアルに保存]をクリック

※PASMOには20件までしか履歴が残らないので、
　定期的にCSVを取得し続ける必要があります。
　

### Amazon

1.
Chrome拡張の「マゾン注文履歴フィルタ」をインストールします。

https://chrome.google.com/webstore/detail/%E3%82%A2%E3%83%9E%E3%82%BE%E3%83%B3%E6%B3%A8%E6%96%87%E5%B1%A5%E6%AD%B4%E3%83%95%E3%82%A3%E3%83%AB%E3%82%BF/jaikhcpoplnhinlglnkmihfdlbamhgig

2.
Amazon.co.jpにログインします。

https://www.amazon.co.jp/

3.
[アカウント&リスト] -> [注文履歴]をクリック

4.
[対象月選択]を選択し、[領収書印刷用画面]ボタンをクリック

5.
ログイン画面が表示されるのでログインします。

6.
[注文履歴CSV(参考用)ダウンロード]ボタンをクリックします。
