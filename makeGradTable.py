import re
import os

def extract_date_and_no(filename):
    pattern = r"output_aatr_vel_(\d{8})-(\d+)\.png"
    match = re.search(pattern, filename)
    if match:
        return match.group(1), match.group(2)  # NOをそのまま取得
    else:
        return None, None

def extract_info_from_file(filename, prn_no):
    prn_no_int = int(prn_no)  # NOを整数として扱う
    with open(filename, 'r') as file:
        for line in file:
            if line.startswith(f"PRN: {prn_no_int}"):  # 整数として扱ったPRNを使う
                info = line.strip()  # 改行を除去
                return info
        return None

def process_status_file(status_file, output_file):
    with open(status_file, 'r') as file:
        lines = [line.strip() for line in file.readlines()]  # 改行を取り除く

    output_lines = []
    for line in lines:
        date, no = extract_date_and_no(line)
        if date and no and not line.endswith("Bad"):
            grad2d_file = f"results/grad2d/grad2d_{date}000000.txt"
            if os.path.exists(grad2d_file):
                info = extract_info_from_file(grad2d_file, no)
                if info:
                    line += f", {info.rstrip()}"  # 改行を削除
                    output_lines.append(line)

    with open(output_file, 'w') as file:
        file.write('\n'.join(output_lines))  # 改行を追加して書き込み

status_file = "status_vel.txt"
output_file = "status_vel_with_info.txt"
process_status_file(status_file, output_file)
