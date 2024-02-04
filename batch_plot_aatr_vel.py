import subprocess
import re
import os
import pickle

# Specify the file containing the list of dates
dateList = 'disturb_list.txt'

# Read the list of dates from the file
with open(dateList, 'r') as date_file:
    date_list = [line.strip() for line in date_file]

# Specify the file for storing velocity data
velocityFile = "velocity_dict.pkl"

# Check if the velocity file exists
if os.path.exists(velocityFile):
    # If the file exists, load the data from it
    with open(velocityFile, 'rb') as file:
        database = pickle.load(file)
else:
    # If the file does not exist, initialize an empty dictionary
    database = {}


# ...

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
                    'python/plot_aatr_vel_jsf.py',
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
                    
                    user_input = input(f"Execute command? ('y' to execute, 'q' to quit): ").upper()
                    if user_input == "Q":
                        print("Quitting...")
                        exit()
                    if user_input == "Y":

                        # Check if kstr exists in the database
                        if kstr in database:
                            print(f"Velocity for {kstr} already exists in the database.")
                            user_input = input("Do you want to overwrite? ('y' to overwrite): ").upper()
                            if user_input != "Y":
                                continue  # Skip to the next iteration if not confirmed
                        
                        output = subprocess.run(cmd, capture_output=True)

                        stdout = output.stdout.decode("utf-8")
                        print(stdout)

                        # Extract the value of V
                        v_start = stdout.find("V = ")
                        v_end = None
                        v = None
                        while v_start != -1:
                            v_end = stdout.find(" (m/s)\n", v_start)
                            v = stdout[v_start + 4: v_end]
                            v_start = stdout.find("V = ", v_end)

                        # Extract the value of Angle
                        angle_start = stdout.find("Angle (CW from N) = ")
                        angle_end = None
                        angle = None
                        while angle_start != -1:
                            angle_end = stdout.find(" (deg)\n", angle_start)
                            angle = stdout[angle_start + 20: angle_end]
                            angle_start = stdout.find("Angle (CW from N) = ", angle_end)

                        # Save the values in the dictionary
                        data_dict["cmd"]= cmd
                        data_dict["V"] = v
                        data_dict["Angle"] = angle
                        print(data_dict)

                        # Update or add the entry to the database
                        database[kstr] = data_dict
                    else:
                        continue
 
# Display the final database
print(database)

# Save the database in binary format
with open(velocityFile, "wb") as f:
    if os.path.exists(velocityFile):
        d = subprocess.run(['cp', velocityFile, velocityFile+'.back'])
    pickle.dump(database, f, protocol=2)
                   
# ...

    

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
