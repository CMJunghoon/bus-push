#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔔 OneSignal 푸시 알림 테스트 스크립트
버스 API 없이 푸시 알림만 테스트
"""

import os
import asyncio
from dotenv import load_dotenv
from push_notification import PushAPI

# .env 파일 로드
load_dotenv()


async def test_push():
    """푸시 알림 테스트"""
    print("🔔 OneSignal 푸시 알림 테스트 시작!")
    print("=" * 50)

    # 환경변수 확인
    app_id = os.getenv("ONESIGNAL_APP_ID")
    rest_key = os.getenv("ONESIGNAL_REST_KEY")

    print(f"📱 OneSignal APP_ID: {app_id[:10] if app_id else 'None'}...")
    print(f"🔑 OneSignal REST_KEY: {rest_key[:10] if rest_key else 'None'}...")

    if not app_id or not rest_key:
        print("❌ OneSignal 환경변수가 설정되지 않았습니다!")
        print("💡 .env 파일에서 ONESIGNAL_APP_ID와 ONESIGNAL_REST_KEY를 확인해주세요.")
        return

    # 테스트 메시지
    title = "🧪 푸시 테스트"
    message = (
        "이것은 테스트 푸시 알림입니다!\n\n시간: "
        + asyncio.get_event_loop().time().__str__()[:10]
    )

    print(f"\n📤 푸시 발송 시도...")
    print(f"제목: {title}")
    print(f"내용: {message}")

    try:
        # 푸시 발송
        success = await PushAPI.send(title, message)

        if success:
            print("\n🎉 푸시 알림 전송 성공!")
            print("📱 휴대폰에서 알림을 확인해보세요.")
        else:
            print("\n❌ 푸시 알림 전송 실패!")
            print("🔍 OneSignal 설정을 다시 확인해주세요.")

    except Exception as e:
        print(f"\n💥 푸시 발송 중 오류 발생: {e}")
        print("🔍 네트워크 연결과 OneSignal 설정을 확인해주세요.")


def main():
    """메인 함수"""
    print("🔔 OneSignal 푸시 알림 테스트")
    print("=" * 40)

    try:
        asyncio.run(test_push())
    except KeyboardInterrupt:
        print("\n🛑 테스트 중단")
    except Exception as e:
        print(f"\n❌ 테스트 실행 오류: {e}")


if __name__ == "__main__":
    main()
