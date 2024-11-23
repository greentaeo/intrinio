import json
import os
from sic_mappings import SICMappings

def convert_to_hierarchy(input_path, output_path):
    """SIC 코드 계층 구조 변환"""
    if not os.path.exists(input_path):
        print(f"입력 파일이 존재하지 않습니다: {input_path}")
        return

    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)
    except json.JSONDecodeError:
        print("JSON 파일 형식이 올바르지 않습니다.")
        return

    hierarchy = {"sic_codes": {}}
    data_items = raw_data.get('indices', [])
    
    # 1. 데이터 정리 및 유효성 검사
    valid_items = {}
    for item in data_items:
        code = item['symbol'].replace('$SIC.', '')
        if SICMappings.is_valid_code(code) and not code.endswith('0'):
            valid_items[code] = item['name']
    
    # 2. 계층 구조 생성
    for code, name in valid_items.items():
        division_info = SICMappings.get_division_info(code)
        if not division_info:
            continue
            
        division_code = division_info['numeric_code']
        
        # 분류(Division) 추가
        if division_code not in hierarchy["sic_codes"]:
            hierarchy["sic_codes"][division_code] = {
                "name": division_info['name'],
                "name_en": division_info['name_en'],  # 영문 이름 추가
                "type": "division",
                "division_letter": division_info['letter'],
                "subcategories": {}
            }
        
        # 중분류(Major Group) 및 소분류(Industry) 처리
        major_group_code = code[:2] + "00"  # 예: "2000"
        if major_group_code not in hierarchy["sic_codes"][division_code]["subcategories"]:
            hierarchy["sic_codes"][division_code]["subcategories"][major_group_code] = {
                "name": SICMappings.get_major_group_name(major_group_code, "ko"),  # 한글 이름
                "name_en": SICMappings.get_major_group_name(major_group_code, "en"),  # 영문 이름
                "type": "major_group",
                "subcategories": {}
            }
        
        # 소분류(Industry) 추가
        hierarchy["sic_codes"][division_code]["subcategories"][major_group_code]["subcategories"][code] = {
            "name": name,  # 영문 이름만 유지
            "type": "industry"
        }
    
    # 3. 결과 저장
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(hierarchy, f, indent=2, ensure_ascii=False)
        print(f"\n계층 구조 생성 완료: {output_path}")
    except Exception as e:
        print(f"결과 저장 중 오류 발생: {e}")

if __name__ == "__main__":
    input_file_path = '/Users/xodh3/intrinio/backend/app/services/screener/data/sic_data.json'
    output_file_path = '/Users/xodh3/intrinio/backend/app/services/screener/data/sic_hierarchy.json'
    convert_to_hierarchy(input_file_path, output_file_path)