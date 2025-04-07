import asyncio
from aiogram import Bot

# 🔹 텔레그램 봇 API 토큰 (자신의 토큰 입력
API_TOKEN = '7327136374:AAGf5-in-1rjZ2dGSmjLP9CJ2pkHDwxh1xU'
chat_id = '7632593871'

async def send_message(text):
    """텔레그램으로 메시지를 보내는 비동기 함수"""
    bot = Bot(token=API_TOKEN)
    await bot.send_message(chat_id=chat_id, text=text)

async def main():
    """사용자로부터 메시지를 입력받아 텔레그램으로 전송하는 함수"""
    while True:
        message = input("보낼 메시지를 입력하세요 (종료하려면 'exit' 입력): ")
        
        if message.lower() == 'exit':
            print("메시지 전송을 종료합니다.")
            break

        # 🔹 send_message 비동기 호출
        await send_message(message)

# 🔹 비동기 이벤트 루프 실행
if __name__ == "__main__":
    asyncio.run(main())
