import requests
import json
from datetime import datetime

def fetch_sic_data():
    """Intrinio API에서 원본 SIC 데이터를 가져와서 JSON 파일로 저장합니다."""
    
    # API 설정
    API_KEY = "OjFlODE0NzEwMDVhOTlhZjFjNzY4OGViNmI1ODY3ODEy"
    BASE_URL = "https://api-v2.intrinio.com/indices/sic"
    
    try:
        # API 요청
        params = {
            "api_key": API_KEY,
            "page_size": 2000  # 최대 데이터 수
        }
        
        print("API에서 데이터를 가져오는 중...")
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()  # HTTP 에러 체크
        
        # 응답 데이터 가져오기
        data = response.json()
        
        # 고정된 파일명 사용
        filename = "/Users/xodh3/intrinio/backend/app/services/screener/data/sic_data.json"
        
        # 백업 파일 생성 (필요한 경우)
        backup_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"/Users/xodh3/intrinio/backend/app/services/screener/data/backups/sic_data_backup_{backup_timestamp}.json"
        
        # 기존 파일 백업
        try:
            with open(filename, 'r') as f:
                with open(backup_filename, 'w') as backup_f:
                    backup_f.write(f.read())
                print(f"기존 파일이 {backup_filename}으로 백업되었습니다.")
        except FileNotFoundError:
            pass
        
        # 새로운 데이터 저장
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            
        print(f"데이터가 {filename}에 저장되었습니다.")
        print(f"총 {len(data['indices'])}개의 SIC 코드 데이터가 저장되었습니다.")
        
    except requests.exceptions.RequestException as e:
        print(f"API 요청 중 오류 발생: {e}")
    except Exception as e:
        print(f"처리 중 오류 발생: {e}")

if __name__ == "__main__":
    fetch_sic_data()