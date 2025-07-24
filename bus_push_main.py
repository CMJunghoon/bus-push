#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import json
import urllib.parse
import asyncio
import time
import schedule
import os
from datetime import datetime, time as dt_time
from dotenv import load_dotenv
from push_notification import PushAPI

# .env 파일 로드
load_dotenv()


def get_bus_info(station_id="223000149"):
    """버스 도착 정보 조회"""

    # API 설정 (환경변수에서 가져오기)
    api_key = os.getenv("BUS_API_KEY")
    if not api_key:
        print("❌ BUS_API_KEY 환경변수가 설정되지 않았습니다.")
        print("💡 .env 파일을 생성하고 BUS_API_KEY를 설정해주세요.")
        return None
    url = "https://apis.data.go.kr/6410000/busarrivalservice/v2/getBusArrivalListv2"

    params = {"format": "json", "serviceKey": api_key, "stationId": station_id}

    # URL 생성
    encoded_params = urllib.parse.urlencode(params)
    full_url = f"{url}?{encoded_params}"

    try:
        # curl 명령 실행
        result = subprocess.run(
            ["curl", "-k", "-s", full_url], capture_output=True, text=True, timeout=15
        )

        if result.returncode == 0 and result.stdout:
            data = json.loads(result.stdout)

            # 버스 도착 정보 추출
            if "response" in data and "msgBody" in data["response"]:
                bus_list = data["response"]["msgBody"].get("busArrivalList")

                if bus_list:
                    # 202번 버스만 필터링
                    bus_202_list = [
                        bus
                        for bus in bus_list
                        if str(bus.get("routeName", "")) == "202"
                    ]

                    if bus_202_list:
                        return bus_202_list[0]  # 첫 번째 202번 버스 정보 반환

        return None

    except Exception as e:
        print(f"❌ 버스 정보 조회 오류: {e}")
        return None


def should_send_push(bus_info):
    """푸시 알림을 보낼지 판단하는 로직"""

    if not bus_info:
        return False, "버스 정보 없음"

    predict_time1 = bus_info.get("predictTime1")
    predict_time2 = bus_info.get("predictTime2")

    # 도착 시간이 숫자인지 확인
    try:
        time1 = int(predict_time1) if predict_time1 else None
        time2 = int(predict_time2) if predict_time2 else None
    except (ValueError, TypeError):
        return False, "도착 시간 정보 없음"

        # 푸시 알림 조건: 가장 빠른 버스가 11분 이하일 때
    if time1 is not None and time1 <= 11:
        if time1 <= 1:
            return True, f"🚨 긴급! 202번 버스가 {time1}분 후 도착합니다!"
        elif time1 <= 3:
            return True, f"🔥 곧 도착! 202번 버스가 {time1}분 후 도착합니다!"
        else:
            return True, f"🚌 202번 버스가 {time1}분 후 도착합니다!"

    return False, f"알림 조건 불충족 ({time1}분 > 11분)"


def format_bus_message(bus_info):
    """버스 정보를 메시지로 포맷팅"""

    predict_time1 = bus_info.get("predictTime1", "N/A")
    predict_time2 = bus_info.get("predictTime2", "N/A")
    location1 = bus_info.get("locationNo1", "N/A")
    location2 = bus_info.get("locationNo2", "N/A")
    plate_no1 = bus_info.get("plateNo1", "")
    plate_no2 = bus_info.get("plateNo2", "")

    message = ""

    # 첫 번째 버스 정보
    bus1_name = plate_no1 if plate_no1 else "202번"
    message += f"🚌 {bus1_name}: {predict_time1}분후"
    if location1 and str(location1) != "N/A" and str(location1) != "":
        message += f" ( {location1}전 )"

    # 두 번째 버스 정보
    if predict_time2 and str(predict_time2) != "" and str(predict_time2) != "N/A":
        bus2_name = plate_no2 if plate_no2 else "202번"
        message += f"\n🚌 {bus2_name}: {predict_time2}분후"
        if location2 and str(location2) != "N/A" and str(location2) != "":
            message += f" ( {location2}전 )"

    return message


