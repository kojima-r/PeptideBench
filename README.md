# PeptideBench
peptipediaからベンチマークデータを作成するスクリプト

## Requirements
```
tqdm
requests
pandas
biopython
```
加えて，pypeptは以下でインストール加えて，
```
pip install git+https://github.com/Boehringer-Ingelheim/pyPept.git
```
## Preprocessing
今回はPositiveデータが5%以上のActivityに限定(33項目)

以下を除外
- Non-asciiを含む配列(beta 等)：
- アルファベット以外を含む配列：Anti-H など, 独自記法を導入している配列
- X,Z(グルタミンorグルタミン酸),B(アスパラギン酸orアスパラギン),J(ロイシンorイソロイシン)を含む配列（SMILES変換の都合上）
- その他SMILES変換に失敗する配列
 - TODO：pypeptのデフォルトモノマーライブラリ
 - O: ピロリシン（pyrrolysine）
 - U: セレノシステイン（Selenocysteine）
- 長さ150以上の配列
- 今回，予測対象とする全てのActivity でnegativeになる配列

## 使用API

Activity一覧
```
https://api.app.peptipedia.cl/api/get_activities_sources_list/
```

ダウンロード
```
https://api.app.peptipedia.cl/files/downloads/**.fasta
```
