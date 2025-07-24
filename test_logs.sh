#!/bin/bash

echo "📋 202번 버스 알림 시스템 테스트 모드 로그"
echo "=========================================="

# 테스트 컨테이너 상태 먼저 확인
echo "📊 테스트 컨테이너 상태:"
docker compose -f docker-compose.test.yml ps

echo ""
echo "📋 최근 테스트 로그 (마지막 20줄):"
docker compose -f docker-compose.test.yml logs --tail=20

echo ""
echo "🔄 실시간 테스트 로그 시작... (Ctrl+C로 종료)"
echo "=============================================="

# 실시간 테스트 로그 확인
docker compose -f docker-compose.test.yml logs -f 