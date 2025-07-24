#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔑 OneSignal API 키 유효성 테스트
API 키가 올바른지 직접 확인
"""

import os
import requests
import json


def test_onesignal_api():
    """OneSignal API 키 테스트"""
    print("🔑 OneSignal API 키 유효성 테스트")
    print("=" * 50)

    # 환경변수에서 API 키 가져오기
    app_id = os.getenv("ONESIGNAL_APP_ID")
    rest_key = os.getenv("ONESIGNAL_REST_KEY")

    print(f"📱 APP_ID: {app_id[:10] if app_id else 'None'}...")
    print(f"🔐 REST_KEY: {rest_key[:10] if rest_key else 'None'}...")

    if not app_id or not rest_key:
        print("❌ OneSignal API 키가 설정되지 않았습니다!")
        return False

    # 1. 앱 정보 조회 테스트
    print("\n1️⃣ 앱 정보 조회 테스트:")
    try:
        url = f"https://api.onesignal.com/apps/{app_id}"
        headers = {
            "Authorization": f"Basic {rest_key}",
            "Content-Type": "application/json",
        }

        response = requests.get(url, headers=headers, timeout=10)
        print(f"   상태 코드: {response.status_code}")

        if response.status_code == 200:
            app_data = response.json()
            print(f"   ✅ 앱 정보 조회 성공!")
            print(f"   📱 앱 이름: {app_data.get('name', 'N/A')}")
            print(f"   🆔 앱 ID: {app_data.get('id', 'N/A')}")
        else:
            print(f"   ❌ 앱 정보 조회 실패: {response.text}")
            return False

    except Exception as e:
        print(f"   ❌ 앱 정보 조회 오류: {e}")
        return False

    # 2. 구독자 목록 조회 테스트
    print("\n2️⃣ 구독자 목록 조회 테스트:")
    try:
        url = "https://api.onesignal.com/players"
        params = {"app_id": app_id, "limit": 1}
        headers = {
            "Authorization": f"Basic {rest_key}",
            "Content-Type": "application/json",
        }

        response = requests.get(url, headers=headers, params=params, timeout=10)
        print(f"   상태 코드: {response.status_code}")

        if response.status_code == 200:
            players_data = response.json()
            total_count = players_data.get("total_count", 0)
            print(f"   ✅ 구독자 목록 조회 성공!")
            print(f"   👥 총 구독자 수: {total_count}")

            if total_count == 0:
                print("   ⚠️  등록된 구독자가 없습니다!")
                print("   💡 휴대폰에서 OneSignal 앱을 설치하고 기기를 등록해주세요.")
        else:
            print(f"   ❌ 구독자 목록 조회 실패: {response.text}")

    except Exception as e:
        print(f"   ❌ 구독자 목록 조회 오류: {e}")

    # 3. 테스트 푸시 발송
    print("\n3️⃣ 테스트 푸시 발송:")
    try:
        url = "https://api.onesignal.com/notifications"
        headers = {
            "Authorization": f"Basic {rest_key}",
            "Content-Type": "application/json",
        }

        # 테스트 푸시 데이터
        data = {
            "app_id": app_id,
            "headings": {"en": "API Test"},
            "contents": {"en": "OneSignal API key is working correctly!"},
            "ios_badgeType": "Increase",
            "ios_badgeCount": 1,
            "include_aliases": {
                "onesignal_id": [
                    "27d455a0-9ce9-4d4f-bbd2-fe68810fd5f1",
                ]
            },
        }

        response = requests.post(url, headers=headers, json=data, timeout=10)
        print(f"   상태 코드: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ 테스트 푸시 발송 성공!")
            print(f"   📊 응답: {json.dumps(result, ensure_ascii=False, indent=2)}")
            return True
        else:
            print(f"   ❌ 테스트 푸시 발송 실패: {response.text}")
            return False

    except Exception as e:
        print(f"   ❌ 테스트 푸시 발송 오류: {e}")
        return False


def main():
    """메인 함수"""
    success = test_onesignal_api()

    print("\n" + "=" * 50)
    if success:
        print("🎉 OneSignal API 키가 정상 작동합니다!")
        print("📱 휴대폰에서 테스트 알림을 확인해보세요.")
    else:
        print("❌ OneSignal API 키에 문제가 있습니다.")
        print("🔧 다음을 확인해주세요:")
        print("   1. .env 파일의 API 키가 올바른지")
        print("   2. OneSignal 대시보드에서 앱이 활성화되어 있는지")
        print("   3. 휴대폰에 OneSignal 앱이 설치되어 있는지")


if __name__ == "__main__":
    main()
