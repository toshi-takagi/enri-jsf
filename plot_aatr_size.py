#!/home/gbas/anaconda3/bin/python
from numpy import *
from pylab import *
from coord_trans import *
import sys
import os
import datetime as dt

class click_counter():
 def __init__(self):
  self.c = 0
  self.c1 = 0
  self.x = [0,0]
  self.y = [0,0]
  self.t0 = [0,0]
  self.az = [0,0]
  self.el = [0,0]
 def count_up(self):
  self.c = self.c + 1
  self.c1 = self.c1 + 1
 def reset(self):
  self.c1 = 0
  self.x = [0,0]
  self.y = [0,0]
  self.t0 = [0,0]
  self.az = [0,0]
  self.el = [0,0]
 def full_reset(self):
  self.c = 0
  self.c1 = 0
  self.x = [0,0]
  self.y = [0,0]
  self.t0 = [0,0]
  self.az = [0,0]
  self.el = [0,0]

class delay_tri_data():
 def __init__(self):
  self.xdata = {}
  self.ydata = {}
  self.az = {}
  self.el = {}
 def reset(self):
  self.xdata = {}
  self.ydata = {}
  self.az = {}
  self.el = {}

def onclick(event):
# print 'event.button=%d, event.x=%d, event.y=%d, event.xdata=%f, event.ydata=%f' %(event.button,event.x,event.y,event.xdata,event.ydata)
 c.count_up()
 c.x[c.c1-1] = event.xdata
 c.y[c.c1-1] = event.ydata
 site_id = int((c.c-1)/2)
 ind = where(abs(data_tri.xdata[site_id] - event.xdata) == abs(data_tri.xdata[site_id] - event.xdata).min())[0][0] # there may be the case where pointer at exactly at the middle
 c.t0[c.c1-1] = data_tri.xdata[site_id][ind]
 c.az[c.c1-1] = data_tri.az[site_id][ind]
 c.el[c.c1-1] = data_tri.el[site_id][ind]
 ax5.plot([data_tri.xdata[site_id][ind]],[data_tri.ydata[site_id][ind]],".",color=cols[site_id])
 fig5.canvas.draw()
 print(c.c1)
 if c.c1 == 2:
#  print "Clicked 6 times"
#  print "Mean_x: %f, Mean_y: %f" %(mean(c.x),mean(c.y))
  print('caz = ',c.az)
  cal_csize(c,gg,vv,theta)
 if c.c == 6:
  c.full_reset()
 else:
  if c.c1 % 2 == 0:
   c.reset()

#def oncpaint(event):
## ind = np.searchsorted(data_tri.xdata[c.c-1],event.xdata,side='right')
# ind = where(abs(data_tri.xdata[c.c-1] - event.xdata) == abs(data_tri.xdata[c.c-1] - event.xdata).min())[0][0] # there may be the case where pointer at exactly at the middle
# c.t0[c.c-1] = data_tri.xdata[c.c-1][ind]
# ax5.plot([data_tri.xdata[c.c-1][ind]],[data_tri.ydata[c.c-1][ind]],".",color=cols[c.c-1])
# fig5.canvas.draw()

def onkey(event):
 if event.key == 'q':
  close()
 sys.stdout.flush()

def hr2hms(f):
 h=int(f)
 m=int((f-h)*60)
 s=(f*3600)%60 
 print("%2.2d:%2.2d:%f" %(h,m,s))

def cal_csize(cdata,gg,vv,theta):
 t01 = cdata.t0[0]
 az1 = cdata.az[0]
 el1 = cdata.el[0]
 ipp1 = pierce_point(gg[int((cdata.c-1)/2)],az1,el1,map_alt,10)
 ipp1[2] = ipp1[2]*1e3
 t01_b = cdata.t0[1]
 az1_b = cdata.az[1]
 el1_b = cdata.el[1]
 ipp1_b = pierce_point(gg[int((cdata.c-1)/2)],az1_b,el1_b,map_alt,10)
 ipp1_b[2] = ipp1_b[2]*1e3
 dt_tb = (t01_b-t01)*3600
 x1_b_ecef = gg2ecef(ipp1_b)
 x1_b_x1 = ecef2enu(x1_b_ecef,ipp1)
 x1_t_1_x =(vv*dt_tb*tan(theta)*sin(theta)+vv*dt_tb*cos(theta)+double(x1_b_x1[0])/tan(theta)-double(x1_b_x1[1]))/(1/tan(theta)+tan(theta))
 x1_t_1_y = -tan(theta)*x1_t_1_x+vv*dt_tb*(tan(theta)*sin(theta) + cos(theta))
 d1_b_t = sqrt((x1_t_1_x-double(x1_b_x1[0]))**2 + (x1_t_1_y-double(x1_b_x1[1]))**2)
 print("Scale size (%s) = %f (m)" % (site[int((c.c-1)/2)],d1_b_t))


### main ###
f_L1 = 1.57542e9
tec2delay = 40.3e16/f_L1/f_L1

### Edit Here ###
#data_dir = '.'
data_dir = './results/stec/'
#site = ['kmit','stfd','aero']
# by DOY 321, 2023 (2023/11/17)
site = ['vas2','hust','pht2']
# after DOY 342, 2023 (2023/12/9)
#site = ['vas2','hus2','pht2']
site_id = [0,1,2]
###


#cols = ["blue","green","red"]
cols = ["blue","red","green"]
c = click_counter()

if len(sys.argv) > 1:
 date = int(sys.argv[1])
else:
 date = int(input('Date? '))

yr0=int(date/10000)
mn0=int((date % 10000)/100)
day0=int(date % 100)
date0 = dt.datetime(yr0,mn0,day0)
doy0 = date0.timetuple().tm_yday
yr2 = int(yr0 % 100)

