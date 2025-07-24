#!/bin/bash

# 📊 Cron 설정 확인 스크립트 - 202번 버스 알림 시스템

echo "📊 202번 버스 알림 시스템 Cron 상태 확인"
echo "======================================"

echo "🕐 현재 시간: $(date)"
echo ""

echo "📋 현재 crontab:"
crontab -l 2>/dev/null || echo "설정된 crontab이 없습니다."
echo ""

echo "🐳 bus-push 도커 컨테이너 상태:"
docker compose ps 2>/dev/null | grep bus-push || echo "bus-push 도커가 실행되지 않았거나 프로젝트 디렉토리가 아닙니다."
echo ""

echo "📝 Cron 로그 (최근 10줄):"
if [ -f "/home/coolmint/bus-push-cron.log" ]; then
    tail -10 /home/coolmint/bus-push-cron.log
else
    echo "Cron 로그 파일이 없습니다."
fi
echo ""

echo "🔧 Cron 서비스 상태:"
sudo systemctl status cron --no-pager -l 2>/dev/null || echo "Cron 서비스 상태를 확인할 수 없습니다."
echo ""

echo "💡 다음 실행 예정:"
echo "   - 평일 오전 5:44: 도커 시작"
echo "   - 평일 오전 6:01: 도커 종료"
echo ""
echo "📅 오늘은 $(date +%A)입니다."
if [[ $(date +%u) -ge 1 && $(date +%u) -le 5 ]]; then
    echo "✅ 오늘은 평일입니다. Cron이 정상 작동합니다."
else
    echo "ℹ️  오늘은 주말입니다. Cron이 실행되지 않습니다."
fi 