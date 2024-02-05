
# ENRI�ł̓d�������z�ϑ��f�[�^��͍�Ƃ̎菇 

## �O�D����

�E��ƃf�B���N�g���̊m�F�iVietnam or IND) 
enri/analysis/{Vietnam,IND} 
enri/analysis/sfcbca/
enri/analysis/jsf/    (��͗p�X�N���v�g�j
enri/data/{Hanoi,Bandung,common}

�E�o�͐�@results/�@�̍쐬
mkdir -p results/{grad2d,output,sigma_vig,stec}/figs


�E�ȉ��̐ݒ��grep �Ŋm�F���Ċe�t�@�C����ݒ�
data_dir
nav_dir
sfcbca_bin
cal_stec 


## �P�Dstec �v���b�g�쐬

$ python3 auto_stec.py  
$ python3 auto_plot_aatr.py 


## �Q�D���n��v���b�g�m�F

�t�@�C���̗�F

./results/stec/Hanoi20220927.png�@
./results/stec/IDN20220927.png


�E����ƐÉ����̃��X�g�쐬

�v���b�g�����Ȃ��� judgeScript.py�@�X�N���v�g�ŋL�^���Ă����B
�i�v�m�F�j
�����P�ʂɔ��f�B������x�iday/night)�ŋ敪����̂ł悢���H

