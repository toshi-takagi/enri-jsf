# -*- coding: utf-8 -*-
#!/home/gbas/anaconda3/bin/python


import datetime as dt
import sys
import os
from numpy import *
import glob
from pylab import *

### Edit Here ###
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

data_dir = '/data/iono/Hanoi/'
nav_dir = '/data/iono/common/brdc/'

cal_stec = '/home/iono/analysis/sfcbca/src/cal_stec_aatr'

out_dir = './results/stec'
fig_dir = './results/stec'
###

ndays = (end_date-start_date).days+1

el_mask = 30.0
print(ndays)
pos = loadtxt(refpos_file)

nsites = len(site_names)

for ii in range(ndays):
 date0 = start_date + dt.timedelta(days=ii)
 date = date0.year*10000 + date0.month*100 + date0.day

 yr0 = int(date/10000)
 mon0 = int((date % 10000)/100)
 day0 = int(date % 100)
 doy0 = dt.datetime(yr0,mon0,day0).timetuple().tm_yday
 yr02 = yr0 % 100

 vast_str='vast'
 
 for jj in range(0,nsites):
  lat0 = pos[jj,0]
  lon0 = pos[jj,1]
  alt0 = pos[jj,2]
  fname_o = os.path.join(data_dir,site_names2[jj],'rinex','%s%3.3d0.%2.2do' %(site_names[jj],doy0,yr02))
  fname_o2 = os.path.join(data_dir,site_names2[jj],'rinex','%s%3.3d0.%2.2do' %(site_names[jj],doy0,yr02))
#  fname_n = os.path.join(data_dir,site_names2[jj],'rinex','%s%3.3d0.%2.2dn' %(site_names[jj],doy0,yr02))
#  fname_n = os.path.join(data_dir,'VAST','nav','%s%3.3d0.%2.2dn' %(vast_str,doy0,yr02))
  fname_n = os.path.join(nav_dir,'%4.4d' %(yr0),'brdc%3.3d0.%2.2dn' %(doy0,yr02))
  fname_stec = os.path.join(out_dir,'%s%4.4d%2.2d%2.2d.stec' %(site_names[jj],yr0,mon0,day0))
  fname_fig = os.path.join(fig_dir,'%s%4.4d%2.2d%2.2d.png' %(site_names[jj],yr0,mon0,day0))

  print(fname_o)
  print(fname_o2)

  if os.path.exists(fname_o) == False:
   if os.path.exists(fname_o2) == True:
    fname_o = fname_o2
  if os.path.exists(fname_o):
   com_cal_stec = '%s -o %s -n %s -e %f -l %f -g %f -a %f -s 1 > %s' %(cal_stec,fname_o,fname_n,el_mask,lat0,lon0,alt0,fname_stec)
   print(com_cal_stec)
   os.system(com_cal_stec)

   if os.path.getsize(fname_stec) > 0:
    d = loadtxt(fname_stec)
    id = where(d[:,8] != 0.0)[0]
    t = (d[id,0] % 86400)/3600.0
    fig1=figure()
    plot(t,d[id,8],'.')
    xlim(0,24)
    ylim(-1,1)
    title('%s %4.4d-%2.2d-%2.2d' %(site_names2[jj],yr0,mon0,day0))
    xlabel('GPST [Hour]')
    ylabel('AATR [TECU/sec]')
    savefig(fname_fig)
    close(fig1)



