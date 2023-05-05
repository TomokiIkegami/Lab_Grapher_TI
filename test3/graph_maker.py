# # モジュール
import re   # 文字列操作用のモジュール
import pandas as pd  # csvからデータフレーム作成用
import matplotlib.pyplot as plt  # グラフ描画
import matplotlib.ticker as ptick   # グラフ描画
import pylab    # グラフ描画
import numpy as np  # グラフ描画（軸目盛り作成）

# # 始めに定義する変数など
# ## 補助単位の対応表（辞書型データ）
aux_unit_dic = {
    18: 'E',     # エクサ
    15: 'P',     # ペタ
    12: 'T',     # テラ
    9: 'G',      # ギガ
    6: 'M',      # メガ
    3: 'k',      # キロ
    0: '',       # ※0乗のときは何もつけない
    -3: 'm',     # ミリ
    -6: 'μ',     # マイクロ
    -9: 'n',     # ナノ
    -12: 'p',    # ピコ
    -15: 'f',    # フェムト
    -18: 'a'     # アト
}

# ## 単位の換算係数
mm = 1.0/25.4  # インチをmmに換算する係数 ※ 1[in]=25.4[mm]

# ## マーカー（データの数より多く用意）
point_mk=["^","s","o","x","o","o","o","o","None"]  # マーカーの設定（必要に応じて）

# # 関数
# ## 指定した倍数に丸めてくれる関数（そのまま使わせてもらいました）URL:https://ishi-tech.biz/python-mround/


def MROUND(value, unit):
    """
    目的の倍数に丸められた数値を返す関数。

    Parameters
    ----------
    value : int or float
        丸めの対象となる数値を指定。
    unit : int or float
        数値を丸くする倍数を指定。

    Returns
    -------
    round_value : int or float
    """
    if value < 0:
        value_judge = -value
    else:
        value_judge = value
    if unit < 0:
        unit_judge = -unit
    else:
        unit_judge = unit
    if value_judge == unit_judge or value_judge % unit_judge == 0:
        round_value = value-(value % unit)
    else:
        round_value = value-(value % unit)+unit
    return round_value

# ## 10の3乗ごとの指数表記を求め、指数の肩を取得する関数


def get_num_exp(max_val):   # max_val:軸の最大絶対値
    # 指数部を選ぶ処理
    max_str = "{0:e}".format(max_val)  # 値を指数表記の文字列に変換
    # 仮数部と指数部を分離（▲▲+e##または▲▲-e##。▲▲が仮数部、##が指数部。eは基数が10であることを意味）
    size = max_str.split("e", 1)[1]
    print("軸の最大絶対値の指数表現：", max_str, sep="")  # 元データの最大絶対値を指数表現
    # print(size)
    d1 = MROUND(int(size), 3)  # d1:3乗ごとに切り上げたときの指数部
    d2 = MROUND(int(size), -3)  # d2:3乗ごとに切り下げたときの指数部
    # print(d1)
    # print(d2)

    # 元の指数部に近いものをd1,d2から選ぶ処理
    if abs(int(size)-d1) < abs(int(size)-d2):
        # print(d1)
        dt = d1   # dt:選んだ指数部
    else:
        # print(d2)
        dt = d2   # dt:選んだ指数部
    # print(d)
    # print("dt",dt,sep="=")

    final = max_val*10**(-dt)  # final:10の3乗ごとで表現したときの仮数部

    # print("final",final)
    # final_e:最終的に求めたい指数表現の定型文（{:+}は数字を符号付き表現で表すという意味。+が省略されない）
    final_e = "{0}e{1:+}"
    # 定型文（final_e）に仮数部と指数部を当てはめて、最終的な指数表現を完成。
    exp_val = final_e.format(final, dt)

    return exp_val, dt   # 指数表現と指数部を返す（関数から出力）

# ## 指数部に対応した補助単位（ギガ、キロ、ミリ、マイクロなど）を自動で選ぶ関数


def get_aux_unit_label(dt):
    # 指数部に対応した補助単位を辞書から自動選択
    aux_unit = aux_unit_dic[dt]
    # A=9
    # print("10の{}乗を表す補助単位は{}です".format(A,aux_unit[A]))
    if dt == 0:
        cur = 1   # cur:軸ラベルの単位表記に使うインデックス（cur==1:補助単位がないとき）
    else:
        cur = 2   # cur:軸ラベルの単位表記に使うインデックス（cur==2:補助単位があるとき）
    return aux_unit, cur  # 補助単位の文字と、軸ラベルの単位表記に使うインデックスを取得

# ## 逆順の辞書を作る関数


def inverse_dic(dic):
    return{v: k for k, v in dic.items()}

# ## 補助単位に対応した指数部（10の何乗か）を自動で選ぶ関数


def get_e_aux_unit(axis_unit):
    inv_dic = inverse_dic(aux_unit_dic)   # 逆の辞書を生成
    if not (axis_unit[1] in inv_dic.keys()) == False:
        # e_aux_unit_x:補助単位に対応するx軸の乗数(10の何乗か)
        e_aux_unit = inv_dic[axis_unit[1]]
    else:
        e_aux_unit = 0    # 補助単位がない場合は乗数を0に
    # print(e_aux_unit)   #　乗数（指数部）を表示
    return e_aux_unit  # 補助単位に対応した指数部を出力


