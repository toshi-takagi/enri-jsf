import subprocess
import re
import os

# Specify the file containing the list of dates
dateList = 'disturb_list.txt'

# Read the list of dates from the file
with open(dateList, 'r') as date_file:
    date_list = [line.strip() for line in date_file]

    
# Process for each date in the list
for date in date_list:
    # Read data from the specified file for the current date
    with open(f'results/grad2d/grad2d_{date}000000.txt', 'r') as awk_input_file:
        # Iterate through each line in the file
        for line in awk_input_file:
            fields = line.strip().split(':')
            if len(fields) >= 4:
                # Split the line by commas
                splits = line.split(",")
                # Create a dictionary
                data_dict = {}
                data_dict["Date"] = date
                # Populate the dictionary with key-value pairs
                for split in splits:
                    key, value = split.split(":")
                    data_dict[key.strip()] = value.strip()

                satNo = str(data_dict['PRN'])
                time = str(data_dict['id2_time']).strip("\n")

                # Extract necessary information
                cmd = [
                    'python3',
                    'python/plot_aatr_vel_fig.py',
                    str(date),
                    'refpos_Hanoi2.dat',
                    str(satNo),
                    str(float(time) / 3600. - 0.1),
                    str(float(time) / 3600. + 0.1)
                ]

                command = " ".join(cmd)

                # Execute the Python script
                if float(data_dict['MaxGrad']) > 100:
                    kstr = date + '-' + satNo


                    print(command)
                    print(f"MaxGrad={data_dict['MaxGrad']}")
                    output = subprocess.run(cmd, capture_output=True)
 


    

"""
import subprocess

# ファイルからdateのリストを読み込む
with open('disturb_list.txt', 'r') as date_file:
    date_list = [line.strip() for line in date_file]

# dateごとに処理を実行
for date in date_list:
    # AWKコマンドを組み立て
    awk_command = f"awk -v date={date} '{{gsub(/,/, " "); if ($4 > 300) {{cmd="python3 python/plot_aatr_vel.py "date" refpos_Hanoi2.dat "$2" "($8/3600.-0.1)" "($8/3600.+0.1); print cmd; system(cmd)}}}}' results/grad2d/grad2d_{date}000000.txt"

    # AWKコマンドを実行
    subprocess.run(awk_command, shell=True)
"""
