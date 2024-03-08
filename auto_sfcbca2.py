#!/home/gbas/anaconda3/bin/python
# coding: utf-8
### auto_sfcbca.py

import datetime as dt
import sys
import os
import param_gen as pg
from numpy import *

bas_rov = [1,0]
if len(sys.argv) < 3:
 bas_rov[0] = int(input('Base (0,1,2)?: '))
 bas_rov[1] = int(input('Rover (0,1,2)?: '))
else:
 bas_rov[0] = int(sys.argv[1])
 bas_rov[1] = int(sys.argv[2])

## Edit Here
stime0 = 0
#etime0 = 90000
etime0 = 240000

start_date = dt.datetime(2023,12,9)
end_date = dt.datetime(2024,2,28)

# by DOY 321, 2023 (2023/11/17)
#refpos_file = 'refpos_Hanoi_HUST.dat'
#site_names = ['vas2','hust','pht2']
#site_names2 = ['VAS2','HUST','PHU2']
#site_codes = ['VAS2','HUST','PHU2']

# after DOY 342, 2023 (2023/12/9)
refpos_file = 'refpos_Hanoi_HUS2.dat'
site_names = ['vas2','hus2','pht2']
site_names2 = ['VAS2','HUS2','PHU2']
site_codes = ['VAS2','HUS2','PHU2']

pos_info = loadtxt(refpos_file)

clock_types = [0,0,0]

data_dir = '/data/iono/Hanoi/'
nav_dir = '/data/iono/common/brdc/'

sfcbca_bin = '/home/iono/analysis/sfcbca/src/sfcbca'
out_dir = './results/output'
###

ndays = (end_date-start_date).days+1


el_mask = 10.0
cn0_mask = 38.0
total_press = 1012.0
part_humid = 0.5
temperature = 300.0
sig2b =  0.02696265536210453
sig2b2 = 0.07096286454050198
a_iono = 0.02
sig2_viono = 0.000001
sig2_amb = 0.00000001
sig2_n_adr = 0.000009
sig2_n_psr = 1.5
shell_h = 350.0
n_cand = 2
ratio_th = 2.0
clock_model = 1
ref_sat_el_th = 45.0
max_gap_time_iono = 60.0
param_file_suffix = ''
param_file_suffix = '_test'

for ii in range(ndays):
 date0 = start_date + dt.timedelta(days=ii)
 date = date0.year*10000 + date0.month*100 + date0.day
 print(date0)

 stime = date*1000000+stime0
 etime = date*1000000+etime0

 yr0 = int(date/10000)
 mon0 = int((date % 10000)/100)
 day0 = int(date % 100)
 doy0 = dt.datetime(yr0,mon0,day0).timetuple().tm_yday
 yr02 = yr0 % 100

 data_file_bas = os.path.join(data_dir,'%s' %(site_names2[bas_rov[0]]),'rinex','%s%3.3d0.%2.2do' %(site_names[bas_rov[0]],doy0,yr02))
 data_file_rov = os.path.join(data_dir,'%s' %(site_names2[bas_rov[1]]),'rinex','%s%3.3d0.%2.2do' %(site_names[bas_rov[1]],doy0,yr02))
# nav_file = os.path.join(nav_dir,'%s' %(site_names2[bas_rov[0]]),'rinex','%s%3.3d0.%2.2dn' %(site_names[bas_rov[0]],doy0,yr02))
 nav_file = os.path.join(nav_dir,'%4.4d' %(yr0),'brdc%3.3d0.%2.2dn' %(doy0,yr02))

 if ((os.path.exists(data_file_bas)) & (os.path.exists(data_file_rov))):
  bas = pg.site_info(pos_info[bas_rov[0],:],site_names[bas_rov[0]],site_codes[bas_rov[0]],clock_types[bas_rov[0]],data_file_bas)
  rov = pg.site_info(pos_info[bas_rov[1],:],site_names[bas_rov[1]],site_codes[bas_rov[1]],clock_types[bas_rov[1]],data_file_rov)

  gen = pg.gen_info(date,stime,etime,nav_file,out_dir,el_mask,cn0_mask,total_press,part_humid,temperature,sig2b,sig2b2,a_iono,sig2_viono,sig2_amb,sig2_n_adr,sig2_n_psr,shell_h,n_cand,ratio_th,clock_model,ref_sat_el_th,max_gap_time_iono,param_file_suffix)

  fname_param = pg.param_gen(rov,bas,gen)

  print('%s -p %s  2> /dev/null' %(sfcbca_bin,fname_param))
  os.system('%s -p %s  2> /dev/null' %(sfcbca_bin,fname_param))
 else:
  if os.path.exists(data_file_bas) == False:
   print('%s not exists' %(data_file_bas))
  if os.path.exists(data_file_rov) == False:
   print('%s not exists' %(data_file_rov))

