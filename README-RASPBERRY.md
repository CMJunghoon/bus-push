# 🍓 라즈베리파이 + 도커로 202번 버스 알림 시스템 실행하기

라즈베리파이에서 도커를 사용해 202번 버스 자동 알림 시스템을 24/7 실행하는 가이드입니다.

## ⚡ 빠른 시작 (이미 설정된 경우)

```bash
# 프로젝트 디렉토리로 이동
cd bus-push

# 즉시 시작
docker compose up -d

# 로그 확인
docker compose logs -f
```

## 🛠️ 사전 준비

### 1. 라즈베리파이 설정
- **OS**: Raspberry Pi OS (Bullseye 이상 권장)
- **메모리**: 최소 1GB (2GB 이상 권장)
- **저장공간**: 최소 8GB

### 2. 도커 설치
```bash
# 도커 설치 스크립트 실행
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 현재 사용자를 도커 그룹에 추가
sudo usermod -aG docker $USER

# 도커 컴포즈 설치 (v2)
sudo apt update
sudo apt install docker-compose-plugin

# 재부팅 (권장)
sudo reboot
```

### 3. 도커 설치 확인
```bash
docker --version
docker compose version
```

## 🚀 시스템 설치 및 실행

### 1. 프로젝트 다운로드
```bash
# Git으로 클론 (GitHub에 업로드된 경우)
git clone [your-repo-url]
cd bus-push

# 또는 파일 직접 업로드
scp -r ./bus-push pi@[라즈베리파이_IP]:/home/pi/
```

### 2. 환경 설정
```bash
# 환경변수 파일 생성
cp env.example .env

# OneSignal 설정 수정
nano .env
```

**.env 파일 예시:**
```bash
# 버스 API 설정 (실제 값으로 변경)
BUS_API_KEY=your_actual_bus_api_key_here

# OneSignal 설정 (실제 값으로 변경)
ONESIGNAL_APP_ID=your_actual_onesignal_app_id_here
ONESIGNAL_REST_KEY=your_actual_onesignal_rest_key_here

# 시간대 설정
TZ=Asia/Seoul
```

### 3. 시스템 시작
```bash
# 🚀 가장 간단한 방법
docker compose up -d

# 또는 스크립트 사용 (추가 검증 포함)
./start.sh
```

## 📋 관리 명령어

### 빠른 명령어 (스크립트)
```bash
./start.sh    # 시스템 시작
./stop.sh     # 시스템 중지  
./logs.sh     # 실시간 로그 확인
```

### 도커 명령어
```bash
# 컨테이너 상태 확인
docker compose ps

# 실시간 로그 확인
docker compose logs -f

# 컨테이너 중지
docker compose down

# 컨테이너 재시작
docker compose restart

# 이미지 재빌드
docker compose up --build -d
```

## 🔧 시스템 동작 확인

### 1. 컨테이너 실행 상태
```bash
docker compose ps
```
**예상 출력:**
```
NAME               IMAGE           COMMAND                  STATUS
bus-push-system    bus-push_bus-push   "python3 bus_push_m…"   Up 2 minutes
```

### 2. 실시간 로그 확인
```bash
./logs.sh
```
**예상 로그:**
```
============================================================
🚌 202번 버스 자동 알림 시스템 시작
📍 정류장: 호반써밋라포레후문 (ID: 223000149)
⏰ 실행 조건: 평일 오전 5:45-6:00, 1분마다
🎯 알림 조건: 가장 빠른 버스가 11분 이하일 때 (단계별 알림)
============================================================
🔄 스케줄러 시작됨 - 2025-07-24 10:15:30

⏰ 2025-07-24 10:15:30 - 202번 버스 확인 중...
❌ 실행 시간이 아닙니다. (평일 오전 5:45-6:00만 실행)
```

## 🕐 자동 시작 설정 (부팅 시 자동 실행)

### systemd 서비스 생성
```bash
# 서비스 파일 생성
sudo nano /etc/systemd/system/bus-push.service
```

**/etc/systemd/system/bus-push.service:**
```ini
[Unit]
Description=202번 버스 알림 시스템
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/home/pi/bus-push
ExecStart=/usr/bin/docker compose up -d
ExecStop=/usr/bin/docker compose down
User=pi

[Install]
WantedBy=multi-user.target
```

### 서비스 활성화
```bash
# 서비스 등록 및 활성화
sudo systemctl daemon-reload
sudo systemctl enable bus-push.service

# 서비스 시작
sudo systemctl start bus-push.service

# 서비스 상태 확인
sudo systemctl status bus-push.service
```

## 🐛 문제 해결

### 도커 권한 오류
```bash
# 사용자를 도커 그룹에 추가 후 재로그인
sudo usermod -aG docker $USER
# 또는 재부팅
sudo reboot
```

### 메모리 부족
```bash
# 스왑 파일 생성 (1GB)
sudo fallocate -l 1G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

# 영구 설정
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

### 시간대 오류
```bash
# 라즈베리파이 시간대 설정
sudo raspi-config
# → Localisation Options → Timezone → Asia → Seoul
```

### OneSignal 푸시 실패
- .env 파일의 APP_ID와 REST_KEY 확인
- OneSignal 대시보드에서 기기 등록 상태 확인

## 📊 시스템 모니터링

### 리소스 사용량 확인
```bash
# 도커 컨테이너 리소스 사용량
docker stats bus-push-system

# 라즈베리파이 전체 리소스
htop
```

### 로그 파일 관리
```bash
# 로그 파일 크기 확인
docker system df

# 오래된 로그 정리
docker system prune -f
```

## 💡 활용 팁

### 1. 원격 모니터링
- SSH로 원격 접속하여 로그 확인
- VNC 활성화하여 GUI로 관리

### 2. 백업
```bash
# 설정 파일 백업
tar -czf bus-push-backup.tar.gz .env docker-compose.yml
```

### 3. 업데이트
```bash
# 코드 업데이트 후
git pull
docker compose up --build -d
```

---

## 🔗 참고 자료

- [라즈베리파이 공식 사이트](https://www.raspberrypi.org/)
- [도커 공식 문서](https://docs.docker.com/)
- [도커 컴포즈 가이드](https://docs.docker.com/compose/)

---

💡 **라즈베리파이에서 24/7 안정적으로 실행되는 202번 버스 알림 시스템을 즐기세요!** 🚌🍓 