# zaim-csv-converter の対応口座追加開発手順

## 1. ユーザー設定の開発
config.yml によるユーザー設定を利用する場合、以下の開発を行います。

### 1-1. yaml キーの追加
config.py の AccountKey Enum クラスに新規対応口座用の yaml キーを追加します。

### 1-2. 設定 dataclass の作成
config.py に DataClassJsonMixin を継承し、 config.yml で設定できる項目を property として定義した dataclass を作成します。

### 1-3. type hint の追加
config.py の Config クラスに新規対応口座の AccountConfig インスタンスの type hint のための property を追加します。

## 2. 入力 CSV ファイルのフォーマットに依存する処理の追加
inputcsvformat 配下に新規対応口座の入力 CSV モデル module を作成します。

### 2-1. 入力 CSV の行の各列のプロパティを定義した dataclass の作成
入力 CSV の行の各列のプロパティを定義した dataclass を作成します。
入力 CSV の行がお店単位の場合は AccountStoreRowData を継承、
入力 CSV の行が品目単位の場合は AccountItemRowData を継承して作成します。

入力 CSV の行のいずれかの列データから日付型を返すプロパティ date を実装します。

入力 CSV の行がお店単位の場合は、変換用テーブルの CSV からお店を検索するための
入力 CSV の行のいずれかの列データを返すプロパティ store_name を実装します。

入力 CSV の行が品目単位の場合は、変換用テーブルの CSV から品目を検索するための
入力 CSV の行のいずれかの列データを返すプロパティ item_name を実装します。

### 2-2. 入力 CSV の行のモデルクラスの作成
入力 CSV の行のモデルクラスを作成します。
入力 CSV の行がお店単位の場合は InputStoreRow を継承、
入力 CSV の行が品目単位の場合は InputItemRow を継承して作成します。

__init__() で必ず super().__init__() を呼び出してください。
インスタンス生成時、super().__init__() 内で、
手順2-1.で指定した zaim_store, zaim_item プロパティを使ってデータベースを検索し、
zaim_store, zaim_item に検索結果のモデルがセットされます。
検索に失敗した場合、zaim_store, zaim_item は None となり、
変換処理がこれを検知して、この行のお店、品目がデータベースに未登録であると判定し、
error.csv に書き出します。

なお、InputItemRow を継承した場合は zaim_store プロパティをオーバーライトして
Store モデルを返すように実装してください。(amazon.py を参考にしてください。)

抽象メソッド、プロパティは以下の内容を実装してください。

メソッド、プロパティ名|実装内容
---|---
convert_to_zaim_row|ZaimIncomeRow, ZaimPaymentRow, ZaimTransferRowのいずれかをインスタンス生成して返してください。この行がZaimの支出、収入、振替の内、どの記録にあたるか、ということです。
is_row_to_skip|この行を処理する必要がない場合、Falseを返すように実装してください。実装しない場合は常にskipせず処理されます。
zaim_income_cash_flow_target|この行が収入の行の場合、出力 CSV に「入金先」として記載すべき文字列を返してください。
zaim_income_ammount_income|この行が収入の行の場合、出力 CSV に「収入」として記載すべき数値を返してください。
zaim_payment_cash_flow_source|この行が支出の行の場合、出力 CSV に「支払元」として記載すべき文字列を返してください。
zaim_payment_amount_payment|この行が支出の行の場合、出力 CSV に「支出」として記載すべき数値を返してください。
zaim_transfer_cash_flow_source|この行が振替の行の場合、出力 CSV に「支払元」として記載すべき文字列を返してください。
zaim_transfer_cash_flow_target|この行が振替の行の場合、出力 CSV に「入金先」として記載すべき文字列を返してください。
zaim_transfer_amount_transfer|この行が振替の行の場合、出力 CSV に「振替」として記載すべき数値を返してください。

### 2-3. CSVの行モデルクラスを生成する Factory クラスの作成

手順2-2.の各プロパティの実装が if だらけにならないよう、
Factory クラスで入力 CSV の行モデルクラスインスタンスを作り分けることで
Strategy パターンを実装できます。(mufg.py, waon.py を参考にしてください。)

InputRowFactory を継承した Factory クラスを作成し、
手順2-1.で作成した dataclass を引数に、手順2-2.で作成したモデルクラスを返す
create メソッドを実装してください。

## 3. 口座に依存するプロパティを定義
account.py の Account Enum クラスに新規対応口座用の AccountDependency インスタンス定数を追加します。
AccountDependency の各プロパティは以下のように定義します。

プロパティ名|内容
---|---
id|データベースカラムで口座の種類を表す"account_id"として使われます。重複しないように連番を付与してください。
file_name_csv_convert|お店、品目の変換テーブルが定義されている CSV ファイル名を定義します。
regex_csv_file_name|入力 CSV ファイルが、この口座の CSV ファイルであると判定するための正規表現を定義します。
convert_table_model_class|入力 CSV ファイルの各行がお店単位の場合は Store を、品目単位の場合は Item を、それぞれ指定します。
input_row_data_class|手順2.で作成した InputRowData を指定します。
input_row_factory|手順2.で作成した InputRowFactory を指定します。こちらはクラスではなくインスタンス生成して渡します。
encode|入力 CSV のエンコードが UTF-8 以外の場合、定義します。
csv_header|入力 CSV にヘッダーが含まれる場合、定義します。定義すると、読み取り処理がヘッダーの行までを自動的に読み飛ばします。

## 4. unittestの実行

```bash
pipenv run test
```