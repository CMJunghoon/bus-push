# 🚌 202번 버스 자동 알림 시스템

평일 오전 5:45-6:00 사이에 호반써밋라포레후문 정류장의 202번 버스가 11분 전에 도착할 때 OneSignal을 통해 푸시 알림을 전송하는 자동화 시스템입니다.

## ✨ 주요 기능

- **자동 스케줄링**: 평일 오전 5:45-6:00, 1분마다 실행
- **정확한 알림 조건**: 가장 빠른 버스가 정확히 11분 전일 때만 알림
- **실제 버스 정보**: 차량번호, 현재 위치, 도착 시간 표시
- **OneSignal 푸시 알림**: 실시간 모바일 알림

## 🛠️ 설치 및 설정

### 1. 의존성 설치
```bash
pip3 install -r requirements.txt
```

### 2. OneSignal 설정
`push_notification.py` 파일에서 다음 값들을 설정하세요:
```python
APP_ID = "your_onesignal_app_id"
REST_KEY = "your_onesignal_rest_api_key"
```

## 🚀 사용법

### 스케줄러 모드 (서버용)
```bash
python3 bus_push_main.py --schedule
```

### 일회성 실행 (테스트용)
```bash
python3 bus_push_main.py
```

## 📱 푸시 알림 예시
```
호반써밋라포레후문 정류장
🚌 경기74자9169: 11분후 ( 10전 )
🚌 경기74자1012: 25분후 ( 15전 )
```

## 🌐 서버 배포

### Railway 배포 (추천)

1. **Railway 계정 생성**: [railway.app](https://railway.app) 회원가입
2. **GitHub 연동**: 이 프로젝트를 GitHub에 업로드
3. **Railway 프로젝트 생성**: 
   - "New Project" → "Deploy from GitHub repo"
   - 이 리포지토리 선택
4. **환경 변수 설정**: Railway 대시보드에서 설정
5. **시작 명령어 설정**: `python3 bus_push_main.py --schedule`

#### Railway 배포용 파일들

**Procfile** (Railway가 자동으로 실행할 명령어):
```
worker: python3 bus_push_main.py --schedule
```

**railway.json** (Railway 설정):
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python3 bus_push_main.py --schedule"
  }
}
```

### 기타 배포 옵션

- **Render**: 무료 플랜 있지만 15분 후 슬립 모드
- **Google Cloud Run**: $300 무료 크레딧
- **AWS Lambda**: 서버리스, 설정 복잡
- **PythonAnywhere**: Python 특화, 스케줄링은 유료

## 🔧 시스템 요구사항

- Python 3.7+
- 인터넷 연결
- OneSignal 계정 및 API 키

## 📋 파일 구조

```
bus-push/
├── bus_push_main.py      # 메인 실행 파일
├── push_notification.py  # OneSignal 푸시 알림
├── simple_bus.py        # 버스 정보 조회 (단독 실행용)
├── requirements.txt     # Python 패키지 의존성
└── README.md           # 이 파일
```

## ⚙️ 설정 옵션

### 알림 조건 변경
`should_send_push()` 함수에서 조건 수정:
```python
if time1 is not None and time1 == 11:  # 11분 → 다른 값으로 변경
```

### 실행 시간 변경
`is_target_time()` 함수에서 시간 수정:
```python
start_time = dt_time(5, 45)  # 5시 45분 → 다른 시간으로 변경
end_time = dt_time(6, 0)     # 6시 → 다른 시간으로 변경
```

## 🐛 문제 해결

### SSL 인증서 오류
- 현재 `curl` 명령어로 우회 처리됨
- 필요시 `requests`에서 `verify=False` 옵션 사용

### OneSignal 푸시 실패
- APP_ID와 REST_KEY 확인
- OneSignal 대시보드에서 기기 등록 상태 확인

### 스케줄러 중지
- `Ctrl+C`로 안전하게 중지 가능

## 📞 API 정보

- **경기도 버스 API**: `https://apis.data.go.kr/6410000/busarrivalservice/v2/getBusArrivalListv2`
- **정류장 ID**: 223000149 (호반써밋라포레후문)
- **OneSignal API**: `https://api.onesignal.com/notifications`

---

💡 **문의사항이나 개선 제안이 있으시면 언제든 연락주세요!** 