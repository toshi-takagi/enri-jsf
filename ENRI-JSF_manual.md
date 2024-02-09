
# ENRIでの電離圏勾配観測データ解析作業の手順 

## ０．準備

・作業ディレクトリの確認（Vietnam or IND) 
```
enri/analysis/{Vietnam,IND} 
enri/analysis/sfcbca/
enri/analysis/enri-jsf/    (解析用スクリプト）
enri/data/{Hanoi,Bandung,common}
```

・出力先　results/　の作成
```
mkdir -p results/{grad2d,output,sigma_vig,stec,figs}/figs
```

・以下の設定をgrep で確認して各ファイルを設定
```
data_dir =
nav_dir =
sfcbca_bin =
cal_stec =
```

・各スクリプトにある日付範囲設定を確認して設定
```
$ grep start_date *py
$ grep end_date *py
```

・速度、サイズ測定用のスクリプトでSite設定の確認
```
plot_aatr_vel.py plot_aatr_vel_jsf.py plot_aatr_vel_fig.py plot_aatr_size.py
```
以下の箇所を変更する。
```
#site = ['pht2','vas2','hust']
site = ['IDN4','IDN3','IDN1']
```


## １．stec プロット作成
```
$ python3 auto_stec.py  
$ python3 auto_plot_aatr.py 
```

## ２．時系列プロット確認

ファイルの例：
```
./results/stec/Hanoi20220927.png　
./results/stec/IDN20220927.png
```

・擾乱日と静穏日のリスト作成

プロットを見ながら judgeScript.py　スクリプトで記録していく。
- イメージの表示と結果の記録
```
$ python3 judgeScript.py  （入力ファイル[*.png]はスクリプト内で指定すること）
　-> status.txt
```

半日単位に判断。昼夜程度（day/night)で区分する。プロットのウィンドウで、以下を入力する。
```
d = day disturbance
n = night disturbance
q = quiet
x = bad data
e = end session  
```
結果は、`status.txt`に出力される。



## ３．2次元勾配計算
```
$ python3 auto_sfcbca.py 0 1
$ python3 auto_sfcbca.py 1 2
$ python3 auto_sfcbca.py 2 0
 -> results/output/*.grad 

$ python3 auto_plot_sfcbca.py 
 -> results/output/figs/IDN3IDN420221001000000.png 他

$ python3 auto_csum.py 
 -> results/sigma_vig/20220928000000csum.out　他
　→　cyclic_csum.pyはpython2で実行されている。GCPではそのためにエラー発生　
```

この出力ファイルには資料では14列のデータがあることになっているが、
実際には11列しかない。2022/4/8に新しく追加された列がない。<br> 
　→　現行バージョンで問題ない

## ４．CDF計算
```
$ python3 auto_cdf.py > auto_cdf.output.txt 2>&1 
$ python3 auto_cdf.py |tee auto_cdf.output.txt 
 -> results/sigma_vig/2022****000000cdf.out 
```

標準出力をリダイレクトで出力すると
print(コマンド)とos.systemの出力が分かれてしまい、どの日付の
値か分からなくなる。但し、解析では使わない出力なので気にする必要はなし。

・後段処理のために、静穏日・擾乱日のリスト作成　
```
$ python3 makeQuietList.py 　（入力ファイルは status.txt）
 -> quiet_list.txt 　(**cdf.outファイルのリスト）
 -> disturb_list.txt (YYYYMMDDのリスト）
```

・CDFプロット <br> 
```
<<<InflationFactorを調整して適正値を決定する>>>
$ python3 python/plot_cdf_tot.py 1.2 quiet_list.txt

Mean           : 0.087859 [mm/km]
Std. (Raw)     : 1.687723 [mm/km]
Std (Inflated).: 2.531584 [mm/km]
 -> ./20210319_cdf_tot.png （ファイル名はplot_cdf_tot.py中に記載あり）
```

## ５.　速度の測定

・csum.outのリスト作成
```
$ find results/sigma_vig/*csum.out > flist_csum
```

・grad2ファイルの作成
```
$ python3 auto_plot_grad2.py flist_csum
 -> results/grad2d/grad2d_20220927000000.txt 他
```

・`flist_csum`ファイルから日付を読み込み、grad2dファイルで最大勾配が大きいPRNについて速度測定用のプロットを作成
```
$ python3 batch_plot_aatr_vel_fig.py　（refposFileを場所に合わせてスクリプト冒頭で指定）
 -> results/figs/output_aatr_vel_20221006-20.png 他
```


・速度測定に使えるデータの選定

プロットを見ながら judgeVelScript.py　スクリプトで記録していく。イメージの表示と結果の記録を実行。
```
$ python3 judgeVelScript.py  （入力ファイル[*.png]はスクリプト内で指定）
　-> status_vel.txt
```

Good or Bad をプロットのウィンドウで判断し、以下を入力する。
```
g = good data
b = bad data
e = end session  
```
結果は、`status_vel.txt`に出力される。


