#!/bin/bash

echo "📋 202번 버스 알림 시스템 로그"
echo "=============================="

# 컨테이너 상태 먼저 확인
echo "📊 컨테이너 상태:"
docker compose ps

echo ""
echo "📋 최근 로그 (마지막 20줄):"
docker compose logs --tail=20

echo ""
echo "🔄 실시간 로그 시작... (Ctrl+C로 종료)"
echo "=================================="

# 실시간 로그 확인
docker compose logs -f 