#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 202번 버스 알림 시스템 테스트 버전
5분마다 버스 조회하고 푸시 발송 (11분 이하 조건 제거)
"""

import os
import asyncio
import time
import json
import subprocess
from datetime import datetime
from push_notification import PushAPI


def get_bus_info():
    """버스 도착 정보 조회"""
    try:
        api_key = os.getenv("BUS_API_KEY")
        if not api_key:
            print("❌ BUS_API_KEY 환경변수가 설정되지 않았습니다.")
            return None

        # API URL 구성
        base_url = (
            "https://apis.data.go.kr/6410000/busarrivalservice/v2/getBusArrivalItemv2"
        )
        params = {
            "serviceKey": api_key,
            "stationId": "223000149",  # 호반써밋라포레후문
            "routeId": "203000069",  # 202번 버스
            "staOrder": "19",
            "format": "json",
        }

        # URL 인코딩
        from urllib.parse import urlencode

        query_string = urlencode(params)
        full_url = f"{base_url}?{query_string}"

        print(f"🔍 API 호출: {full_url[:100]}...")

        # curl을 사용하여 API 호출 (SSL 문제 해결)
        result = subprocess.run(
            ["curl", "-k", "-s", full_url], capture_output=True, text=True, timeout=10
        )

        if result.returncode != 0:
            print(f"❌ API 호출 실패: {result.stderr}")
            return None

        # JSON 파싱
        data = json.loads(result.stdout)

        if "response" not in data or "body" not in data["response"]:
            print(f"❌ API 응답 형식 오류: {data}")
            return None

        items = data["response"]["body"].get("items", [])
        if not items:
            print("❌ 버스 정보가 없습니다.")
            return None

        return items[0]  # 첫 번째 버스 정보 반환

    except Exception as e:
        print(f"❌ 버스 정보 조회 오류: {e}")
        return None


def format_bus_message(bus_info):
    """버스 정보를 메시지로 포맷팅"""
    predict_time1 = bus_info.get("predictTime1", "N/A")
    predict_time2 = bus_info.get("predictTime2", "N/A")
    location1 = bus_info.get("locationNo1", "N/A")
    location2 = bus_info.get("locationNo2", "N/A")
    plate_no1 = bus_info.get("plateNo1", "")
    plate_no2 = bus_info.get("plateNo2", "")

    message = f"🧪 테스트 - 호반써밋라포레후문 정류장\n"

    bus1_name = plate_no1 if plate_no1 else "202번"
    message += f"🚌 {bus1_name}: {predict_time1}분후"
    if location1 and str(location1) != "N/A" and str(location1) != "":
        message += f" ( {location1}전 )"

    if predict_time2 and str(predict_time2) != "" and str(predict_time2) != "N/A":
        bus2_name = plate_no2 if plate_no2 else "202번"
        message += f"\n🚌 {bus2_name}: {predict_time2}분후"
        if location2 and str(location2) != "N/A" and str(location2) != "":
            message += f" ( {location2}전 )"

    return message


async def send_test_push(bus_info):
    """테스트 푸시 발송"""
    try:
        message = format_bus_message(bus_info)
        title = "🧪 202번 버스 테스트 알림"

        print(f"📱 푸시 발송 시도...")
        print(f"제목: {title}")
        print(f"내용: {message}")

        success = await PushAPI.send(title, message)

        if success:
            print("✅ 푸시 발송 성공!")
        else:
            print("❌ 푸시 발송 실패!")

        return success

    except Exception as e:
        print(f"❌ 푸시 발송 오류: {e}")
        return False


async def test_bus_check():
    """테스트용 버스 체크 및 푸시 발송"""
    print(f"\n🕐 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - 테스트 시작")
    print("=" * 60)

    # 버스 정보 조회
    bus_info = get_bus_info()

    if bus_info:
        print("✅ 버스 정보 조회 성공!")
        print(f"첫 번째 버스: {bus_info.get('predictTime1', 'N/A')}분 후")
        print(f"두 번째 버스: {bus_info.get('predictTime2', 'N/A')}분 후")

        # 푸시 발송 (조건 없이 항상 발송)
        await send_test_push(bus_info)

    else:
        print("❌ 버스 정보 조회 실패!")

    print("=" * 60)


async def run_test_scheduler():
    """테스트 스케줄러 실행"""
    print("🧪 202번 버스 알림 시스템 테스트 모드 시작!")
    print("📋 설정:")
    print("   - 5분마다 버스 조회")
    print("   - 조건 없이 항상 푸시 발송")
    print("   - 테스트용 메시지 형식")
    print("=" * 60)

    # 즉시 첫 번째 테스트 실행
    await test_bus_check()

    # 5분마다 반복
    while True:
        print(
            f"\n⏰ 다음 테스트까지 5분 대기 중... ({datetime.now().strftime('%H:%M:%S')})"
        )
        await asyncio.sleep(300)  # 5분 = 300초
        await test_bus_check()


def main():
    """메인 함수"""
    print("🧪 202번 버스 알림 시스템 테스트 버전")
    print("=" * 50)

    # 환경변수 확인
    required_vars = ["BUS_API_KEY", "ONESIGNAL_APP_ID", "ONESIGNAL_REST_KEY"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]

    if missing_vars:
        print("❌ 필수 환경변수가 설정되지 않았습니다:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\n💡 .env 파일을 확인해주세요.")
        return

    print("✅ 모든 환경변수가 설정되었습니다!")

    try:
        # 테스트 스케줄러 실행
        asyncio.run(run_test_scheduler())
    except KeyboardInterrupt:
        print("\n\n🛑 테스트 모드 종료")
    except Exception as e:
        print(f"\n❌ 테스트 실행 오류: {e}")


if __name__ == "__main__":
    main()
