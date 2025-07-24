#!/bin/bash

echo "🧪 202번 버스 알림 시스템 테스트 모드 시작"
echo "================================================"

# .env 파일 확인
if [ ! -f ".env" ]; then
    echo "⚠️  .env 파일이 없습니다. env.example을 복사해서 .env 파일을 만들어주세요."
    echo "💡 사용법: cp env.example .env"
    echo "📝 그리고 .env 파일에서 API 키들을 설정해주세요."
    exit 1
fi

# .env 파일 내용 검증
if ! grep -q "BUS_API_KEY=" .env || ! grep -q "ONESIGNAL_APP_ID=" .env; then
    echo "⚠️  .env 파일에 필수 설정이 누락되었습니다."
    echo "📝 다음 항목들을 확인해주세요:"
    echo "   - BUS_API_KEY"
    echo "   - ONESIGNAL_APP_ID"
    echo "   - ONESIGNAL_REST_KEY"
    exit 1
fi

# 로그 디렉토리 생성
mkdir -p logs

# 테스트용 도커 컴포즈로 실행
echo "🧪 테스트 모드 도커 컨테이너 실행 중..."
echo "📋 테스트 설정:"
echo "   - 5분마다 버스 조회"
echo "   - 조건 없이 항상 푸시 발송"
echo "   - 테스트용 메시지 형식"
echo ""

docker compose -f docker-compose.test.yml up -d

echo ""
echo "⏳ 컨테이너 시작 대기 중... (10초)"
sleep 10

echo ""
echo "📊 테스트 컨테이너 상태 확인:"
docker compose -f docker-compose.test.yml ps

echo ""
echo "🔍 헬스체크 확인:"
docker compose -f docker-compose.test.yml ps --format "table {{.Name}}\t{{.Status}}\t{{.Ports}}"

echo ""
echo "📋 유용한 명령어:"
echo "  - 테스트 로그 확인: docker compose -f docker-compose.test.yml logs -f"
echo "  - 실시간 테스트 로그: ./test_logs.sh"
echo "  - 테스트 컨테이너 중지: docker compose -f docker-compose.test.yml down"
echo "  - 테스트 시스템 업데이트: ./test_update.sh"
echo ""
echo "✅ 테스트 시스템이 성공적으로 시작되었습니다!"
echo "🧪 5분마다 버스 정보를 조회하고 푸시를 발송합니다."
echo "⚠️  테스트 완료 후 반드시 ./test_stop.sh로 중지해주세요!" 