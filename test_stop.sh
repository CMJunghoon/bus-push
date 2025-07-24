#!/bin/bash

echo "🛑 202번 버스 알림 시스템 테스트 모드 중지"
echo "=========================================="

# 현재 실행 중인 테스트 컨테이너 확인
echo "📊 현재 테스트 컨테이너 상태:"
docker compose -f docker-compose.test.yml ps

echo ""
echo "⏹️  테스트 컨테이너 중지 중..."

# 테스트용 도커 컴포즈로 중지
docker compose -f docker-compose.test.yml down

echo ""
echo "✅ 테스트 컨테이너가 성공적으로 중지되었습니다!"
echo "💡 다시 테스트하려면: ./test_start.sh"
echo "💡 실제 시스템 시작: ./start.sh" 