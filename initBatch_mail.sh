#!/bin/bash

# 実行するスクリプト
scripts=("auto_stec.py" "auto_plot_aatr.py" "auto_sfcbca.py 0 1" "auto_sfcbca.py 1 2" "auto_sfcbca.py 2 0" "auto_plot_sfcbca.py" "auto_csum.py" "auto_cdf.py" "auto_plot_grad2d.py" "batch_plot_aatr_vel_fig.py")

# ログディレクトリの作成
log_dir="logs"
mkdir -p $log_dir

# スクリプト実行とログの保存
for script in "${scripts[@]}"; do
    echo "Running $script"
    python3 $script > "$log_dir/${script// /_}.log" 2>&1
done

# ログをtarで固める
tar -czf logs.tar.gz $log_dir

# メール送信
recipient="recipient@example.com"
subject="Logs from script execution"
body="Please find attached the logs from the script execution."
attachments="logs.tar.gz"

mail -s "$subject" -a "$attachments" "$recipient" <<< "$body"

# 一時ファイルの削除
rm -rf $log_dir logs.tar.gz

