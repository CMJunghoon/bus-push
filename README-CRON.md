# 🕐 Cron 설정 가이드 - 202번 버스 알림 시스템

## 📋 개요

Cron을 사용하여 평일 오전 5:44-6:01 시간대에만 bus-push 도커 컨테이너를 실행하고, 나머지 시간에는 완전히 중지하여 시스템 리소스를 절약합니다. 다른 도커 컨테이너들은 영향을 받지 않습니다.

## 🎯 설정 내용

- **시작 시간**: 평일 오전 5:44
- **종료 시간**: 평일 오전 6:01  
- **실행 시간**: 총 17분 (매일)
- **절약 시간**: 23시간 43분 (매일)

## 🚀 설정 방법

### 1. Cron 설정 스크립트 실행

```bash
# 라즈베리파이에서 실행
chmod +x setup_cron.sh
./setup_cron.sh
```

### 2. 수동 설정 (스크립트 없이)

```bash
# crontab 편집
crontab -e

# 다음 내용 추가:
44 5 * * 1-5 cd /home/coolmint/bus-push/bus-push && ./start.sh >> /home/coolmint/bus-push-cron.log 2>&1
1 6 * * 1-5 cd /home/coolmint/bus-push/bus-push && ./stop.sh >> /home/coolmint/bus-push-cron.log 2>&1
```

## 📊 관리 명령어

### Cron 상태 확인
```bash
./check_cron.sh
```

### Cron 설정 제거
```bash
./remove_cron.sh
```

### 수동 명령어
```bash
# 현재 crontab 확인
crontab -l

# Cron 로그 확인
tail -f /home/coolmint/bus-push-cron.log

# Cron 서비스 상태 확인
sudo systemctl status cron
```

## 💾 리소스 절약 효과

### 메모리 절약
- **bus-push 도커 실행 시**: ~50-100MB
- **bus-push 도커 중지 시**: ~0MB
- **일일 절약**: ~1.1-2.3GB

### 전력 절약
- **bus-push 도커 실행 시**: 지속적인 CPU 사용
- **bus-push 도커 중지 시**: 거의 0% CPU 사용
- **예상 절약**: 상당한 전력 절약

## ⚠️ 주의사항

1. **시간 정확성**: 라즈베리파이의 시간이 정확한지 확인
2. **네트워크 연결**: 시작 시 인터넷 연결 필요
3. **로그 모니터링**: 정기적으로 로그 확인 권장

## 🔧 문제 해결

### Cron이 실행되지 않는 경우
```bash
# Cron 서비스 상태 확인
sudo systemctl status cron

# Cron 서비스 재시작
sudo systemctl restart cron

# 로그 확인
tail -f /home/coolmint/bus-push-cron.log
```

### 수동으로 bus-push 도커 시작/중지
```bash
# bus-push 도커 시작
./start.sh

# bus-push 도커 중지
./stop.sh
```

## 📅 Cron 표현식 설명

```
44 5 * * 1-5
│  │ │ │ │
│  │ │ │ └── 요일 (1-5 = 월-금)
│  │ │ └──── 월 (모든 월)
│  │ └────── 일 (모든 일)
│  └──────── 시간 (5시)
└─────────── 분 (44분)
```

## 🎉 완료!

Cron 설정이 완료되면:
- ✅ 평일 오전 5:44에 자동으로 도커 시작
- ✅ 평일 오전 6:01에 자동으로 도커 종료
- ✅ 23시간 43분 동안 시스템 리소스 절약
- ✅ 매일 정확한 시간에 푸시 알림 수신 