#!/bin/bash
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