def is_weekday():
    """평일인지 확인하는 함수 (월요일=0, 일요일=6)"""
    return datetime.now().weekday() < 5  # 0-4가 평일


def is_target_time():
    """현재 시간이 평일 오전 5:45-6:00 사이인지 확인"""
    if not is_weekday():
        return False

    now = datetime.now().time()
    start_time = dt_time(5, 45)  # 오전 5시 45분
    end_time = dt_time(6, 0)  # 오전 6시

    return start_time <= now <= end_time


async def check_bus():
    """버스 정보를 확인하고 필요시 푸시 알림 전송"""

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n⏰ {current_time} - 202번 버스 확인 중...")

    # 평일 오전 5:45-6:00 시간대가 아니면 실행하지 않음 (테스트용 주석처리)
    # if not is_target_time():
    #     print("❌ 실행 시간이 아닙니다. (평일 오전 5:45-6:00만 실행)")
    #     return

    # 1. 버스 정보 조회
    bus_info = get_bus_info()

    if not bus_info:
        print("❌ 202번 버스 정보를 찾을 수 없습니다.")
        return

    # 2. 버스 정보 표시
    predict_time1 = bus_info.get("predictTime1", "N/A")
    predict_time2 = bus_info.get("predictTime2", "N/A")
    dest_name = bus_info.get("routeDestName", "N/A")
    plate_no1 = bus_info.get("plateNo1", "N/A")

    print(f"✅ 202번 버스 발견!")
    print(f"   - 종점: {dest_name}")
    print(f"   - 도착예정시간1: {predict_time1}분 후")
    print(f"   - 도착예정시간2: {predict_time2}분 후")
    print(f"   - 차량번호: {plate_no1}")

    # 3. 푸시 알림 조건 확인 (테스트용: 항상 푸시 발송)
    # should_push, reason = should_send_push(bus_info)
    # print(f"📱 푸시 알림 판단: {reason}")

    # 테스트용: 항상 푸시 발송
    should_push = True
    print(f"📱 푸시 알림 판단: 테스트 모드 - 항상 발송")

    if should_push:
        # 4. 푸시 알림 전송
        title = "202번 버스, 호반써밋라포레후문 정류장"
        message = format_bus_message(bus_info)

        print(f"🔔 푸시 알림 전송 중...")
        print(f"제목: {title}")
        print(f"내용:\n{message}")

        # 실제 푸시 전송
        success = await PushAPI.send(title, message)

        if success:
            print("🎉 푸시 알림 전송 완료!")
        else:
            print("😞 푸시 알림 전송 실패!")
    else:
        print(f"💤 푸시 알림을 보내지 않습니다.")


def run_scheduler():
    """스케줄러 실행"""
    print("=" * 60)
    print("🚌 202번 버스 자동 알림 시스템 시작")
    print("📍 정류장: 호반써밋라포레후문 (ID: 223000149)")
    print("⏰ 실행 조건: 테스트 모드 - 1분마다 (시간 제한 없음)")
    print("🎯 알림 조건: 테스트 모드 - 항상 푸시 발송")
    print("=" * 60)

    # 매분마다 실행하도록 스케줄 설정
    schedule.every().minute.do(lambda: asyncio.run(check_bus()))

    print(f"🔄 스케줄러 시작됨 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    try:
        while True:
            schedule.run_pending()
            time.sleep(1)  # 1초마다 스케줄 확인
    except KeyboardInterrupt:
        print("\n⏹️  스케줄러 중지됨")


async def main():
    """메인 함수 - 일회성 실행용"""

    print("=" * 60)
    print("🚌 202번 버스 푸시 알림 시스템 (일회성 실행)")
    print("📍 정류장: 호반써밋라포레후문 (ID: 223000149)")
    print(f"⏰ 실행시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    await check_bus()


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--schedule":
        # 스케줄러 모드
        run_scheduler()
    else:
        # 일회성 실행 모드
        asyncio.run(main())
