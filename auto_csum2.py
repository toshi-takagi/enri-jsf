# coding: utf-8
#### auto_csum.py edited for Ubuntu by M.Nakamura 20201221
#### based on ~/programs/py_mac/auto_csum.py edited by M.Nakamura 20191224
import datetime as dt
import sys
import os
from numpy import *
from pylab import *
#from coord_trans import *


#############################################################################################
### difinitions of environment-dependent variables（スクリプト、プログラム、データの場所定義）
#############################################################################################
python_str="/home/gbas/anaconda3/bin/python "
script_place="/home/iono/analysis/Vietnam/python/"
grad_dir="/home/iono/analysis/Vietnam/results/output/"
vsigma_dir =('/home/iono/analysis/Vietnam/results/sigma_vig/')
#site_codes = ['VAS2','HUST','PHU2']
#refpos_file = 'refpos_Hanoi_for_sigma2.dat'
# by DOY 321, 2023 (2023/11/17)
#site_codes = ['VAS2','HUST','PHU2']
#refpos_file = 'refpos_Hanoi_HUST.dat'
# after DOY 342, 2023 (2023/12/9)
site_codes = ['VAS2','HUS2','PHU2']
refpos_file = 'refpos_Hanoi_HUS2.dat'
#### end of environment-dependent variable difinitions
#############################################################################################
cyclic_sum_str=(script_place + "cyclic_sum.py ")

station='Hanoi'

data_dir=(grad_dir)
out_dir =(vsigma_dir)

st1=site_codes[0]
st2=site_codes[1]
st3=site_codes[2]

stime0 = 0
#etime0 = 90000
etime0 = 240000
#start_date = dt.datetime(2015,4,1)
#end_date = dt.datetime(2015,12,31)
#start_date = dt.datetime(2021,2,1)
#end_date = dt.datetime(2021,2,17) #

start_date = dt.datetime(2023,12,9)
end_date = dt.datetime(2024,2,28)

ndays = (end_date-start_date).days+1


##############################
#### [o] refpos fileの書き出し
# refpos_file = 'refpos_' + station + '.dat'
# fid1 = open(refpos_file,'w')

# ######################################
# ###### [o] st1,st2, st3 の座標取得
# ######################################
# ## [1] "bnx_DEG.txt" を読込
# st_list=loadtxt('/home/gbas/1_analysis/sfcbca/map/bnx_DEG.txt',comments='%',delimiter=' ')### ENRI保有200点のリスト
# ## [2] st1, st2 の緯度経度 degで取り出して
# list_of_st_list=list(st_list[:,0])
# #st1_id=find(st_list[:,0] == int(st1))
# #st1_id=st1_id[0]
# st1_id=[i for i, x in enumerate(list_of_st_list) if int(x)==int(st1)]
# st1_lat=st_list[st1_id,1]
# st1_lon=st_list[st1_id,2]
# st1_alt=st_list[st1_id,3]
# #st2_id=find(st_list[:,0] == int(st2))
# st2_id=[i for i, x in enumerate(list_of_st_list) if int(x)==int(st2)]
# st2_id=st2_id[0]
# st2_lat=st_list[st2_id,1]
# st2_lon=st_list[st2_id,2]
# st2_alt=st_list[st2_id,3]
# #st3_id=find(st_list[:,0] == int(st3))
# st3_id=[i for i, x in enumerate(list_of_st_list) if int(x)==int(st3)]
# st3_id=st3_id[0]
# st3_lat=st_list[st3_id,1]
# st3_lon=st_list[st3_id,2]
# st3_alt=st_list[st3_id,3]

# outstr = '%f %f %f\n%f %f %f\n%f %f %f\n' %(st1_lat,st1_lon,st1_alt,st2_lat,st2_lon,st2_alt,st3_lat,st3_lon,st3_alt)
# fid1.write(outstr)

# fid1.close()

# ######## refpos fileの書き出し
# ##############################

#csum_th = 0.1
csum_th = 0.2

for ii in range(ndays):
 date0 = start_date + dt.timedelta(days=ii)
 yr0 = date0.year
 mon0 = date0.month
 day0 = date0.day

# fname1 = os.path.join(data_dir,'%s%s%4.4d%2.2d%2.2d%2.2d0000.grad' %(site_codes[0],site_codes[1],yr0,mon0,day0,stime0))
# fname2 = os.path.join(data_dir,'%s%s%4.4d%2.2d%2.2d%2.2d0000.grad' %(site_codes[1],site_codes[2],yr0,mon0,day0,stime0))
# fname3 = os.path.join(data_dir,'%s%s%4.4d%2.2d%2.2d%2.2d0000.grad' %(site_codes[2],site_codes[0],yr0,mon0,day0,stime0))
 
 fname1 = os.path.join(data_dir,'%s%s%4.4d%2.2d%2.2d%2.2d0000.grad' %(site_codes[1],site_codes[0],yr0,mon0,day0,stime0))
 fname2 = os.path.join(data_dir,'%s%s%4.4d%2.2d%2.2d%2.2d0000.grad' %(site_codes[2],site_codes[1],yr0,mon0,day0,stime0))
 fname3 = os.path.join(data_dir,'%s%s%4.4d%2.2d%2.2d%2.2d0000.grad' %(site_codes[0],site_codes[2],yr0,mon0,day0,stime0))

 # fname1 = os.path.join(data_dir,'%s_%s_%s_%4.4d%2.2d%2.2d%2.2d0000_%4.4d%2.2d%2.2d235900.grad' %(station,site_codes[0],site_codes[1],yr0,mon0,day0,stime0,yr0,mon0,day0))
 # fname2 = os.path.join(data_dir,'%s_%s_%s_%4.4d%2.2d%2.2d%2.2d0000_%4.4d%2.2d%2.2d235900.grad' %(station,site_codes[1],site_codes[2],yr0,mon0,day0,stime0,yr0,mon0,day0))
 # fname3 = os.path.join(data_dir,'%s_%s_%s_%4.4d%2.2d%2.2d%2.2d0000_%4.4d%2.2d%2.2d235900.grad' %(station,site_codes[2],site_codes[0],yr0,mon0,day0,stime0,yr0,mon0,day0))

# com_csum = 'python cyclic_sum.py %s %s %s %f %s' %(fname1,fname2,fname3,csum_th,refpos_file)
 com_csum = 'python %s %s %s %s %f %s' %(cyclic_sum_str,fname1,fname2,fname3,csum_th,refpos_file)
 print(com_csum)
 os.system(com_csum)
# csum_fname = os.path.join(out_dir,'%4.4d%2.2d%2.2d%2.2d0000csum.out' %(yr0,mon0,day0,stime0))
# com_copy = 'cp csum_check.out %s' %(csum_fname)
# print(com_copy)
# os.system(com_copy)