# # データフレームdfをcsvから作成
# df:データフレーム（Data Frame：pandasの表形式の型）
df = pd.read_csv("data.csv", encoding="shift-jis") # 文字コードはcsvファイルに合わせて設定すれば良い（今回はshift-jisに設定。Excelからcsvを生成するとshift-jisになるため）。
# print(df)
# # 初期設定
# ## グラフ全体のフォントを「Times New Roman」に
plt.rcParams['font.family'] = "Times New Roman"
# ## 数式のフォントを「STIX Math」に（Times系の数式フォント）
plt.rcParams['mathtext.fontset'] = "stix"
plt.rcParams["font.size"] = 12                    # フォントサイズを12ptに
# ## グラフサイズの設定（画面に表示されるウィンドウのサイズ、保存されるときのサイズ）
plt.rcParams["figure.figsize"] = (120*mm, 70*mm)  # 全描画範囲のサイズ指定
# ## 目盛りの設定
plt.rcParams['xtick.direction'] = "inout"  # 交差
plt.rcParams['ytick.direction'] = "in"  # 内向き
# ## グラフを用意
fig = plt.figure()  # fig:グラフ描画の基礎になるオブジェクト
ax = fig.add_subplot(111)  # ax:グラフカスタマイズ（軸の設定など）に必要なオブジェクト ※311=グラフエリアを3×1マスで区切ったのうちの1番目、つまり一番上
# ax2 = fig.add_subplot(111)  # ax:グラフカスタマイズ（軸の設定など）に必要なオブジェクト 
# ax.set_aspect('equal')  # 縦横比を一定に

# # 補助単位に応じてデータを加工
# ## 1行目の値をすべて表示
# print(df.index.names)   # 横軸のデータ名を表示
# print(df.columns.values)   # 縦軸のデータ名を表示
# ## 軸名、量記号、単位に文字列を分離
x_label = []    # x軸ラベルを入れるリスト
y_label = []    # y軸ラベルを入れるリスト
# ## 横軸
x_label = str(df.columns.values[0]).split(' ')  # 空白で分割
print(x_label)  # 分割結果を表示
# ## 縦軸
for j in range(1,len(df.columns.values[1:])+1):
    y_label.append(str(df.columns.values[j]).split(' '))  # 空白で分割
print(y_label)  # 分割結果を表示

# # 乗数を辞書から取得
# ## x軸の乗数
x_unit = x_label[-1]  # x_unit:x軸の単位
# print(x_label[-1])
# print(x_unit[1])
x_e_aux_unit = get_e_aux_unit(x_unit)  # 補助単位を取得
# print(x_e_aux_unit)  # x軸の乗数を表示

# ## y軸の乗数
y_sig = []    # y軸の量記号を入れる空のリスト
y_unit = []   # y軸の単位を入れる空のリスト
y_e_aux_unit = []  # y軸の指数部を入れる空のリスト
for i in range(len(df.columns.values[1:])):
    y_sig.append(y_label[i][-2])    # 量記号を保存
    y_unit.append(y_label[i][-1])   # 単位を保存
    y_e_aux_unit.append(get_e_aux_unit(y_unit[i]))  # 補助単位を取得
# print(y_e_aux_unit)  # y軸の乗数を表示

# # データを補助単位無しの値に戻す
# 1列目のy軸データの補助単位を全yデータに適用。（y軸の単位はすべてそろったデータを用意する）
# ## x軸
df2=df.copy() # データフレームをコピー（元のデータフレームが変更されないようにするため）
df2.iloc[:,0]*=10**x_e_aux_unit # x軸を補助単位なしの値に変更
# ## y軸
df3=df2.copy()
for i in range(1,len(df.columns.values[1:])+1): # x軸の処理は済ませているので添え字は1から
    df3.iloc[:,i]*=10**y_e_aux_unit[i-1]    # y軸を補助単位なしの値に変更
# print(df3) # 補助単位無しのデータ（表示上の単位は元のまま）
# # 軸の設定
# ## 軸の描画に必要な情報を取得
# ### 各軸の一番大きな絶対値を取得
ana_x=df3[df.columns.values[0]].describe()   # ※ana→analysis。ana_x:x軸を分析した時の各種統計量（最大/最小値、標準偏差、平均など...）
ana_y=[]    # ana_y:y軸を分析した時の各種統計量（最大・最小値、標準偏差、平均など...）
for i in range(1,len(df.columns.values[1:])+1):
    ana_y.append(df3[df.columns.values[i]].describe())  # y軸の統計量を保存
x_max=ana_x[-1] #　x軸の最大値を保存
x_min=ana_x[3]  # y軸の最大値を保存
x_abs_max = max(x_max,x_min,key=abs)    # x軸の最大絶対値を取得
y_max_min=[]    # y軸の全系列の最大・最小値を保存するリスト
for i in range(len(df.columns.values[1:])):
    y_max_min.append(max(ana_y[i][-1],ana_y[i][3],key=abs)) # 最大・最小値を保存
