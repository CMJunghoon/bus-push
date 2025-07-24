#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import json
import urllib.parse
from datetime import datetime


def main():
    """정류장 223000149의 버스 도착 정보 조회"""

    print("=" * 60)
    print("🚌 버스 도착 정보 조회")
    print("📍 정류장 ID: 223000149")
    print(f"⏰ 조회시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    # API 설정
    api_key = "AHjKW+qu2/FOtF3rr3+d0PYHm1ItUYDCyaq2RYkUqrCMb0pY42Q20KMMZGV5PBHLFkZqZWwXiPVz5riNMKeV4A=="
    url = "https://apis.data.go.kr/6410000/busarrivalservice/v2/getBusArrivalListv2"

    params = {"format": "json", "serviceKey": api_key, "stationId": "223000149"}

    # URL 생성
    encoded_params = urllib.parse.urlencode(params)
    full_url = f"{url}?{encoded_params}"

    print(f"🔍 API 호출 중...")
    print(f"URL: {url}")
    print(f"정류장 ID: 223000149")

    try:
        # curl 명령 실행
        result = subprocess.run(
            ["curl", "-k", "-s", full_url], capture_output=True, text=True, timeout=15
        )

        if result.returncode == 0 and result.stdout:
            print("✅ API 호출 성공!")

            try:
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
                            print(f"\n🚌 202번 버스 도착 정보:")

                            for bus in bus_202_list:
                                route_name = bus.get("routeName", "N/A")
                                predict_time1 = bus.get("predictTime1", "N/A")
                                predict_time2 = bus.get("predictTime2", "N/A")
                                plate_no1 = bus.get("plateNo1", "N/A")
                                plate_no2 = bus.get("plateNo2", "N/A")
                                location1 = bus.get("locationNo1", "N/A")
                                location2 = bus.get("locationNo2", "N/A")
                                dest_name = bus.get("routeDestName", "N/A")

                                print(f"\n   🎯 202번 버스:")
                                print(f"      - 종점: {dest_name}")
                                print(f"      - 도착예정시간1: {predict_time1}분 후")
                                print(f"      - 도착예정시간2: {predict_time2}분 후")
                                print(f"      - 차량번호1: {plate_no1}")
                                print(f"      - 차량번호2: {plate_no2}")
                                print(f"      - 현재위치1: {location1}번째 전")
                                print(f"      - 현재위치2: {location2}번째 전")

                                # 상세 정보 출력
                                print(f"\n   📋 상세 정보:")
                                print(f"      - 노선 ID: {bus.get('routeId', 'N/A')}")
                                print(
                                    f"      - 정류장 순번: {bus.get('staOrder', 'N/A')}"
                                )
                                print(
                                    f"      - 저상버스1: {'예' if bus.get('lowPlate1') == 1 else '아니오'}"
                                )
                                print(
                                    f"      - 저상버스2: {'예' if bus.get('lowPlate2') == 1 else '아니오'}"
                                )

                                # 202번 버스 원본 데이터 출력
                                print(f"\n   📋 202번 버스 원본 데이터:")
                                print(json.dumps(bus, ensure_ascii=False, indent=2))
                        else:
                            print(f"\n❌ 202번 버스가 이 정류장에 없습니다.")

                            # 다른 버스들 간단히 표시
                            other_buses = [
                                str(bus.get("routeName", "N/A"))
                                for bus in bus_list
                                if str(bus.get("routeName", "")) != "202"
                            ]
                            if other_buses:
                                print(
                                    f"   📋 이 정류장의 다른 버스: {', '.join(other_buses)}"
                                )
                    else:
                        print("\n❌ 버스 도착 정보가 없습니다.")
                else:
                    print("\n❌ 응답 구조를 파싱할 수 없습니다.")

            except json.JSONDecodeError:
                print("❌ JSON 파싱 실패")
                print(f"응답 내용: {result.stdout}")

        else:
            print(f"❌ API 호출 실패")
            if result.stderr:
                print(f"오류: {result.stderr}")

    except Exception as e:
        print(f"❌ 오류 발생: {e}")


if __name__ == "__main__":
    main()
