import subprocess
import re
import os
import pickle

#refposFile = 'refpos_Hanoi2.dat'
refposFile = 'refpos_IDN_20230318.txt' #### 20230320

print(f'Reference position file = {refposFile}')

def save_database(database, velocityFile):
    """
    Save the database in binary format with backup.
    
    Parameters:
    - database: The dictionary containing the data to be saved.
    - velocityFile: The file path where the data should be saved.
    """
    # Display the final database
    print(database)

    # Save the database in binary format
    with open(velocityFile, "wb") as f:
        if os.path.exists(velocityFile):
            # Create a backup of the existing file
            d = subprocess.run(['cp', velocityFile, velocityFile+'.back'])

        # Dump the database dictionary to the file
        pickle.dump(database, f, protocol=2)


        
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


status_vel = {}
statusFile = 'status_vel.txt'
if os.path.exists(statusFile):
    with open(statusFile, 'r') as status_vel_file:
        # Iterate through each line in the file
        for line in status_vel_file:
            fields = line.strip().split()
            if len(fields) >= 2:
                match = re.search(r'(\d{8}-\d+)', fields[0])
                if match:
                    key = match.group(1)
                    status_vel[key] = fields[1]
else:
    print("## No velocity status file 'status_vel.txt'")
    print("## Make 'status_vel.txt' file by judgeVelScript.py")
    exit()
    
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
                    refposFile,
                    str(satNo),
                    str(float(time) / 3600. - 0.1),
                    str(float(time) / 3600. + 0.1)
                ]

                command = " ".join(cmd)


                kstr = f'{date}-{int(satNo):02d}'
                isGood = False
                if kstr in status_vel:                    
                    if status_vel[kstr] == 'Good':
                        isGood = True
                        
                if isGood: 
                    print(command)
                    print(f"MaxGrad={data_dict['MaxGrad']}")
                    
                    user_input = input(f"Execute command? ('y' to execute, 'q' to quit): ").upper()
                    
                    if user_input == "Q":
                        print("Quitting...")
                        save_database(database, velocityFile)  
                        exit()
                        
                    if user_input == "Y":

                        # Check if kstr exists in the database
                        if kstr in database:
                            print(f"Velocity for {kstr} already exists in the database.")
                            user_input = input("Do you want to overwrite? ('y' to overwrite, 'd' to delete the entry): ").upper()
                            if user_input == "D":
                                del database[kstr]
                                print(f"Entry {kstr} deleted.")
                                continue 
                            elif user_input != "Y":
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

                        if (v != None and angle !=None):        
                            # Save the values in the dictionary
                            result_dict = {}
                            result_dict["cmd"]= cmd
                            result_dict["V"] = v
                            result_dict["Angle"] = angle
                            print(result_dict)

                            # Update or add the entry to the database
                            database[kstr] = result_dict
                    else:
                        continue
 

# Save the database using the function
save_database(database, velocityFile)
                   
# ...

    
