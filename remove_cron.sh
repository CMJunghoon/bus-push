#!/bin/bash

# 🗑️ Cron 설정 제거 스크립트 - 202번 버스 알림 시스템

echo "🗑️ 202번 버스 알림 시스템 Cron 설정 제거"
echo "======================================"

# 현재 crontab 백업
echo "📋 현재 crontab 백업 중..."
crontab -l > crontab_backup_$(date +%Y%m%d_%H%M%S).txt 2>/dev/null || echo "백업할 crontab이 없습니다."

# bus-push 관련 cron 작업 제거
echo "🧹 bus-push cron 작업 제거 중..."
(crontab -l 2>/dev/null | grep -v "bus-push") | crontab -

echo "✅ Cron 설정 제거 완료!"
echo ""
echo "📊 현재 crontab 확인:"
crontab -l
echo ""
echo "💡 Cron 설정이 제거되었습니다."
echo "   - 수동으로 도커를 시작하려면: ./start.sh"
echo "   - 수동으로 도커를 중지하려면: ./stop.sh" 