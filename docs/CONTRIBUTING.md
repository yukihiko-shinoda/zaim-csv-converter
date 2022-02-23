# 開発者向けドキュメント

## zaim-csv-converter の対応口座追加開発手順

### 1. ユーザー設定の開発

#### 1-1. `config.yml.dist` の追記

`config.yml.dist` に設定項目と雛形となる値、項目の説明を追記します。

#### 1-2. 設定 dataclass の実装

config.py に `DataClassJsonMixin` を継承し、 config.yml で設定できる項目を property として定義した dataclass を作成します。

#### 1-3. 設定項目の type hint の実装

config.py の Config クラスに新規対応口座の `DataClassJsonMixin` インスタンスの type hint のための property を追加します。

### 2. 変換用テーブル CSV の定義

新しい口座の明細から Zaim のお店・品目への変換のために
新しい変換用テーブル CSV ファイルを追加する必要がある場合は、
`file_csv_convert.py` の `FileCsvConvert` に
変換用テーブル CSV の定義を追加します。

プロパティ名|内容
---|---
id|データベースカラムで変換用テーブル CSV の種類を表す`file_csv_convert_id`として使われます。重複しないように連番を付与してください。
name|CSV ファイル名を定義します。
convert_table_type|入力 CSV ファイルの各行がお店単位の場合は `ConvertTableType.STORE` を、品目単位の場合は `ConvertTableType.ITEM` を、それぞれ指定します。

### 3. 入力 CSV ファイルのフォーマットに依存する処理を追加する開発

inputcsvformats 配下に新規対応口座の入力 CSV モデル module を作成します。

#### 3-1. 入力 CSV の行の各列のプロパティを定義した dataclass の実装

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

#### 3-2. 入力 CSV の行のモデルクラスの実装

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
is_row_to_skip|この行を処理する必要がない場合、`True` を返すように実装してください。実装しない場合は常に skip せず処理されます。

##### どうして dataclass を作ったのに CSV の行のモデルクラスも作るの？

CSV 形式は、実際には性質の異なる行や、その属性を、
言わば強引に 1 つのテーブルとして出力しています。
(データベース用語の「非正規化」)
たとえば、多くの CSV では、出金の行と入金の行で、
それぞれの行のみが値を持つ列が存在することがあります。

このような観点から、行の中の不要な列などはプロパティとして持たないモデルクラスに変換した方が、
プログラム中で間違った仕訳をコーディングしてしまうリスクが減らせることが期待できます。

### 4. 入力 CSV の行モデルを Zaim 形式 CSV の行モデルに変換する処理を追加する開発

rowconverters 配下に新規対応口座の CSV 行モデル変換 module を作成します。

#### 4-1. 入力 CSV の行モデルクラスを生成する Factory クラスの実装

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

#### 4-2. 入力 CSV の行モデルクラスをZaim形式CSVの行モデルクラス変換する Converter クラスの実装

InputRow モデルを ZaimRow モデルに変換するための Converter クラスと、
手順 4-5. で後述する ZaimRowConverterFactory クラスで、
入力 CSV の行モデルクラスインスタンスを作り分けることにより、
Strategy パターンを実装できます。

実装する Converter クラスは、対象の行がZaimの支出、収入、振替の内、どの記録にあたるかによって、
`ZaimIncomeRowConverter`, `ZaimPaymentRowConverter`, `ZaimTransferRowConverter`
のいずれかを継承して実装してください。

`ZaimIncomeRowConverter`

メソッド、プロパティ名|実装内容
---|---
cash_flow_target|この行が収入の行の場合、出力 CSV に「入金先」として記載すべき文字列を返してください。
amount|この行が収入の行の場合、出力 CSV に「収入」として記載すべき数値を返してください。

`ZaimPaymentRowConverter`

メソッド、プロパティ名|実装内容
---|---
cash_flow_source|この行が支出の行の場合、出力 CSV に「支払元」として記載すべき文字列を返してください。
amount|この行が支出の行の場合、出力 CSV に「支出」として記載すべき数値を返してください。

`ZaimTransferRowConverter`

メソッド、プロパティ名|実装内容
---|---
cash_flow_source|この行が振替の行の場合、出力 CSV に「支払元」として記載すべき文字列を返してください。
cash_flow_target|この行が振替の行の場合、出力 CSV に「入金先」として記載すべき文字列を返してください。
amount|この行が振替の行の場合、出力 CSV に「振替」として記載すべき数値を返してください。

### 4-5. ZaimRowConverterFactory クラスの実装

