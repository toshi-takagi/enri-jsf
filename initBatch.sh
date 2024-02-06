#!/bin/bash
echo 'Running auto_stec.py'
python3 auto_stec.py  > auto_stec.log 2>&1
echo 'Running auto_plot_aatr.py'
python3 auto_plot_aatr.py  > auto_plot_aatr.log 2>&1 
echo 'Running auto_sfcbca.py 0 1'
python3 auto_sfcbca.py 0 1  > auto_sfcbca0-1.log 2>&1
echo 'Running auto_sfcbca.py 1 2'
python3 auto_sfcbca.py 1 2  > auto_sfcbca1-2.log 2>&1
echo 'Running auto_sfcbca.py 2 0'
python3 auto_sfcbca.py 2 0  > auto_sfcbca2-0.log 2>&1
echo 'Running auto_plot_sfcbca.py'
python3 auto_plot_sfcbca.py > auto_plot_sfcbca.log 2>&1
echo 'Running auto_csum.py'
python3 auto_csum.py > auto_csum.log 2>&1
echo 'Running auto_cdf.py'
python3 auto_cdf.py > auto_cdf.log 2>&1
find results/sigma_vig/*csum.out > flist_csum
echo 'Running auto_plot_grad2.py'
python3 auto_plot_grad2.py flist_csum > auto_plot_grad2.log 2>&1
echo 'Running batch_plot_aatr_vel_fig.py'
python3 batch_plot_aatr_vel_fig.py > auto_plot_aatr_vel_fig.log 2>&1