if len(sys.argv) < 3:
 fname_refpos = input('Reference Position file? ')
else:
 fname_refpos = sys.argv[2]
#print fname_refpos

if len(sys.argv) < 6:
 prn0 = int(input('PRN? '))
 stime = float(input('Start time (hr)? '))
 etime = float(input('End time (hr)? '))
else:
 prn0 = int(sys.argv[3])
 stime = float(sys.argv[4])
 etime = float(sys.argv[5])

if len(sys.argv) < 8:
 vv = float(input('Front Velocity (m/s)?' ))
 theta = float(input('Orientation (CW from North)? '))
else:
 vv = float(sys.argv[6])
 theta = float(sys.argv[6])

trange1 = [stime,etime]

f = []
#f.append(os.path.join(data_dir,'%s%3.3d0.%2.2daatr' %(site[0],doy0,yr2)))
#f.append(os.path.join(data_dir,'%s%3.3d0.%2.2daatr' %(site[1],doy0,yr2)))
#f.append(os.path.join(data_dir,'%s%3.3d0.%2.2daatr' %(site[2],doy0,yr2)))
f.append(os.path.join(data_dir,'%s%4.4d%2.2d%2.2d.stec' %(site[site_id[0]],yr0,mn0,day0)))
f.append(os.path.join(data_dir,'%s%4.4d%2.2d%2.2d.stec' %(site[site_id[1]],yr0,mn0,day0)))
f.append(os.path.join(data_dir,'%s%4.4d%2.2d%2.2d.stec' %(site[site_id[2]],yr0,mn0,day0)))
print(f)

rpos = loadtxt(fname_refpos)
gg1 = matrix([rpos[site_id[0],0],rpos[site_id[0],1],rpos[site_id[0],2]]).T
gg2 = matrix([rpos[site_id[1],0],rpos[site_id[1],1],rpos[site_id[1],2]]).T
gg3 = matrix([rpos[site_id[2],0],rpos[site_id[2],1],rpos[site_id[2],2]]).T


plot_tec = 0

map_alt = 350
elmask = 20
elmask = 10

d1=loadtxt(f[0])
d2=loadtxt(f[1])
d3=loadtxt(f[2])

t10=(d1[:,0] % 86400)/3600.0 
t20=(d2[:,0] % 86400)/3600.0
t30=(d3[:,0] % 86400)/3600.0

id1=where((d1[:,1] == prn0) & (d1[:,7] >= elmask) & (t10 >= stime) & (t10 < etime))[0]
id2=where((d2[:,1] == prn0) & (d2[:,7] >= elmask) & (t20 >= stime) & (t20 < etime))[0]
id3=where((d3[:,1] == prn0) & (d3[:,7] >= elmask) & (t30 >= stime) & (t30 < etime))[0]

print(len(id1),len(id2),len(id3))
if((len(id1) == 0) | (len(id2) == 0) | (len(id3) == 0)):
 print('Not enough data found')
 exit()

t1=t10[id1]
t2=t20[id2]
t3=t30[id3]

stec_offs1=(d1[id1,2]-d1[id1,3]).mean()
stec_offs2=(d2[id2,2]-d2[id2,3]).mean()
stec_offs3=(d3[id3,2]-d3[id3,3]).mean()

stec1=d1[id1,3]+stec_offs1
stec2=d2[id2,3]+stec_offs2
stec3=d3[id3,3]+stec_offs3

aatr1=d1[id1,8]
aatr2=d2[id2,8]
aatr3=d3[id3,8]

dstec21 = zeros(86400)
t21 = zeros(86400)

count = 0
for ii in range(0,len(id1)):
 if (t1[ii] > stime) & (t1[ii] < etime):
  id21 = where(t2 == t1[ii])[0]
  if len(id21) > 0:
   t21[count] = t1[ii]
   dstec21[count] = stec2[id21] - stec1[ii] - stec_offs2 + stec_offs1
   count = count + 1

#print count
#fig2 = figure(2)
#id_dstec_base = abs(t21 - stime).argmin()
#plot(t21[0:count],-(dstec21[0:count]-dstec21[id_dstec_base])*tec2delay)
#ylabel('%s - %s (m)' %(site[0],site[1]))
#xlim(trange1[0],trange1[1])
#grid()
#xlabel('GPST')

data_tri = delay_tri_data()
data_tri.xdata[0] = t1
data_tri.xdata[1] = t2
data_tri.xdata[2] = t3
data_tri.ydata[0] = stec1*tec2delay
data_tri.ydata[1] = stec2*tec2delay
data_tri.ydata[2] = stec3*tec2delay
data_tri.az[0] = 90 - d1[id1,6]
data_tri.az[1] = 90 - d2[id2,6]
data_tri.az[2] = 90 - d3[id3,6]
data_tri.el[0] = d1[id1,7]
data_tri.el[1] = d2[id2,7]
data_tri.el[2] = d3[id3,7]
gg = {}
gg[0] = gg1
gg[1] = gg2
gg[2] = gg3
print(gg[0])

fig5 = figure(5)
ax5 = fig5.add_subplot(111)
for ii in range(3):
 ax5.plot(data_tri.xdata[ii],data_tri.ydata[ii],label=site[site_id[ii]])
ylabel('Slant Delay (m)')
xlim(trange1[0],trange1[1])
grid()
cid5 = fig5.canvas.mpl_connect('button_press_event',onclick)
#cid5 = fig5.canvas.mpl_connect('button_press_event',oncpaint)
cid5 = fig5.canvas.mpl_connect('key_press_event',onkey)

show()

ttt=1