`ZaimRowConverterFactory` クラスを継承し、`create()` メソッドを実装します。
引数の `ValidatedInputRow` に対して、どの `ZaimRowConverter` クラスを利用するかを選択します。
(rowconverters/waon.py, rowconverters/mufg.py, rowconverters/sf_card_viewer.py を参考にしてください。)

### 5. 口座に依存する属性を定義

account.py の Account Enum クラスに新規対応口座用の AccountContext インスタンス定数を追加します。
AccountContext の各プロパティは以下のように定義します。

プロパティ名|内容
---|---
regex_csv_file_name|入力 CSV ファイルが、この口座の CSV ファイルであると判定するための正規表現を定義します。
god_slayer_factory|CSV ファイルのレコードを読み取るためのジェネレーターである `GodSlayer` の Factory クラス `GodSlayerFactory` のインスタンスを指定します。CSV の書式に合わせ、引数で `hedder`, `footer`, `partition`, `encoding` などを指定します。詳しくは [GodSlayer の README](https://pypi.org/project/godslayer/) を確認してください。
input_row_data_class|手順3.で実装した `InputRowData` を指定します。
input_row_factory|手順4.で実装した `InputRowFactory` を指定します。こちらはクラスではなくインスタンス生成して渡します。
zaim_row_converter_factory|手順4.で実装した `ZaimRowConverter` を指定します。こちらはクラスではなくインスタンス生成して渡します。

### 6. 属性の定義の追加に伴うテストの修正

### 6-1. `FilePathConvertTable` の修正

手順 2. で変換テーブル CSV ファイルに依存する属性の定義を追加すると、
テストが失敗するようになるので修正します。

`tests/test_file_csv_convert.py` の `FilePathConvertTable` に
追加した口座のお店、品目の変換テーブルが定義されている
CSV ファイルへのパスの例を追加します。

### 6-2. `FilePathInput` の修正

手順 5. で口座に依存する属性の定義を追加すると、
テストが失敗するようになるので修正します。

`tests/test_account.py` の `FilePathInput` に
追加した口座の入力 CSV ファイルへのパスの例を追加します。

### 7. 結合テストの追加

#### 7-1. 変換テーブルの例の追加

次のディレクトリー内に変換テーブルの例となる CSV ファイルを追加します。

`tests/testresources/zaim/test_zaim_csv_converter/csvconvettable`

#### 7-2. 入力 CSV ファイルの例の追加

次のディレクトリー内に入力 CSV ファイルの例となる CSV ファイルを追加します。
クレジットカード情報などをリポジトリーにコミットしないよう注意します。

`tests/testresources/zaim/test_zaim_csv_converter/csvinput_test_success`

#### 7-3. テスト用 config.yml に口座の設定を追加

`tests/testresources/config.yml.dist` に追加した口座の設定の例を追加します。

#### 7-4. 期待する変換結果の定義

`tests/testlibraries/integration_test_expected_factory.py` に、期待する変換結果を返す関数を定義します。

#### 7-5. `test_zaim_csv_converter.py` の修正

`tests/zaim/test_zaim_csv_converter.py` を開き、`test_success()` を確認します。

ファイルの数を確認している箇所を修正します:

```diff
- assert len(files) == 17
+ assert len(files) == 18
```

変換後のファイルの assertion を追加します:

```diff
        checker.assert_file("pay_pal201810.csv", create_zaim_row_data_pay_pal_201810())
+       checker.assert_file("sbi_sumishin_net_bank202201.csv", create_zaim_row_data_sbi_sumishin_net_bank_202201())
```

### 8. ユニットテストの実行

```console
pipenv run test
```

### 9. `README.md` の追記

#### 9-1. 対応口座情報の追加

「現在は以下の口座の CSV に対応しています」の箇所に口座を追加します。

#### 9-2. 対応口座情報の追加

「各口座毎に、以下のファイル名と形式で準備します」の箇所に口座とファイル名を追加します。

#### 9-3. 変換対象の CSV の追加

「変換対象の CSV を準備します」の箇所に口座とファイル名に含まれるべき文字列を追加します。

#### 9-4. 変換対象 CSV の準備方法の追加

「変換対象 CSV の準備方法」の箇所に口座の CSV ファイルを準備する方法を追加します。

## ユビキタス言語

言葉|内容
---|---
row|CSV の行を表します。
record|CSV の設計者が意図していると思われる、 1 レコード分のデータを表します。神 CSV に対応するため、必ずしも CSV 1 行と対応するとは限らないものとして設計します。
record data|record を一旦、文字列型のままオブジェクト化するための dataclass です。validate メソッドを実装し、プロパティが正しい型に変換できるか検証します。
store|Zaim の「お店」を表します。
item|Zaim の「品目」を表します。
