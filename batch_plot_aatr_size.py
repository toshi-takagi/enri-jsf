import subprocess
import pickle
import os
import re

def save_database(database, sizeFile):
    """
    Save the database in binary format with backup.
    
    Parameters:
    - database: The dictionary containing the data to be saved.
    - sizeFile: The file path where the data should be saved.
    """
    # Display the final database
    print(database)

    # Save the database in binary format
    with open(sizeFile, "wb") as f:
        if os.path.exists(sizeFile):
            # Create a backup of the existing file
            d = subprocess.run(['cp', sizeFile, sizeFile+'.back'])

        # Dump the database dictionary to the file
        pickle.dump(database, f, protocol=2)


# File path for the velocity data
velocityFile = "velocity_dict.pkl"

# Check if the file exists
if not os.path.isfile(velocityFile):
    print(f"Error: {velocityFile} not found. Exiting.")
    exit(1)

# Load database from the velocity file
with open(velocityFile, 'rb') as file:
    try:
        database = pickle.load(file)
    except Exception as e:
        print(f"Error loading data from {velocityFile}: {e}")
        exit(1)

# List to store the new command lists
new_command_list = []

# Process each entry in the database
for key, entry in database.items():
    # Replace 'python/plot_aatr_vel.py' with 'python/plot_aatr_size.py'
    entry['cmd'][1] = 'python/plot_aatr_size.py'
    
    # Add V and Angle to the cmd list
    entry['cmd'].extend([entry['V'], entry['Angle']])
    
    # Create a new command list
    if (entry['V'] is not None):    
        new_command_list.append(entry['cmd'])
    else:
        print(f"No velocity data for {key}")


# Specify the file for storing size data
sizeFile = "size_dict.pkl"

# Check if the size file exists
if os.path.exists(sizeFile):
    # If the file exists, load the data from it
    with open(sizeFile, 'rb') as file:
        result_dict = pickle.load(file)
else:
    # If the file does not exist, initialize an empty dictionary
    result_dict = {}


# Execute the new command lists sequentially
for cmd in new_command_list:
    kstr = f"{cmd[2]}-{cmd[4]}" # date + '-' + satNo
    print(f"### Size measurement for {kstr}")

    user_input = input(f"Execute command? ('y' to execute, 'q' to quit): ").upper()
    if user_input == "Q":
        print("Quitting...")
        save_database(database, velocityFile)  
        exit()
    if user_input == "Y":
        # Check if kstr exists in the database
        if kstr in result_dict:
            print(f"Size data for {kstr} already exists in the dictionaly.")
            user_input = input("Do you want to overwrite? ('y' to overwrite, 'q' to quit): ").upper()
            if user_input == "Q":
                print("Quitting...")
                # Save the result in binary format
                save_database(result_dict, sizeFile)            
                exit()
            if user_input != "Y":
                continue  # Skip to the next iteration if not confirmed
        
        # Run the command and capture the output
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # Split the output by lines
        lines = result.stdout.strip().split('\n')
        print(lines)
        
        # Iterate through the lines to find "Scale size" and corresponding value
        size_dict = {}
        for line in lines:
            # Use regular expression to match "Scale size (something)"
            match = re.search(r"Scale size \((\w+)\) = ([\d.]+) \(m\)", line)
            if match:
                key = match.group(1)
                value = float(match.group(2))
                # Add to the size_dict
                size_dict[key] = value

        result_dict[kstr]= {'cmd':cmd,'size':size_dict}
    

# Save the result in binary format
save_database(result_dict, sizeFile)

    
