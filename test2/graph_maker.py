# モジュール
import re   # 文字列操作用のモジュール
import pandas as pd # csvからデータフレーム作成用
import matplotlib.pyplot as plt # グラフ描画
import matplotlib.ticker as ptick   # グラフ描画
import pylab    # グラフ描画
import numpy as np  # グラフ描画（軸目盛り作成）

# 関数
## 指定した倍数に丸めてくれる関数（そのまま使わせてもらいました）URL:https://ishi-tech.biz/python-mround/
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
        round_value = value-(value%unit)
    else:
        round_value = value-(value%unit)+unit
    return round_value

## 10の3乗ごとの指数表記を求め、指数の肩を取得する関数
def get_num_exp(max_val):   # max_val:軸の最大絶対値
    # 指数部を選ぶ処理
    max_str="{0:e}".format(max_val) # 値を指数表記の文字列に変換
    size=max_str.split("e",1)[1]    # 仮数部と指数部を分離（▲▲+e◆◆または▲▲-e◆◆。▲▲が仮数部、◆◆が指数部。eは基数が10であることを意味）
    print("軸の最大絶対値の指数表現：",max_str,sep="")  # 元データの最大絶対値を指数表現
    # print(size)
    d1=MROUND(int(size),3)  # d1:3乗ごとに切り上げたときの指数部
    d2=MROUND(int(size),-3) # d2:3乗ごとに切り下げたときの指数部
    # print(d1)
    # print(d2)

    # 元の指数部に近いものをd1,d2から選ぶ処理
    if abs(int(size)-d1)<abs(int(size)-d2):
        # print(d1)
        dt=d1   # dt:選んだ指数部
    else:
        # print(d2)
        dt=d2   # dt:選んだ指数部
    # print(d)
    # print("dt",dt,sep="=")

    final=max_val*10**(-dt) # final:10の3乗ごとで表現したときの仮数部

    #print("final",final)
    final_e="{0}e{1:+}"     # final_e:最終的に求めたい指数表現の定型文（{:+}は数字を符号付き表現で表すという意味。+が省略されない）
    exp_val=final_e.format(final,dt)    # 定型文（final_e）に仮数部と指数部を当てはめて、最終的な指数表現を完成。

    return exp_val,dt   # 指数表現と指数部を返す（関数から出力）

## 指数部に対応した補助単位（ギガ、キロ、ミリ、マイクロなど）を自動で選ぶ関数
def get_aux_unit_label(dt):

    # 補助単位の対応表（辞書型データ）
    aux_unit_dic={
            18:'E',     # エクサ
            15:'P',     # ペタ
            12:'T',     # テラ
            9:'G',      # ギガ
            6:'M',      # メガ
            3:'k',      # キロ
            0:'',       # ※0乗のときは何もつけない
            -3:'m',     # ミリ
            -6:'μ',     # マイクロ
            -9:'n',     # ナノ
            -12:'p',    # ピコ
            -15:'f',    # フェムト
            -18:'a'     # アト
            } 

    # 指数部に対応した補助単位を辞書から自動選択
    aux_unit=aux_unit_dic[dt]
    # A=9
    #print("10の{}乗を表す補助単位は{}です".format(A,aux_unit[A]))
    return aux_unit #補助単位の文字を返す

# フォントの設定
plt.rcParams['font.family']="Times New Roman"   # グラフ全体のフォントを「Times New Roman」に
plt.rcParams['mathtext.fontset']="stix"         # 数式のフォントを「STIX Math」に（Times系の数式フォント）
plt.rcParams["font.size"]=12                    # フォントサイズを12ptに

# グラフサイズの設定（画面に表示されるウィンドウのサイズ、保存されるときのサイズ）
## 1[in]=25.4[mm]
mm=1.0/25.4 # インチをmmに換算する係数
plt.rcParams["figure.figsize"]=(120*mm,70*mm) # 全描画範囲のサイズ指定

