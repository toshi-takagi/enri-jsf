
# ENRIでの電離圏勾配観測データ解析作業の手順 

## ０．準備

・作業ディレクトリの確認（Vietnam or IND) 
enri/analysis/{Vietnam,IND} 
enri/analysis/sfcbca/
enri/analysis/jsf/    (解析用スクリプト）
enri/data/{Hanoi,Bandung,common}

・出力先　results/　の作成
mkdir -p results/{grad2d,output,sigma_vig,stec}/figs


・以下の設定をgrep で確認して各ファイルを設定
data_dir
nav_dir
sfcbca_bin
cal_stec 


## １．stec プロット作成

$ python3 auto_stec.py  
$ python3 auto_plot_aatr.py 


## ２．時系列プロット確認

ファイルの例：

./results/stec/Hanoi20220927.png　
./results/stec/IDN20220927.png


・擾乱日と静穏日のリスト作成

プロットを見ながら judgeScript.py　スクリプトで記録していく。
（要確認）
半日単位に判断。昼夜程度（day/night)で区分するのでよいか？

- イメージの表示と結果の記録
$ python3 judgeScript.py 
　-> status.txt
　（入力ファイルはスクリプト内で指定すること） 


## ３．2次元勾配計算

$ python3 auto_sfcbca.py 0 1
$ python3 auto_sfcbca.py 1 2
$ python3 auto_sfcbca.py 2 0
 -> results/output/*.grad 

$ python3 auto_plot_sfcbca.py 
 -> results/output/figs/IDN3IDN420221001000000.png 他

$ python3 auto_csum.py 
 -> results/sigma_vig/20220928000000csum.out　他
　→　cyclic_csum.pyはpython2で実行されている。GCPではそのためにエラー発生　

（要確認）
この出力ファイルには資料では14列のデータがあることになっているが、
実際には11列しかない。2022/4/8に新しく追加された列がない。
　→　現行バージョンで問題ない

## ４．CDF計算

$ python3 auto_cdf.py > auto_cdf.output.txt 2>&1 
$ python3 auto_cdf.py |tee auto_cdf.output.txt 
 -> results/sigma_vig/2022****000000cdf.out 

（要確認）
標準出力を保存する必要があるか？リダイレクトで出力すると
print(コマンド)とos.systemの出力が分かれてしまい、どの日付の
値か分からなくなる。

静穏日・擾乱日のリスト作成（入力ファイル設定）
$ python3 makeQuietList.py 
 -> quiet_list.txt 　(**cdf.outファイルのリスト）
 -> disturb_list.txt (YYYYMMDDのリスト）

CDFプロット
<<<InflationFactorを調整して適正値を決定する>>>
$ python3 python/plot_cdf_tot.py 1.2 quiet_list.txt

Mean           : 0.087859 [mm/km]
Std. (Raw)     : 1.687723 [mm/km]
Std (Inflated).: 2.531584 [mm/km]

 -> ./20210319_cdf_tot.png （ファイル名はplot_cdf_tot.py中に記載あり）


## ５.　速度の測定

・csum.outのリスト作成
$ find results/sigma_vig/*csum.out > flist_csum

・grad2ファイルの作成
$ python3 auto_plot_grad2.py flist_csum
 -> results/grad2d/grad2d_20220927000000.txt 他


・擾乱日のリストから日付を読み込み、最大勾配が大きいPRNについて速度を測定する。

$ python3 batch_plot_aatr_vel.py
 -> velocity_dict.pkl に速度の測定結果の辞書をバイナリで保存

{'20221004-1': {'Date': '20221004', 'PRN': '1', 'MaxGrad': '130.446344', 'max_id2_str': '1848.000000', 'id2_time': '57109.00000021780', 'cmd': ['python3', 'python/plot_aatr_vel.py', '20221004', 'refpos_Hanoi2.dat', '1', '15.763611111171612', '15.96361111117161'], 'V': '172.720835', 'Angle': '-11.703966'}, '20221004-27': {'Date': '20221004', 'PRN': '27', 'MaxGrad': '130.756007', 'max_id2_str': '513609.000000', 'id2_time': '45518.0000000', 'V': '140.321086', 'Angle': '-7.653290'}}


・確認用の図だけ出力するため、python/plot_aatr_vel_fig.pyを新たに作成した。
$ python3 batch_plot_aatr_vel_fig.py
 -> output_aatr_vel_20221005-27.png 他

（要確認）
最大勾配の大きさだけでは、速度測定ができない場合が多く作業効率が悪い。
効率をあげる方法はないか？
　→　stecの絶対値を見ると選別できるかもしれない。1000以上のものはダメ
　　plot_aatr_vel.py: plot(t3,stec3*tec2delay,label=site[site_id[2]])　を見る
　　→　stec2の値を調べる前に計算時間がかかっているのであまり効率が上がらない


６．サイズの測定

$ python3 batch_plot_aatr_size.py
 -> size_dict.pkl にサイズの測定結果の辞書をバイナリで保存

result_dict: {'20221004-1': {'cmd': ['python3', 'python/plot_aatr_size.py', '20221004', 'refpos_Hanoi2.dat', '1', '15.763611111171612', '15.96361111117161', '172.720835', '-11.703966'], 'size': {'pht2': 144176.504047, 'vas2': 136952.331942, 'hust': 145173.096192}}, '20221004-27': {'cmd': ['python3', 'python/plot_aatr_size.py', '20221004', 'refpos_Hanoi2.dat', '27', '12.543888888888889', '12.743888888888888', '141.457992', '-8.126086'], 'size': {'pht2': 47084.380292, 'vas2': 44045.276995, 'hust': 46808.225723}}}

（要確認）
結果はPythonの辞書を保存したバイナリファイルでも良いか？
　→ pickleの古いバージョンで保存してほしい。protocol=2  で指定

データ取得予定
2月19日の週
次回2月28日14時



●　補足：

- スライドショーでプロットを見る
$ python3 slideshow.py 
　（results/stec/Hanoi*.pngを開くようにslideshow.pyを修正すること）

- 結果を記録していく
$ python3 judgeByDate.py <出力ファイル(Hanoi_Status.txt)>


<<Google Compute Portal のVMを使う>> 
・Compute Engineサービスで、VMインスタンスを作成
・SSH公開鍵を追加
　https://cloud.google.com/compute/docs/connect/add-ssh-keys?hl=ja&cloudshell=true#metadata
　「プロジェクト メタデータに SSH 認証鍵を追加する」で[メタデータ]ページに移動して
　　public-key username 
   をboxに記入して追加した。
・各種インストール
  126  sudo apt install python3-pip
  139  sudo apt install x11-apps
  133  pip3 install Pillow
  121  sudo apt-get install python3-tk

toshinobu_takagi@toshinobu:~/work$ python3 ./judgeByImageDate.py Hanoi 
　→　originalではWindowが出なかった。tkinterを使うように変更して judgeScript.pyを作成

・VNCを入れてみる
  128  sudo apt-get install xfce4 xfce4-goodies
  129  sudo apt-get install tightvncserver
  193  tightvncserver :1 -localhost no -geometry 1680x980 -alwaysshared -nevershared -clipboard yes -depth 24
  192  vncserver -kill :1
GCPコンソールでファイアウォールを設定（5901）を開けた
　→　VNC viewerで接続できた。しかしterminalがどうしても開かない
　→　Alt+F2 でLauncherが出てきたので、terminalを起動できた


<<github>>
takagits@jsfnow10p245:~/work/enri/analysis/jsf$ 
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/toshi-takagi/enri-jsf.git
git push -u origin master

git clone https://github.com/toshi-takagi/enri-jsf.git

toshi-takagi/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


