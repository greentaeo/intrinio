"""
SIC (Standard Industrial Classification) 코드 매핑 모듈
"""
import json

class SICMappings:
    """SIC (Standard Industrial Classification) 코드 매핑 및 번역 클래스"""
    
    # 대분류 정의
    DIVISION_RANGES = {
        'A': {'range': (1, 9), 'name': '농업, 임업 및 어업', 'name_en': 'Agriculture, Forestry, and Fishing'},
        'B': {'range': (10, 14), 'name': '광업', 'name_en': 'Mining'},
        'C': {'range': (15, 17), 'name': '건설업', 'name_en': 'Construction'},
        'D': {'range': (20, 39), 'name': '제조업', 'name_en': 'Manufacturing'},
        'E': {'range': (40, 49), 'name': '운송, 통신 및 공공 서비스', 'name_en': 'Transportation, Communications, Electric'},
        'F': {'range': (50, 51), 'name': '도매업', 'name_en': 'Wholesale Trade'},
        'G': {'range': (52, 59), 'name': '소매업', 'name_en': 'Retail Trade'},
        'H': {'range': (60, 67), 'name': '금융, 보험 및 부동산', 'name_en': 'Finance, Insurance, and Real Estate'},
        'I': {'range': (70, 89), 'name': '서비스업', 'name_en': 'Services'},
        'J': {'range': (91, 99), 'name': '공공 행정', 'name_en': 'Public Administration'}
    }

    # 산업 분류 한글 매핑
    INDUSTRY_TRANSLATIONS = {
        # 제조업 관련
        "Plastics Products, nec": "플라스틱 제품 (기타)",
        "Communications Equipment, nec": "통신장비 (기타)",
        "Electronic Components, nec": "전자부품 (기타)",
        "Food And Kindred Products": "식품 및 관련 제품",
        "Beverages": "음료",
        "Tobacco Products": "담배 제품",
        "Textile Mill Products": "섬유 제품",
        
        # 금융/보험 관련
        "Investment Advice": "투자자문",
        "Security Brokers & Dealers": "증권 중개인 및 딜러",
        "Commercial Banks": "상업은행",
        "Insurance Carriers": "보험회사",
        "Real Estate": "부동산",
        
        # 통신/서비스 관련
        "Communications Services, nec": "통신서비스 (기타)",
        "Computer Programming Services": "컴퓨터 프로그래밍 서비스",
        "Business Services": "사업 서비스",
        "Health Services": "보건 서비스",
        
        # 특수 산업
        "Hazardous Waste Management": "유해폐기물 관리",
        "Electric Services": "전기 서비스",
        "Water Supply": "수도 공급",
        
        # 일반적인 용어
        "Manufacturing": "제조업",
        "Services": "서비스업",
        "Products": "제품",
        "Equipment": "장비",
        "Management": "관리",
        "Operations": "운영",
        
        # 약어 및 일반 용어
        "nec": "기타",
        "And": "및",
        "&": "및",
        "Services": "서비스"
    }

    @classmethod
    def get_korean_name(cls, english_name: str) -> str:
        """영문 산업명에 대한 한글 설명을 반환"""
        # 정확한 매칭 먼저 시도
        if english_name in cls.INDUSTRY_TRANSLATIONS:
            return cls.INDUSTRY_TRANSLATIONS[english_name]
        
        # 부분 매칭 시도
        translated_name = english_name
        for eng, kor in cls.INDUSTRY_TRANSLATIONS.items():
            translated_name = translated_name.replace(eng, kor)
        
        return translated_name

    @classmethod
    def get_division_info(cls, code: str) -> dict:
        """대분류 정보 반환 (한글 포함)"""
        if not code.isdigit():
            return None
            
        code_num = int(code[:2])
        
        for division_letter, info in cls.DIVISION_RANGES.items():
            start, end = info['range']
            if start <= code_num <= end:
                return {
                    'letter': division_letter,
                    'name': info['name'],
                    'name_en': info['name_en'],
                    'code_range': f"{start:02d}-{end:02d}",
                    'numeric_code': f"{code_num:02d}"
                }
        return None

    @classmethod
    def is_valid_code(cls, code: str) -> bool:
        """SIC 코드 유효성 검사"""
        try:
            if not code.isdigit():
                return False
            code_num = int(code)
            return 1000 <= code_num <= 9999 or 10 <= code_num <= 99
        except ValueError:
            return False

    @classmethod
    def format_code(cls, code: str) -> str:
        """코드 형식 통일화"""
        if not code.isdigit():
            return None
        return code.zfill(4)[:4]

    @staticmethod
    def get_hierarchy_info(code):
        """
        SIC 코드의 계층 구조 정보를 반환합니다.
        
        Args:
            code (str): SIC 코드
            
        Returns:
            dict: 계층 구조 정보를 담은 딕셔너리
                {
                    'major_group': {'code': str, 'name': str},
                    'industry': {'code': str, 'name': str}
                }
        """
        # 메이저 그룹은 코드의 첫 두 자리
        major_group_code = code[:2] + "00"
        
        return {
            'major_group': {
                'code': major_group_code,
                'name': SICMappings.get_major_group_name(major_group_code)
            },
            'industry': {
                'code': code,
                'name': SICMappings.get_korean_name(code)
            }
        }

    @classmethod
    def get_major_group_name(cls, code: str, lang: str = 'en') -> str:
        """
        메이저 그룹 코드에 대한 이름을 반환합니다.
        
        Args:
            code (str): SIC 메이저 그룹 코드 (예: "2900")
            lang (str): 언어 코드 ('ko' 또는 'en')
            
        Returns:
            str: 메이저 그룹의 이름
        """
        # 메이저 그룹 이름 매핑 정의
        MAJOR_GROUP_NAMES = {
            "2000": {
                "ko": "식품 및 관련 제품",
                "en": "FOOD AND KINDRED PRODUCTS"
            },
            "2800": {
                "ko": "화학 및 관련 제품",
                "en": "CHEMICALS AND ALLIED PRODUCTS"
            },
            # ... 다른 메이저 그룹들도 추가
        }
        
        try:
            # 먼저 하드코딩된 매핑에서 확인
            if code in MAJOR_GROUP_NAMES:
                return MAJOR_GROUP_NAMES[code].get(lang, MAJOR_GROUP_NAMES[code]['en'])
                
            # 파일에서 읽기
            file_path = '/Users/xodh3/sic_hierarchy.json'
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            division_code = code[:2]
            division = data['sic_codes'].get(division_code, {})
            major_group = division.get('subcategories', {}).get(code, {})
            
            if lang == 'ko':
                return major_group.get('name', '알 수 없는 그룹')
            else:
                return major_group.get('name_en', 'Unknown Group')
                
        except Exception as e:
            print(f"Error reading major group name: {e}")
            return '알 수 없는 그룹' if lang == 'ko' else 'Unknown Group'
