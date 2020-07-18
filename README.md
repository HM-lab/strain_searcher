# strain_searcher

## Description
複数のファイルを横断して酵母株のデータを検索するGUIアプリケーション
gene-name、y-nameどちらでも検索可能

## Requirements

* python 3.x

* pandas 1.0.3

* numpy 1.18.2

* PyQt5 5.14.2

## usage

* 任意のフォルダにクローンしてください。

```bash
git clone git@github.com:HM-lab/strain_searcher.git
```

* 検索先のデータシートを'datasheets'フォルダに配置してください。\
デフォルトで以下のファイルが配置されています。
  - Heterozygous_diploid_obs_v7.0.xls
  - Mat_a_obs_v5.0_wiki用.xlsx
  - TS mutant (TSv6) library_list.xls
  - Yeast_GFP_Collection_Data.xls
\
※ 'name_dict.csv' は設定はファイルなので変更しないでください。

* gui.pyを実行してGUIから検索を実行してください。
```bash
python gui.py
```

## コンパイル
コンパイルすることで、スタンドアロンアプリケーション (pythonなしで実行可能) にすることができます。

""""""編集中""""""