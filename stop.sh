#!/bin/bash

echo "🛑 202번 버스 알림 시스템 중지"
echo "==============================="

# 현재 실행 중인 컨테이너 확인
echo "📊 현재 컨테이너 상태:"
docker compose ps

echo ""
echo "⏹️  컨테이너 중지 중..."

# 도커 컴포즈로 중지
docker compose down

echo ""
echo "✅ 컨테이너가 성공적으로 중지되었습니다!"
echo "💡 다시 시작하려면: ./start.sh 또는 docker compose up -d" 