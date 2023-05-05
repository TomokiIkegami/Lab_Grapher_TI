# What is "Lab_Grapher_TI" ?
研究室のフォーマットで自動的にグラフを生成するプログラムです。

Excelでグラフを研究室のフォーマットに合わせる作業が大変で、楽にグラフ作成したいと思って作り始めました。

でもプログラムが複雑になって、なんちゃってExcelが完成しそうです（笑）
# Features
いくつかの便利な機能を用意しました。

* 縦軸・横軸の補助単位を自動設定
* 生成したグラフは.svg形式で自動保存（Wordに貼るとグラフが綺麗）
* グラフエリアサイズを指定可能（mm単位）
* ラベルに数式を入力可能（Tex形式の数式入力。上付き・下付き文字なども入力可能。）
  
  ＜入力例＞
  * "\$\omega_{\rm{max}}\$" → $\omega_{\rm{max}}$
  * "\$\theta=\frac{F_Y}{F_X}\$" → $\theta=\frac{F_Y}{F_X}$

# Installation
## Prepare「data.csv」 
　実験データを「data.csv」に保存してください。保存時は次の形式でデータを保存してください。

**◎「data.csv」の中身◎**

1行目   X軸の名前␣\$X軸の量記号\$␣[-X軸の単位],Y軸の名前␣\$Y軸の量記号\$␣[-Y軸の単位]

2行目   X軸データ,Y軸データ

3行目   X軸データ,Y軸データ

…

データが用意できたら文字コードは「UTF-8」で保存してください。（文字化けの原因になります）

また、データは「graph_maker.py」と同じフォルダに置いてください。

## Run 「graph_maker.py」
「graph_maker.py」を実行してください。実行が完了すると、「graph.svg」というグラフファイルが自動生成します。

## Paste 「graph_maker.py」
　グラフファイル「graph.svg」をレポートなどに貼り付けてください。拡大しても綺麗なグラフです。

# Examples
　Lab_Grapher_TIを使って作ったグラフ例です。

![test1](https://github.com/TomokiIkegami/Lab_Grapher_TI/blob/main/test1/graph.svg)

![test2](https://github.com/TomokiIkegami/Lab_Grapher_TI/blob/main/test2/graph.svg)

![test3](https://github.com/TomokiIkegami/Lab_Grapher_TI/blob/main/test3/graph.svg)

![test4](https://github.com/TomokiIkegami/Lab_Grapher_TI/blob/main/test4/graph.svg)

![test5](https://github.com/TomokiIkegami/Lab_Grapher_TI/blob/main/test5/graph.svg)

![test6](https://github.com/TomokiIkegami/Lab_Grapher_TI/blob/main/test6/graph.svg)

![test7](https://github.com/TomokiIkegami/Lab_Grapher_TI/blob/main/test7/graph.svg)