# 目盛りの設定
plt.rcParams['xtick.direction']="inout" # 交差
plt.rcParams['ytick.direction']="in" #内向き

# グラフ作成
fig = plt.figure() # fig:グラフ描画の基礎になるオブジェクト
ax = fig.add_subplot()  # ax:グラフカスタマイズ（軸の設定など）に必要なオブジェクト
ax.set_aspect('equal')  # 縦横比を一定に

# データフレームdfをcsvから作成
df=pd.read_csv("data.csv",encoding="shift-jis",index_col=0) # df:データフレーム（Data Frame：pandasの表形式の型）、文字コードはcsvファイルに合わせて設定すれば良い（今回はshift-jisに設定）。
df.plot(ax=ax) #matplotlibと連携

# 軸の設定
## 軸の描画に必要な情報を取得
### 各軸の一番大きな絶対値を取得
x_max=max(ax.get_xlim(),key=abs)
y_max=max(ax.get_ylim(),key=abs)

### 各軸の最大値の指数表記を取得
exp_x,dt_x=get_num_exp(x_max)
exp_y,dt_y=get_num_exp(y_max)

### x軸、y軸の補助単位をそれぞれ取得
aux_unit_x=get_aux_unit_label(dt_x)
aux_unit_y=get_aux_unit_label(dt_y)

## 横軸と縦軸の表示範囲を設定
ax.set_xlim(0,1)   # 必要に応じて最大、最小値を設定
ax.set_ylim(0,1)  # 必要に応じて最大、最小値を設定

## 目盛り間隔設定
# ax.set_xticks(np.arange(0,100,10))  # np.arrange(開始値,終了値,刻み幅)で設定
# ax.set_yticks(np.arange(-50,50,10))  # np.arrange(開始値,終了値,刻み幅)で設定

## 軸ラベルの設定。補助単位は自動で設定。
ax.xaxis.set_major_formatter(ptick.ScalarFormatter(useMathText=True))   # 軸に数式フォーマットが使えるように設定
ax.yaxis.set_major_formatter(ptick.ScalarFormatter(useMathText=True))   # 軸に数式フォーマットが使えるように設定
# ax.ticklabel_format(style="sci",axis="x",scilimits=(-3,-3)) # 10^(-3)固定で表示
# ax.ticklabel_format(style="sci",axis="y",scilimits=(9,9)) # 10^(9)固定で表示
ax.set_xlabel("$x$ [{0}-]".format(aux_unit_x),fontsize=12,fontname="Times New Roman")    # 軸ラベルを英語で入力。$マークに挟まれている範囲は数式が入力可能。ここでもフォントサイズの設定が可能。
ax.set_ylabel("$y$ [{0}-]".format(aux_unit_y),fontsize=12,fontname="Times New Roman") # 軸ラベルを英語で入力。$マークに挟まれている範囲は数式が入力可能。ここでもフォントサイズの設定が可能。

## 軸の値を補助単位に合わせて変更
### 軸設定用のオブジェクト生成
xticks,strs = pylab.xticks()
yticks,strs = pylab.yticks()
### %g → 自動, %d → 整数, 小数点以下2桁 → %.2f, 有効数字2桁 → %#.2g
pylab.xticks(xticks,["%g" % x for x in 10**-dt_x * xticks])
pylab.yticks(yticks,["%g" % x for x in 10**-dt_y * yticks])

# 凡例を追加
labels=["curve"]  # 入力データに合わせて設定
plt.legend(labels,frameon=False,loc="upper left",bbox_to_anchor=(1,1))  # 凡例の位置を右上に、枠線は無し。
plt.tight_layout()  # 凡例や軸ラベルがグラフエリアからはみ出さないように

# グラフの保存と表示
plt.savefig("graph.svg")    # graphという名前でグラフを保存。形式はsvg（拡大しても綺麗）。
plt.show()  # グラフを画面に表示