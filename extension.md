# zaim-csv-converter の対応口座追加開発手順

## 1. ユーザー設定の開発

config.yml によるユーザー設定を利用する場合、以下の開発を行います。

### 1-1. 設定 dataclass の実装

config.py に `DataClassJsonMixin` を継承し、 config.yml で設定できる項目を property として定義した dataclass を作成します。

### 1-2. 設定項目の type hint の実装

config.py の Config クラスに新規対応口座の `DataClassJsonMixin` インスタンスの type hint のための property を追加します。

## 2. 入力 CSV ファイルのフォーマットに依存する処理を追加する開発

inputcsvformat 配下に新規対応口座の入力 CSV モデル module を作成します。

### 2-1. 入力 CSV の行の各列のプロパティを定義した dataclass の実装

入力 CSV の行の各列のプロパティを定義した dataclass を作成します。
入力 CSV の行がお店単位の場合は `InputStoreRowData` を継承、
入力 CSV の行が品目単位の場合は `InputItemRowData` を継承して作成します。

入力 CSV の行のいずれかの列データから日付型を返すプロパティ date を実装します。

入力 CSV の行がお店単位の場合は、変換用テーブルの CSV からお店を検索するための
入力 CSV の行のいずれかの列データを返すプロパティ store_name を実装します。

入力 CSV の行が品目単位の場合は、変換用テーブルの CSV から品目を検索するための
入力 CSV の行のいずれかの列データを返すプロパティ item_name を実装します。

その他の抽象メソッド、プロパティは以下の内容を実装してください。

メソッド、プロパティ名|実装内容
---|---
validate|モデル内のプロパティを検証し、異常があれば `InvalidRowError` を生成してプロパティ `list_error` に追加して `True` を返してください。 異常がなければ `False` を返してください。

### 2-2. 入力 CSV の行のモデルクラスの実装

入力 CSV の行のモデルクラスを作成します。
入力 CSV の行がお店単位の場合は InputStoreRow を継承、
入力 CSV の行が品目単位の場合は InputItemRow を継承して作成します。

__init__() で必ず super().__init__() を呼び出してください。
インスタンス生成時、super().__init__() 内で、
手順2-1.で指定した store, item プロパティを使ってデータベースを検索し、
store, item に検索結果のモデルがセットされます。
検索に失敗した場合、store, item は None となり、
変換処理がこれを検知して、この行のお店、品目がデータベースに未登録であると判定し、
error_undefined_content.csv に書き出します。

なお、InputItemRow を継承した場合は store プロパティをオーバーライトして
Store モデルを返すように実装してください。(amazon.py を参考にしてください。)

抽象メソッド、プロパティは以下の内容を実装してください。

メソッド、プロパティ名|実装内容
---|---
validate|モデル内のプロパティを検証し、異常があれば `InvalidRowError` を生成してプロパティ `list_error` に追加して `True` を返してください。 異常がなければ `False` を返してください。
is_row_to_skip|この行を処理する必要がない場合、Falseを返すように実装してください。実装しない場合は常にskipせず処理されます。

## 3. 入力 CSV の行モデルを Zaim 形式 CSV の行モデルに変換する処理を追加する開発

rowconverters 配下に新規対応口座の CSV 行モデル変換 module を作成します。

### 3-1. 入力 CSV の行モデルクラスを生成する Factory クラスの実装

処理の中では InputRow を直接生成せず、 Factory クラスを経由して生成するようにしています。
これは以下の理由のためです:

- InputRow は CSV のフォーマットを表しており、
同じ CSV フォーマットの異なる口座の設定を DI できるようにするため
(inputcsvformats/sf_card_viewer.py を参考にしてください。)
- 手順2-2.で実装した InputRow モデルの各プロパティの実装が if だらけにならないようにするため
- 行の種類によって不要な列を処理から省くため

InputRowFactory を継承した Factory クラスを作成し、
手順2-1.で作成した dataclass を引数に、手順2-2.で作成したモデルクラスを返す
create メソッドを実装してください。

### 3-2. 入力 CSV の行モデルクラスをZaim形式CSVの行モデルクラス変換する Converter クラスの実装

InputRow モデルを ZaimRow モデルに変換するための Converter クラスと、
手順 3-5. で後述する ConverterSelector クラスで、
入力 CSV の行モデルクラスインスタンスを作り分けることにより、
Strategy パターンを実装できます。

実装する Coverter クラスは、対象の行がZaimの支出、収入、振替の内、どの記録にあたるかによって、
`ZaimIncomeRowConverter`, `ZaimPaymentRowConverter`, `ZaimTransferRowConverter`
のいずれかを継承して実装してください。

`ZaimIncomeRowConverter`

メソッド、プロパティ名|実装内容
---|---
_cash_flow_target|この行が収入の行の場合、出力 CSV に「入金先」として記載すべき文字列を返してください。
_amount_income|この行が収入の行の場合、出力 CSV に「収入」として記載すべき数値を返してください。

`ZaimPaymentRowConverter`

メソッド、プロパティ名|実装内容
---|---
_cash_flow_source|この行が支出の行の場合、出力 CSV に「支払元」として記載すべき文字列を返してください。
_amount_payment|この行が支出の行の場合、出力 CSV に「支出」として記載すべき数値を返してください。

`ZaimTransferRowConverter`

メソッド、プロパティ名|実装内容
---|---
_cash_flow_source|この行が振替の行の場合、出力 CSV に「支払元」として記載すべき文字列を返してください。
_cash_flow_target|この行が振替の行の場合、出力 CSV に「入金先」として記載すべき文字列を返してください。
_amount_transfer|この行が振替の行の場合、出力 CSV に「振替」として記載すべき数値を返してください。

## 3-5. 、ConverterSelector クラスの実装

`ZaimRowConverterSelector` クラスを継承し、`create()` メソッドを実装します。
引数の `ValidatedInputRow` に対して、どの `ZaimRowConverter` クラスを利用するかを選択します。
(rowconverters/waon.py, rowconverters/mufg.py, rowconverters/sf_card_viewer.py を参考にしてください。)

## 4. 口座に依存する属性を定義

account.py の Account Enum クラスに新規対応口座用の AccountContext インスタンス定数を追加します。
AccountContext の各プロパティは以下のように定義します。

プロパティ名|内容
---|---
id|データベースカラムで口座の種類を表す`account_id`として使われます。重複しないように連番を付与してください。
file_name_csv_convert|お店、品目の変換テーブルが定義されている CSV ファイル名を定義します。
regex_csv_file_name|入力 CSV ファイルが、この口座の CSV ファイルであると判定するための正規表現を定義します。
convert_table_type|入力 CSV ファイルの各行がお店単位の場合は `ConvertTableType.STORE` を、品目単位の場合は `ConvertTableType.ITEM` を、それぞれ指定します。
input_row_data_class|手順2.で実装した `InputRowData` を指定します。
input_row_factory|手順2.で実装した `InputRowFactory` を指定します。こちらはクラスではなくインスタンス生成して渡します。
zaim_row_converter_selector|手順3.で実装した `ZaimRowConverter` を指定します。こちらはクラスではなくインスタンス生成して渡します。
encode|入力 CSV のエンコードが UTF-8 以外の場合、定義します。
csv_header|入力 CSV にヘッダーが含まれる場合、定義します。定義すると、読み取り処理がヘッダーの行までを自動的に読み飛ばします。

## 5. ユニットテストの実行

```bash
pipenv run test
```