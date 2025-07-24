#!/bin/bash

echo "🔄 202번 버스 알림 시스템 업데이트"
echo "=================================="

# 현재 실행 중인 컨테이너 상태 확인
echo "📊 업데이트 전 상태:"
docker compose ps

# 현재 실행 중인 컨테이너 중지
echo ""
echo "⏹️  현재 시스템 중지 중..."
docker compose down

# 최신 코드 가져오기
echo ""
echo "📥 GitHub에서 최신 코드 가져오는 중..."
git pull origin main

if [ $? -eq 0 ]; then
    echo "✅ 코드 업데이트 성공!"
    
    # 새 이미지로 재빌드 및 시작
    echo ""
    echo "🔨 새 이미지 빌드 및 시작 중..."
    docker compose up --build -d
    
    # 시작 대기
    echo ""
    echo "⏳ 컨테이너 시작 대기 중... (10초)"
    sleep 10
    
    echo ""
    echo "🎉 업데이트 완료!"
    echo ""
    echo "📊 업데이트 후 컨테이너 상태:"
    docker compose ps
    
    echo ""
    echo "🔍 헬스체크 확인:"
    docker compose ps --format "table {{.Name}}\t{{.Status}}\t{{.Ports}}"
    
else
    echo "❌ 코드 업데이트 실패!"
    echo "💡 수동으로 해결이 필요합니다."
    
    # 기존 컨테이너 다시 시작
    echo ""
    echo "🔄 기존 시스템 재시작 중..."
    docker compose up -d
    
    echo ""
    echo "📊 재시작 후 상태:"
    docker compose ps
fi 