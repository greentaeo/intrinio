import pandas as pd
import re
import os

# 현재 작업 디렉토리 출력
print("현재 작업 디렉토리:", os.getcwd())

# 엑셀 파일 경로
excel_file = 'sic_indices.xlsx'

# 엑셀 파일이 존재하는지 확인
if not os.path.exists(excel_file):
    print(f"엑셀 파일 '{excel_file}'을 찾을 수 없습니다. 파일 경로를 확인하세요.")
    exit()

print(f"엑셀 파일 '{excel_file}'이(가) 존재합니다.")

# 대분류 SIC 코드와 산업군 이름 매핑 사전
major_group_mapping = {
    '01': '농업, 임업 및 어업',
    '02': '농업, 임업 및 어업',
    '07': '농업, 임업 및 어업',
    '08': '농업, 임업 및 어업',
    '09': '농업, 임업 및 어업',
    '10': '광업',
    '12': '광업',
    '13': '광업',
    '14': '광업',
    '15': '건설업',
    '16': '건설업',
    '17': '건설업',
    '20': '제조업',
    '21': '제조업',
    '22': '제조업',
    '23': '제조업',
    '24': '제조업',
    '25': '제조업',
    '26': '제조업',
    '27': '제조업',
    '28': '제조업',
    '29': '제조업',
    '30': '제조업',
    '31': '제조업',
    '32': '제조업',
    '33': '제조업',
    '34': '제조업',
    '35': '제조업',
    '36': '제조업',
    '37': '제조업',
    '38': '제조업',
    '39': '제조업',
    '40': '운송 및 공공 서비스',
    '41': '운송 및 공공 서비스',
    '42': '운송 및 공공 서비스',
    '43': '운송 및 공공 서비스',
    '44': '운송 및 공공 서비스',
    '45': '운송 및 공공 서비스',
    '46': '운송 및 공공 서비스',
    '47': '운송 및 공공 서비스',
    '48': '통신서비스',
    '49': '유틸리티',
    '50': '도매업',
    '51': '도매업',
    '52': '소매업',
    '53': '소매업',
    '54': '소매업',
    '55': '소매업',
    '56': '소매업',
    '57': '소매업',
    '58': '소매업',
    '59': '소매업',
    '60': '금융, 보험 및 부동산',
    '61': '금융, 보험 및 부동산',
    '62': '금융, 보험 및 부동산',
    '63': '금융, 보험 및 부동산',
    '64': '금융, 보험 및 부동산',
    '65': '금융, 보험 및 부동산',
    '66': '금융, 보험 및 부동산',
    '67': '금융, 보험 및 부동산',
    '70': '서비스업',
    '72': '서비스업',
    '73': '정보기술',
    '75': '서비스업',
    '76': '서비스업',
    '78': '서비스업',
    '79': '서비스업',
    '80': '헬스케어',
    '81': '서비스업',
    '82': '서비스업',
    '83': '서비스업',
    '84': '서비스업',
    '85': '서비스업',
    '86': '서비스업',
    '87': '서비스업',
    '88': '서비스업',
    '89': '서비스업',
    '91': '공공 행정',
    '92': '공공 행정',
    '93': '공공 행정',
    '94': '공공 행정',
    '95': '공공 행정',
    '96': '공공 행정',
    '97': '공공 행정',
    '98': '공공 행정',
    '99': '공공 행정'
}

# SIC 코드에서 대분류 추출 및 매핑 함수
def map_major_sic(sic_code):
    try:
        sic_str = str(int(sic_code)).zfill(4)  # 숫자를 4자리 문자열로 변환
        major_code = sic_str[:2]
        return major_group_mapping.get(major_code, '기타')
    except:
        return 'Unknown'

# 엑셀 파일 불러오기
try:
    df = pd.read_excel(excel_file)
except FileNotFoundError:
    print(f"엑셀 파일 '{excel_file}'을 찾을 수 없습니다. 파일 경로를 확인하세요.")
    exit()

# 'Code' 열을 문자열로 변환하여 앞 두 자리 추출
df['Code'] = df['Code'].astype(str).str.zfill(4)  # 4자리로 맞추기 (앞에 0 채우기)

# 대분류 산업군 매핑
df['MajorGroup'] = df['Code'].apply(lambda x: x[:2])
df['IndustryGroup'] = df['MajorGroup'].map(major_group_mapping)

# 'Unknown' 및 '기타' 처리 (필요 시)
df['IndustryGroup'] = df['IndustryGroup'].replace({'Unknown': '기타'})

# 세분화 산업군 이름 추가
df['SubCategory'] = df['Name']

# 섹터별로 데이터 그룹화
grouped = df.groupby('IndustryGroup')

# 엑셀 파일로 저장 (각 섹터를 별도의 시트로 저장)
with pd.ExcelWriter('sic_indices_by_sector.xlsx') as writer:
    for sector, group in grouped:
        # Excel 시트 이름은 최대 31자까지 허용 및 특수 문자 제거
        safe_sector = re.sub(r'[\\/*?:"<>|]', "_", sector)[:31]
        group.to_excel(writer, sheet_name=safe_sector, index=False)
    
    print("섹터별로 정렬된 데이터가 'sic_indices_by_sector.xlsx' 파일로 저장되었습니다.")

# 또는, 섹터별로 별도의 CSV 파일로 저장하려면:
for sector, group in grouped:
    # 파일 이름에 사용할 수 없는 문자가 있는지 확인
    safe_sector = re.sub(r'[\\/*?:"<>|]', "_", sector)
    group.to_csv(f'sic_indices_{safe_sector}.csv', index=False)
    print(f"'{safe_sector}' 섹터의 데이터가 'sic_indices_{safe_sector}.csv' 파일로 저장되었습니다.")