#!/bin/bash

echo "🔍 라즈베리파이 푸시 알림 문제 진단"
echo "===================================="

echo ""
echo "1️⃣ 환경변수 확인:"
echo "------------------"
if [ -f ".env" ]; then
    echo "✅ .env 파일 존재"
    echo "📋 .env 파일 내용:"
    cat .env | sed 's/=.*/=***/'  # API 키는 가려서 표시
else
    echo "❌ .env 파일 없음"
    exit 1
fi

echo ""
echo "2️⃣ 도커 컨테이너 상태:"
echo "---------------------"
docker compose ps

echo ""
echo "3️⃣ 도커 로그 확인 (최근 20줄):"
echo "------------------------------"
docker compose logs --tail=20

echo ""
echo "4️⃣ OneSignal 설정 확인:"
echo "----------------------"
# 도커 컨테이너 내부에서 환경변수 확인
docker compose exec bus-push-system env | grep -E "(ONESIGNAL|BUS_API)" || echo "❌ 컨테이너가 실행되지 않음"

echo ""
echo "5️⃣ 네트워크 연결 테스트:"
echo "----------------------"
echo "OneSignal API 연결 테스트:"
curl -I https://api.onesignal.com/notifications 2>/dev/null | head -1 || echo "❌ OneSignal API 연결 실패"

echo ""
echo "6️⃣ 푸시 테스트 실행:"
echo "------------------"
echo "도커 컨테이너 내부에서 푸시 테스트 실행:"
docker compose exec bus-push-system python3 test_push_only.py 2>/dev/null || echo "❌ 푸시 테스트 실패"

echo ""
echo "🔧 문제 해결 방법:"
echo "=================="
echo "1. .env 파일에서 OneSignal API 키 확인"
echo "2. OneSignal 대시보드에서 기기 등록 상태 확인"
echo "3. 휴대폰에서 OneSignal 앱 설치 및 권한 확인"
echo "4. 네트워크 연결 상태 확인" 