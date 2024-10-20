import os
import re
import pikepdf

# パスワードをファイルから読み込む
with open(".password", "r") as file:
    password = file.read().strip()  # パスワードを読み込み、改行を削除

# 入力フォルダと出力フォルダの指定
input_folder = "./input"
output_folder = "./output"

# ファイル名の変換ルール
prefix_map = {
    'bornus': '賞与',
    'gensen': '源泉徴収票',
    'salary': '給与明細'
}

# ファイル名のパターン
file_patterns = {
    'bornus': r'bonus_(\d{4})-(\d{2})-(\d{2})',
    'gensen': r'gensen_(\d{4})',
    'salary': r'salary_(\d{4})-(\d{2})-(\d{2})'
}

# 入力フォルダからすべてのPDFファイルを取得
pdf_files = [f for f in os.listdir(input_folder) if f.endswith('.pdf')]

# 各ファイルを処理
for pdf_file in pdf_files:
    for prefix, pattern in file_patterns.items():
        match = re.match(pattern, pdf_file)
        if match:
            # ファイル名の接頭語を置き換え
            new_prefix = prefix_map[prefix]
            
            if prefix == 'gensen':
                # gensenの場合はYYYYのみ使用
                year = match.group(1)
                new_file_name = f"{new_prefix}_{year}.pdf"
            else:
                # bornus, salaryの場合はYYYYMM形式に変換
                year, month = match.group(1), match.group(2)
                new_file_name = f"{new_prefix}_{year}{month}.pdf"
            
            # ファイルのパスを作成
            input_path = os.path.join(input_folder, pdf_file)
            output_path = os.path.join(output_folder, new_file_name)
            
            # パスワードを使用してPDFを開き、パスワード解除
            try:
                with pikepdf.open(input_path, password=password) as pdf:
                    # パスワード解除後に保存
                    pdf.save(output_path)
                print(f"パスワード解除済み: {pdf_file} -> {new_file_name}")
            except pikepdf._qpdf.PasswordError:
                print(f"パスワード解除に失敗: {pdf_file}")
            break
