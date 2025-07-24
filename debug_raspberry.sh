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
# 실행 중인 컨테이너 확인
if docker compose ps | grep -q "bus-push-system.*Up"; then
    echo "✅ bus-push-system 컨테이너 실행 중"
    docker compose exec bus-push-system env | grep -E "(ONESIGNAL|BUS_API)"
else
    echo "❌ bus-push-system 컨테이너가 실행되지 않음"
    echo "📋 실행 중인 컨테이너:"
    docker compose ps --format "table {{.Name}}\t{{.Status}}"
fi

echo ""
echo "5️⃣ 네트워크 연결 테스트:"
echo "----------------------"
echo "OneSignal API 연결 테스트:"
curl -I https://api.onesignal.com/notifications 2>/dev/null | head -1 || echo "❌ OneSignal API 연결 실패"

echo ""
echo "6️⃣ 푸시 테스트 실행:"
echo "------------------"
# 실행 중인 컨테이너에서 푸시 테스트
if docker compose ps | grep -q "bus-push-system.*Up"; then
    echo "도커 컨테이너 내부에서 푸시 테스트 실행:"
    docker compose exec bus-push-system python3 test_push_only.py
else
    echo "❌ 컨테이너가 실행되지 않아 푸시 테스트 불가"
fi

echo ""
echo "7️⃣ OneSignal API 키 유효성 검사:"
echo "------------------------------"
# OneSignal API 키로 실제 요청 테스트
ONESIGNAL_APP_ID=$(grep ONESIGNAL_APP_ID .env | cut -d'=' -f2)
ONESIGNAL_REST_KEY=$(grep ONESIGNAL_REST_KEY .env | cut -d'=' -f2)

if [ -n "$ONESIGNAL_APP_ID" ] && [ -n "$ONESIGNAL_REST_KEY" ]; then
    echo "🔑 API 키 존재 확인됨"
    echo "📱 APP_ID: ${ONESIGNAL_APP_ID:0:10}..."
    echo "🔐 REST_KEY: ${ONESIGNAL_REST_KEY:0:10}..."
    
    # 간단한 API 테스트
    echo "🧪 OneSignal API 테스트 요청:"
    curl -X POST "https://api.onesignal.com/notifications" \
         -H "Content-Type: application/json" \
         -H "Authorization: Basic $ONESIGNAL_REST_KEY" \
         -d "{\"app_id\":\"$ONESIGNAL_APP_ID\",\"included_segments\":[\"Total Subscriptions\"]}" \
         2>/dev/null | head -c 200 || echo "❌ API 요청 실패"
else
    echo "❌ OneSignal API 키가 설정되지 않음"
fi

echo ""
echo "🔧 문제 해결 방법:"
echo "=================="
echo "1. .env 파일에서 OneSignal API 키 확인"
echo "2. OneSignal 대시보드에서 기기 등록 상태 확인"
echo "3. 휴대폰에서 OneSignal 앱 설치 및 권한 확인"
echo "4. 네트워크 연결 상태 확인"
echo "5. OneSignal API 키가 올바른지 확인" 