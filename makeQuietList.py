import re

status_file = 'status.txt'

# Read the status.txt file to extract dates with "Quiet"
quiet_dates = []
disturb_dates = []
with open(status_file, 'r') as status_file:
    for line in status_file:

        date = ''        
        match = re.search(r'(\d{4})(\d{2})(\d{2})', line)
        if match:
            year, month, day = match.groups()
            date = f"{year}{month}{day}"
            
            if 'Quiet' in line:    
                quiet_dates.append(date)
            if 'Day' in line or 'Night' in line:
                disturb_dates.append(date)
            
# Open flist.txt in write mode and write file paths
with open('quiet_list.txt', 'w') as flist_file:
    for date in quiet_dates:
        # Generate the file path format (adjust as needed)
        file_path = f'results/sigma_vig/{date}000000cdf.out'
        flist_file.write(file_path + '\n')

print("quiet_list.txt has been generated.")

# Open flist.txt in write mode and write file paths
with open('disturb_list.txt', 'w') as flist_file:
    for date in disturb_dates:
        # Generate the file path format (adjust as needed)
        file_path = f'{date}'
        flist_file.write(file_path + '\n')

print("disturb_list.txt has been generated.")
