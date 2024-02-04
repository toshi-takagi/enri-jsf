#!/usr/local/bin/python3

import datetime
import os
import sys

def save_status_to_file(fileName,date, status):
    with open(fileName, "a") as file:
        file.write(f"{date}: {status}\n")

def check_status_exists(fileName,date):
    try:
        with open(fileName, "r") as file:            
            for line in file:
                if line.startswith(f"{date}:"):
                    return True
        return False
    except FileNotFoundError:
        return False
        
if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Usage: python judgeByDate.py <file_name>")
        sys.exit(1)

    fileName = sys.argv[1]
    print(f"Save status to {fileName}")    

    start_date = datetime.date(2022, 9, 27)
    end_date = datetime.date(2022, 10, 6)

    for single_date in (start_date + datetime.timedelta(n) for n in range((end_date - start_date).days + 1)):
        if check_status_exists(fileName,single_date):
            print(f"Status for {single_date} already exists. Skipping.")
            continue

        while True:
            user_input = input(f"Enter status for {single_date} (Enter for Quiet day, 'd/n' for Day/Night disturbance, 'x' for Bad dataset, 'q' to quit): ").upper()
            if user_input == "Q":
                print("Quitting...")
                exit()
            elif user_input == "D":
                save_status_to_file(fileName, single_date, "Day")
                break
            elif user_input == "N":
                save_status_to_file(fileName, single_date, "Night")
                break
            elif user_input == "X":
                save_status_to_file(fileName, single_date, "BadData")
                break
            elif user_input == "":
                save_status_to_file(fileName, single_date, "Quiet")
                break
            else:
                print("Invalid input. Please try again.")