・擾乱日のリストから日付を読み込み、最大勾配が大きいPRNについてjudgeVelScript.pyでプロット
を確認した結果（status_vel.txt）を読み込み、Goodとある場合について速度を測定する。
```
$ python3 batch_plot_aatr_vel.py　　（refposFileを場所に合わせてスクリプト冒頭で指定）
 -> velocity_dict.pkl に速度の測定結果の辞書をバイナリで保存
```

辞書の例：
```
{'20221004-27': {'cmd': ['python3', 'python/plot_aatr_vel_jsf.py', '20221004', 'refpos_Hanoi2.dat', '27', '12.543888888888889', '12.743888888888888'], 'V': '138.899076', 'Angle': '-5.844579'}, '20221004-1': {'cmd': ['python3', 'python/plot_aatr_vel_jsf.py', '20221004', 'refpos_Hanoi2.dat', '1', '15.763611111171612', '15.96361111117161'], 'V': '173.346284', 'Angle': '-9.994422'}}
```
速度測定ができない場合は空の速度情報が入る。

### メモ
最大勾配の大きさだけでは、速度測定ができない場合が多く作業効率が悪い。
効率をあげる方法はないか？ <br> 
 　→　stecの絶対値を見ると選別できるかもしれない。1000以上のものはダメ
　　`plot_aatr_vel.py: plot(t3,stec3*tec2delay,label=site[site_id[2]])`　を見る <br>
　　→　stec2の値を調べる前に計算時間がかかっているのであまり効率が上がらない <br>
　→　プロットを見て結果を記録することにした（judgeVelScript.py)

## ６．サイズの測定
```
$ python3 batch_plot_aatr_size.py
 -> size_dict.pkl にサイズの測定結果の辞書をバイナリで保存
```

辞書の例：
```
result_dict: {'20221004-1': {'cmd': ['python3', 'python/plot_aatr_size.py', '20221004', 'refpos_Hanoi2.dat', '1', '15.763611111171612', '15.96361111117161', '172.720835', '-11.703966'], 'size': {'pht2': 144176.504047, 'vas2': 136952.331942, 'hust': 145173.096192}}, '20221004-27': {'cmd': ['python3', 'python/plot_aatr_size.py', '20221004', 'refpos_Hanoi2.dat', '27', '12.543888888888889', '12.743888888888888', '141.457992', '-8.126086'], 'size': {'pht2': 47084.380292, 'vas2': 44045.276995, 'hust': 46808.225723}}}
```

#### バッチ処理用
```
python3 auto_stec.py  
python3 auto_plot_aatr.py
python3 auto_sfcbca.py 0 1
python3 auto_sfcbca.py 1 2
python3 auto_sfcbca.py 2 0
python3 auto_plot_sfcbca.py
python3 auto_csum.py
python3 auto_cdf.py > auto_cdf.output.txt 2>&1
find results/sigma_vig/*csum.out > flist_csum
python3 auto_plot_grad2.py flist_csum
python3 batch_plot_aatr_vel_fig.py
```
この処理を行うためのスクリプトが、`initBatch.sh`になっている。

・速度測定に必要なファイルをまとめる
```
tar cvfz forVel.tgz  python/coord_trans.py ./*txt results/stec/*.stec results/*/*png results/*/*/*png results/grad2d/*txt results/sigma_vig/*csum.out 
```

### 補足：

・スライドショーでプロットを見る
```
$ python3 slideshow.py 
　（results/stec/Hanoi*.pngを開くようにslideshow.pyを修正すること）
```

・結果を記録していく
```
$ python3 judgeByDate.py <出力ファイル(Hanoi_Status.txt)>
```

#### Google Compute Portal のVMを使う 
・Compute Engineサービスで、VMインスタンスを作成 <br>

・SSH公開鍵を追加 <br>
　https://cloud.google.com/compute/docs/connect/add-ssh-keys?hl=ja&cloudshell=true#metadata
　「プロジェクト メタデータに SSH 認証鍵を追加する」で[メタデータ]ページに移動して
　　public-key username 
   をboxに記入して追加した。
   
・各種インストール
```
  126  sudo apt install python3-pip
  139  sudo apt install x11-apps
  133  pip3 install Pillow
  121  sudo apt-get install python3-tk
```

・VNCを入れてみる
```
  128  sudo apt-get install xfce4 xfce4-goodies
  129  sudo apt-get install tightvncserver
  193  tightvncserver :1 -geometry 1680x980 
  192  vncserver -kill :1
```

GCPコンソールでファイアウォールを設定（5901）を開けた
　→　VNC viewerで接続できた。しかしterminalがどうしても開かない
　→　Alt+F2 でLauncherが出てきたので、terminalを起動できた

・github
```
takagits@jsfnow10p245:~/work/enri/analysis/jsf$ 
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/toshi-takagi/enri-jsf.git
git push -u origin master

git clone https://github.com/toshi-takagi/enri-jsf.git

```

