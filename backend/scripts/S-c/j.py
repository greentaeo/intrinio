import pandas as pd
import os

# 데이터 파일 경로
files_to_process = [
    "/Volumes/data/US Fundamentals, 10+ years/US_FIN_CALCULATIONS/US_FIN_CALCULATIONS.csv",
]

for file_path in files_to_process:
    print(f"Processing file: {file_path}")
    # Read CSV with specified dtype to avoid mixed type warnings
    data = pd.read_csv(file_path, dtype=str)

    # Initial shape
    print(f"Initial data shape: {data.shape}")

    # NaN 값 처리
    data.fillna(0, inplace=True)  # NaN을 0으로 대체

    # 열 이름 확인
    print("Available columns:", data.columns.tolist())

    # 필요한 열 선택
    columns_to_keep = [
        "fundamental_id", "company_id", "name", "ticker", 
        "start_date", "end_date", "ebitdamargin", "investedcapital"
    ]

    # 열이 있는지 확인
    missing_columns = [col for col in columns_to_keep if col not in data.columns]
    if missing_columns:
        print(f"Missing columns: {missing_columns}")
        continue  # Skip to the next file if there are missing columns

    data = data[columns_to_keep]

    # 가공된 데이터 확인
    print(f"Data shape after processing: {data.shape}")

    # 가공된 데이터 저장
    processed_file_path = file_path.replace('.csv', '_processed.csv')
    data.to_csv(processed_file_path, index=False)
    print(f"Processed data saved to: {processed_file_path}")