y_abs_max = max(y_max_min,key=abs)  # y軸の最大絶対値を取得
# ### 各軸の最大値の指数表記を取得
exp_x, dt_x = get_num_exp(x_abs_max)
exp_y, dt_y = get_num_exp(y_abs_max)
# ### x軸、y軸の補助単位をそれぞれ取得
aux_unit_x, cur_x = get_aux_unit_label(dt_x)    # aux_unit_x:x軸の補助単位
aux_unit_y, cur_y = get_aux_unit_label(dt_y)    # aux_unit_y:y軸の補助単位
# ### 描画用のデータフレームを生成（補助単位を使った時の仮数部のみのデータを作るため）
df4=df3.copy()  # 補助単位無しのデータフレームをコピー
# ## x軸
df4.iloc[:,0]*=10**(-dt_x)  # 補助単位の倍率を元データにかける（元データが補助単位の分だけ大きくなるか小さくなる）
# ## y軸
for i in range(1,len(df.columns.values[1:])+1):
    df4.iloc[:,i]*=10**(-dt_y) # 補助単位の倍率を元データにかける（元データが補助単位の分だけ大きくなるか小さくなる）
# print("df4",df4)
# ## データフレームとmatplotlibを連携（タイミング重要）
# ### 折れ線描画
# df4.plot(ax=ax,x=df4.columns.values[0],y=df4.columns.values[1:])  # 折れ線だけならこの行をだけ有効に
# print(df4.iloc[:,0].to_list())
# ### 散布図描画
for i in range(len(df.columns.values[1:])):
    df4.plot(ax=ax,x=df4.columns.values[0],y=df4.columns.values[i+1],marker=point_mk[i])   # この行を有効にすると、折れ線とマーカーを同時に生成可能
    # ax.scatter(x=df4.iloc[:,0].to_list(),y=df4.iloc[:,i+1].to_list(),s=20,marker=point_mk[i])  # 散布図のみならこの行をだけ有効に（s:マーカーサイズ、marker:マーカ種類）

print(df4.iloc[:,1].to_list())
# ## 軸の値を補助単位に合わせて変更
# ### 軸設定用のオブジェクト生成
xticks, strs = pylab.xticks()
yticks, strs = pylab.yticks()
# ### 軸の値を変更 [%g → 自動, %d → 整数, 小数点以下2桁 → %.2f, 有効数字2桁 → %#.2g]
# pylab.xticks(xticks, ["%g" % x for x in 10**-dt_x * xticks])
# pylab.yticks(yticks, ["%g" % x for x in 10**-dt_y * yticks])
# ## 横軸と縦軸の表示範囲を設定
# ax.set_xlim(0,1)   # 必要に応じて最大、最小値を設定
# ax.set_ylim(0,1)  # 必要に応じて最大、最小値を設定
# ## 目盛り間隔設定
# ax.set_xticks(np.arange(0,100,10))  # np.arrange(開始値,終了値,刻み幅)で設定
# ax.set_yticks(np.arange(-50,50,10))  # np.arrange(開始値,終了値,刻み幅)で設定

# # 軸ラベルの設定。補助単位は自動で設定。
# ## 軸に数式フォーマットが使えるように設定
ax.xaxis.set_major_formatter(ptick.ScalarFormatter(
    useMathText=True))
ax.yaxis.set_major_formatter(ptick.ScalarFormatter(
    useMathText=True))
# ## 入力データをもとに軸ラベルを自動設定
# ax.ticklabel_format(style="sci",axis="x",scilimits=(-3,-3)) # 10^(-3)固定で表示
# ax.ticklabel_format(style="sci",axis="y",scilimits=(9,9)) # 10^(9)固定で表示
ax.set_xlabel("{0} {1} [{2}{3}".format(x_label[0], x_label[1], aux_unit_x, x_unit[cur_x:]), fontsize=12,
              fontname="Times New Roman")    # 軸ラベルを英語で入力。$マークに挟まれている範囲は数式が入力可能。ここでもフォントサイズの設定が可能。
ax.set_ylabel("{0} {1} [{2}{3}".format(y_label[0][0], y_label[0][1], aux_unit_y, y_unit[0][cur_y:]), fontsize=12,
              fontname="Times New Roman")  # 軸ラベルを英語で入力。$マークに挟まれている範囲は数式が入力可能。ここでもフォントサイズの設定が可能。

# # 凡例を追加
labels = y_sig  # 入力データに合わせて設定。（手動なら labels = ["凡例1","凡例2","凡例3"]）
ax.legend(labels, frameon=False, loc="upper left",
           bbox_to_anchor=(1, 1),)  # 凡例の位置を右上に、枠線は無し。
fig.tight_layout()  # 凡例や軸ラベルがグラフエリアからはみ出さないように

# # グラフの表示と保存
# plt.plot.scatter(x=df4.columns.values[0],y=df4.columns.values[1])
plt.show()
fig.savefig("graph.svg")    # graphという名前でグラフを保存。形式はsvg（拡大しても綺麗）。