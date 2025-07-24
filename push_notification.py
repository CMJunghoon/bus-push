#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import asyncio
import os
from typing import Optional


class PushAPI:
    """OneSignal 푸시 알림 API 클래스"""

    # OneSignal 설정값 (환경변수 또는 기본값)
    APP_ID = os.getenv("ONESIGNAL_APP_ID")
    REST_KEY = os.getenv("ONESIGNAL_REST_KEY")

    @staticmethod
    async def send(title: str, message: str) -> bool:
        """푸시 알림 전송

        Args:
            title: 알림 제목
            message: 알림 내용

        Returns:
            bool: 전송 성공 여부
        """
        # 환경변수 체크
        if not PushAPI.APP_ID or not PushAPI.REST_KEY:
            print("❌ OneSignal 환경변수가 설정되지 않았습니다.")
            print(
                "💡 .env 파일에서 ONESIGNAL_APP_ID와 ONESIGNAL_REST_KEY를 설정해주세요."
            )
            return False

        try:
            # 요청 파라미터 설정
            parameters = {
                "app_id": PushAPI.APP_ID,
                "headings": {"en": title},
                "contents": {"en": message},
                "ios_badgeType": "Increase",
                "ios_badgeCount": 1,
                "include_aliases": {
                    "onesignal_id": [
                        "27d455a0-9ce9-4d4f-bbd2-fe68810fd5f1",
                    ]
                },
            }

            # 헤더 설정
            headers = {
                "Content-Type": "application/json",
                "accept": "application/json",
                "Authorization": f"Basic {PushAPI.REST_KEY}",
            }

            # API 요청
            url = "https://api.onesignal.com/notifications"

            # asyncio를 사용한 비동기 요청
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: requests.post(
                    url, headers=headers, json=parameters, timeout=30
                ),
            )

            if response.status_code == 200:
                response_data = response.json()
                msg = message.strip()
                print(f"✅ Notification 성공: {title} - {msg}")
                print(
                    f"📊 응답 데이터: {json.dumps(response_data, ensure_ascii=False, indent=2)}"
                )
                return True
            else:
                print(f"❌ Notification 실패: HTTP {response.status_code}")
                print(f"응답 내용: {response.text}")
                return False

        except Exception as error:
            print(f"❌ Notification 실패: {str(error)}")
            return False


# 동기 버전 (필요한 경우)
class PushAPISync:
    """OneSignal 푸시 알림 API 클래스 (동기 버전)"""

    APP_ID = "your_app_id_here"
    REST_KEY = "your_rest_key_here"

    @staticmethod
    def send(title: str, message: str) -> bool:
        """푸시 알림 전송 (동기)

        Args:
            title: 알림 제목
            message: 알림 내용

        Returns:
            bool: 전송 성공 여부
        """
        try:
            # 요청 파라미터 설정
            parameters = {
                "app_id": PushAPISync.APP_ID,
                "headings": {"en": title},
                "contents": {"en": message},
                "ios_badgeType": "Increase",
                "ios_badgeCount": 1,
                "include_aliases": {
                    "onesignal_id": [
                        "27d455a0-9ce9-4d4f-bbd2-fe68810fd5f1",
                    ]
                },
            }

            # 헤더 설정
            headers = {
                "Content-Type": "application/json",
                "accept": "application/json",
                "Authorization": f"Basic {PushAPISync.REST_KEY}",
            }

            # API 요청
            url = "https://api.onesignal.com/notifications"
            response = requests.post(url, headers=headers, json=parameters, timeout=30)

            if response.status_code == 200:
                response_data = response.json()
                msg = message.strip()
                print(f"✅ Notification 성공: {title} - {msg}")
                print(
                    f"📊 응답 데이터: {json.dumps(response_data, ensure_ascii=False, indent=2)}"
                )
                return True
            else:
                print(f"❌ Notification 실패: HTTP {response.status_code}")
                print(f"응답 내용: {response.text}")
                return False

        except Exception as error:
            print(f"❌ Notification 실패: {str(error)}")
            return False


# 테스트 함수
async def test_push_notification():
    """푸시 알림 테스트"""
    print("🔔 푸시 알림 테스트 시작...")

    title = "202번 버스 알림"
    message = "202번 버스가 1분 후 도착합니다!"

    success = await PushAPI.send(title, message)

    if success:
        print("🎉 푸시 알림 전송 성공!")
    else:
        print("😞 푸시 알림 전송 실패!")


# 동기 테스트 함수
def test_push_notification_sync():
    """푸시 알림 테스트 (동기)"""
    print("🔔 푸시 알림 테스트 시작... (동기)")

    title = "202번 버스 알림"
    message = "202번 버스가 1분 후 도착합니다!"

    success = PushAPISync.send(title, message)

    if success:
        print("🎉 푸시 알림 전송 성공!")
    else:
        print("😞 푸시 알림 전송 실패!")


if __name__ == "__main__":
    # 비동기 테스트
    print("=== 비동기 테스트 ===")
    asyncio.run(test_push_notification())

    print("\n=== 동기 테스트 ===")
    test_push_notification_sync()
