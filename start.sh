#!/bin/bash

echo "🍓 라즈베리파이 202번 버스 알림 시스템 시작"
echo "================================================"

# .env 파일 확인
if [ ! -f ".env" ]; then
    echo "⚠️  .env 파일이 없습니다. env.example을 복사해서 .env 파일을 만들어주세요."
    echo "💡 사용법: cp env.example .env"
    echo "📝 그리고 .env 파일에서 OneSignal 설정을 수정해주세요."
    exit 1
fi

# 로그 디렉토리 생성
mkdir -p logs

# 도커 컴포즈로 실행
echo "🐳 도커 컨테이너 빌드 및 실행 중..."
docker-compose up --build -d

echo "✅ 컨테이너가 성공적으로 시작되었습니다!"
echo ""
echo "📊 컨테이너 상태 확인:"
docker-compose ps

echo ""
echo "📋 유용한 명령어:"
echo "  - 로그 확인: docker-compose logs -f"
echo "  - 컨테이너 중지: docker-compose down"
echo "  - 컨테이너 재시작: docker-compose restart" 