- �C���[�W�̕\���ƌ��ʂ̋L�^
$ python3 judgeScript.py 
�@-> status.txt
�@�i���̓t�@�C���̓X�N���v�g���Ŏw�肷�邱�Ɓj 


## �R�D2�������z�v�Z

$ python3 auto_sfcbca.py 0 1
$ python3 auto_sfcbca.py 1 2
$ python3 auto_sfcbca.py 2 0
 -> results/output/*.grad 

$ python3 auto_plot_sfcbca.py 
 -> results/output/figs/IDN3IDN420221001000000.png ��

$ python3 auto_csum.py 
 -> results/sigma_vig/20220928000000csum.out�@��
�@���@cyclic_csum.py��python2�Ŏ��s����Ă���BGCP�ł͂��̂��߂ɃG���[�����@

�i�v�m�F�j
���̏o�̓t�@�C���ɂ͎����ł�14��̃f�[�^�����邱�ƂɂȂ��Ă��邪�A
���ۂɂ�11�񂵂��Ȃ��B2022/4/8�ɐV�����ǉ����ꂽ�񂪂Ȃ��B
�@���@���s�o�[�W�����Ŗ��Ȃ�

## �S�DCDF�v�Z

$ python3 auto_cdf.py > auto_cdf.output.txt 2>&1 
$ python3 auto_cdf.py |tee auto_cdf.output.txt 
 -> results/sigma_vig/2022****000000cdf.out 

�i�v�m�F�j
�W���o�͂�ۑ�����K�v�����邩�H���_�C���N�g�ŏo�͂����
print(�R�}���h)��os.system�̏o�͂�������Ă��܂��A�ǂ̓��t��
�l��������Ȃ��Ȃ�B

�É����E����̃��X�g�쐬�i���̓t�@�C���ݒ�j
$ python3 makeQuietList.py 
 -> quiet_list.txt �@(**cdf.out�t�@�C���̃��X�g�j
 -> disturb_list.txt (YYYYMMDD�̃��X�g�j

CDF�v���b�g
<<<InflationFactor�𒲐����ēK���l�����肷��>>>
$ python3 python/plot_cdf_tot.py 1.2 quiet_list.txt

Mean           : 0.087859 [mm/km]
Std. (Raw)     : 1.687723 [mm/km]
Std (Inflated).: 2.531584 [mm/km]

 -> ./20210319_cdf_tot.png �i�t�@�C������plot_cdf_tot.py���ɋL�ڂ���j


## �T.�@���x�̑���

�Ecsum.out�̃��X�g�쐬
$ find results/sigma_vig/*csum.out > flist_csum

�Egrad2�t�@�C���̍쐬
$ python3 auto_plot_grad2.py flist_csum
 -> results/grad2d/grad2d_20220927000000.txt ��


�E����̃��X�g������t��ǂݍ��݁A�ő���z���傫��PRN�ɂ��đ��x�𑪒肷��B

$ python3 batch_plot_aatr_vel.py
 -> velocity_dict.pkl �ɑ��x�̑��茋�ʂ̎������o�C�i���ŕۑ�

{'20221004-1': {'Date': '20221004', 'PRN': '1', 'MaxGrad': '130.446344', 'max_id2_str': '1848.000000', 'id2_time': '57109.00000021780', 'cmd': ['python3', 'python/plot_aatr_vel.py', '20221004', 'refpos_Hanoi2.dat', '1', '15.763611111171612', '15.96361111117161'], 'V': '172.720835', 'Angle': '-11.703966'}, '20221004-27': {'Date': '20221004', 'PRN': '27', 'MaxGrad': '130.756007', 'max_id2_str': '513609.000000', 'id2_time': '45518.0000000', 'V': '140.321086', 'Angle': '-7.653290'}}


�E�m�F�p�̐}�����o�͂��邽�߁Apython/plot_aatr_vel_fig.py��V���ɍ쐬�����B
$ python3 batch_plot_aatr_vel_fig.py
 -> output_aatr_vel_20221005-27.png ��

�i�v�m�F�j
�ő���z�̑傫�������ł́A���x���肪�ł��Ȃ��ꍇ��������ƌ����������B
��������������@�͂Ȃ����H
�@���@stec�̐�Βl������ƑI�ʂł��邩������Ȃ��B1000�ȏ�̂��̂̓_��
�@�@plot_aatr_vel.py: plot(t3,stec3*tec2delay,label=site[site_id[2]])�@������
�@�@���@stec2�̒l�𒲂ׂ�O�Ɍv�Z���Ԃ��������Ă���̂ł��܂�������オ��Ȃ�


�U�D�T�C�Y�̑���

$ python3 batch_plot_aatr_size.py
 -> size_dict.pkl �ɃT�C�Y�̑��茋�ʂ̎������o�C�i���ŕۑ�

result_dict: {'20221004-1': {'cmd': ['python3', 'python/plot_aatr_size.py', '20221004', 'refpos_Hanoi2.dat', '1', '15.763611111171612', '15.96361111117161', '172.720835', '-11.703966'], 'size': {'pht2': 144176.504047, 'vas2': 136952.331942, 'hust': 145173.096192}}, '20221004-27': {'cmd': ['python3', 'python/plot_aatr_size.py', '20221004', 'refpos_Hanoi2.dat', '27', '12.543888888888889', '12.743888888888888', '141.457992', '-8.126086'], 'size': {'pht2': 47084.380292, 'vas2': 44045.276995, 'hust': 46808.225723}}}

�i�v�m�F�j
���ʂ�Python�̎�����ۑ������o�C�i���t�@�C���ł��ǂ����H
�@�� pickle�̌Â��o�[�W�����ŕۑ����Ăق����Bprotocol=2  �Ŏw��

�f�[�^�擾�\��
2��19���̏T
����2��28��14��



���@�⑫�F

- �X���C�h�V���[�Ńv���b�g������
$ python3 slideshow.py 
�@�iresults/stec/Hanoi*.png���J���悤��slideshow.py���C�����邱�Ɓj

- ���ʂ��L�^���Ă���
$ python3 judgeByDate.py <�o�̓t�@�C��(Hanoi_Status.txt)>


<<Google Compute Portal ��VM���g��>> 
�ECompute Engine�T�[�r�X�ŁAVM�C���X�^���X���쐬
�ESSH���J����ǉ�
�@https://cloud.google.com/compute/docs/connect/add-ssh-keys?hl=ja&cloudshell=true#metadata
�@�u�v���W�F�N�g ���^�f�[�^�� SSH �F�،���ǉ�����v��[���^�f�[�^]�y�[�W�Ɉړ�����
�@�@public-key username 
   ��box�ɋL�����Ēǉ������B
�E�e��C���X�g�[��
  126  sudo apt install python3-pip
  139  sudo apt install x11-apps
  133  pip3 install Pillow
  121  sudo apt-get install python3-tk

toshinobu_takagi@toshinobu:~/work$ python3 ./judgeByImageDate.py Hanoi 
�@���@original�ł�Window���o�Ȃ������Btkinter���g���悤�ɕύX���� judgeScript.py���쐬

�EVNC�����Ă݂�
  128  sudo apt-get install xfce4 xfce4-goodies
  129  sudo apt-get install tightvncserver
  193  tightvncserver :1 -localhost no -geometry 1680x980 -alwaysshared -nevershared -clipboard yes -depth 24
  192  vncserver -kill :1
GCP�R���\�[���Ńt�@�C�A�E�H�[����ݒ�i5901�j���J����
�@���@VNC viewer�Őڑ��ł����B������terminal���ǂ����Ă��J���Ȃ�
�@���@Alt+F2 ��Launcher���o�Ă����̂ŁAterminal���N���ł���


<<github>>
takagits@jsfnow10p245:~/work/enri/analysis/jsf$ 
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/toshi-takagi/enri-jsf.git
git push -u origin master

git clone https://github.com/toshi-takagi/enri-jsf.git

toshi-takagi/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


