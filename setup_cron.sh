#!/bin/bash

# 🕐 Cron 설정 스크립트 - 202번 버스 알림 시스템
# 평일 오전 5:44에 시작, 6:01에 종료

echo "🕐 202번 버스 알림 시스템 Cron 설정"
echo "=================================="

# 현재 crontab 백업
echo "📋 현재 crontab 백업 중..."
crontab -l > crontab_backup_$(date +%Y%m%d_%H%M%S).txt 2>/dev/null || echo "백업할 crontab이 없습니다."

# 프로젝트 디렉토리 경로
PROJECT_DIR="/home/coolmint/bus-push/bus-push"

# 기존 bus-push 관련 cron 작업 제거
echo "🧹 기존 bus-push cron 작업 제거 중..."
(crontab -l 2>/dev/null | grep -v "bus-push") | crontab -

# 새로운 cron 작업 추가
echo "➕ 새로운 cron 작업 추가 중..."

# 평일 오전 5:44에 도커 시작
(crontab -l 2>/dev/null; echo "44 5 * * 1-5 cd $PROJECT_DIR && ./start.sh >> /home/coolmint/bus-push-cron.log 2>&1") | crontab -

# 평일 오전 6:01에 도커 종료  
(crontab -l 2>/dev/null; echo "1 6 * * 1-5 cd $PROJECT_DIR && ./stop.sh >> /home/coolmint/bus-push-cron.log 2>&1") | crontab -

echo "✅ Cron 설정 완료!"
echo ""
echo "📋 설정된 Cron 작업:"
echo "   - 평일 오전 5:44: 도커 시작"
echo "   - 평일 오전 6:01: 도커 종료"
echo ""
echo "📊 현재 crontab 확인:"
crontab -l
echo ""
echo "📝 로그 파일: /home/coolmint/bus-push-cron.log"
echo ""
echo "💡 유용한 명령어:"
echo "   - Cron 로그 확인: tail -f /home/coolmint/bus-push-cron.log"
echo "   - Cron 작업 확인: crontab -l"
echo "   - Cron 서비스 상태: sudo systemctl status cron"
echo ""
echo "⚠️  현재 실행 중인 bus-push 도커 컨테이너를 중지하시겠습니까? (y/n)"
read -r response
if [[ "$response" =~ ^[Yy]$ ]]; then
    echo "🛑 bus-push 도커 컨테이너 중지 중..."
    cd $PROJECT_DIR && ./stop.sh
    echo "✅ bus-push 도커 컨테이너가 중지되었습니다."
    echo "🕐 이제 평일 오전 5:44에 자동으로 시작됩니다!"
else
    echo "ℹ️  bus-push 도커 컨테이너가 계속 실행 중입니다."
fi 