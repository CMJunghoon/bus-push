#!/bin/bash

echo "🔄 202번 버스 알림 시스템 업데이트"
echo "=================================="

# 현재 실행 중인 컨테이너 중지
echo "⏹️  현재 시스템 중지 중..."
docker-compose down

# 최신 코드 가져오기
echo "📥 최신 코드 가져오는 중..."
git pull origin main

if [ $? -eq 0 ]; then
    echo "✅ 코드 업데이트 성공!"
    
    # 새 이미지로 재빌드 및 시작
    echo "🔨 새 이미지 빌드 및 시작 중..."
    docker-compose up --build -d
    
    echo "🎉 업데이트 완료!"
    echo ""
    echo "📊 컨테이너 상태:"
    docker-compose ps
else
    echo "❌ 코드 업데이트 실패!"
    echo "💡 수동으로 해결이 필요합니다."
    
    # 기존 컨테이너 다시 시작
    echo "🔄 기존 시스템 재시작 중..."
    docker-compose up -d
fi 