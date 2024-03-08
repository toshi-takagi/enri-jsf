#!/home/gbas/anaconda3/bin/python
# coding: utf-8
### auto_plot_aatr.py

from numpy import *
from pylab import *
import os
import datetime as dt

### Edit Here ###
start_date = dt.datetime(2023,12,9)
end_date = dt.datetime(2024,2,28)

out_dir = './results/stec'
fig_dir = './results/stec'

 
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

data_dir = '/data/iono/Hanoi/'
nav_dir = '/data/iono/common/brdc/'

#data_dir = '/home/iono/mnt2/iono_data_net/Hanoi/'
#nav_dir = '/home/iono/mnt2/iono_data_net/Hanoi/'

save_to_fig = 0 # Display figures on screen
save_to_fig = 1 # Save figures
###

ndays = (end_date-start_date).days+1
nsites = len(site_names)

t_samp = 1.0

t_int = 60 # average AATR over t_int seconds

n_int = int(t_int/t_samp)

fig1 = figure(figsize=(6,7),dpi=100)
for ii in range(ndays):
 date0 = start_date + dt.timedelta(days=ii)
 date = date0.year*10000 + date0.month*100 + date0.day

 yr0 = int(date/10000)
 mon0 = int((date % 10000)/100)
 day0 = int(date % 100)
 doy0 = dt.datetime(yr0,mon0,day0).timetuple().tm_yday
 yr02 = yr0 % 100 

# fname_fig = os.path.join(fig_dir,'Bangkok%4.4d%2.2d%2.2d.png' %(yr0,mon0,day0))
 fname_fig = os.path.join(fig_dir,'Hanoi%4.4d%2.2d%2.2d.png' %(yr0,mon0,day0))
 print(fname_fig)

 fig1.clear()
 for jj in range(0,nsites):
  fname_stec = os.path.join(out_dir,'%s%4.4d%2.2d%2.2d.stec' %(site_names[jj],yr0,mon0,day0))
  if os.path.exists(fname_stec) == False:
   fname_stec_exist = 0
  else:
   if os.path.getsize(fname_stec) == 0:
    fname_stec_exist = 0
   else:
    fname_stec_exist = 1

  sp0 = subplot(nsites,1,jj+1)
  if fname_stec_exist == 1:
   d = loadtxt(fname_stec)
   for kk in range(1,33):
    id = where(d[:,1] == kk)[0]
    if len(id) > 0:
     t = d[id,0]
     a = d[id,8]
     id1 = where((t % t_int) == 0)[0]
     if len(id1) > 0:
      t1 = zeros(len(id1))
      a1 = zeros(len(id1))
      count = 0
      for tt in range(0,len(id1)):
       id_int = where((t >= t[id1[tt]]) & (t < (t[id1[tt]] + t_int)))[0]
       if len(id_int) == n_int:
        t1[count] = (t[id1[tt]] % 86400)/3600.0
        a1[count] = a[id_int].mean()
        count = count + 1
      t1 = t1[0:count]
      a1 = a1[0:count]
      plot(t1,a1,'.',color='#1f77b4')
  xlim(0,24)
  ylim(-0.1,0.1)
  text(0.9,0.8,site_names2[jj],transform=sp0.transAxes)
  if jj == 0:
   title('%4.4d-%2.2d-%2.2d' %(yr0,mon0,day0))
   title(date0.isoformat()[0:10])
  if jj == nsites-1:
   ylabel('AATR [TECU/sec]')
   xlabel('GPST [Hour]')
   if save_to_fig == 0:
    show()
   else:
    savefig(fname_fig)




