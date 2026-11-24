
import os
import asyncio
import requests
from concurrent.futures import ThreadPoolExecutor
from TikTokLive import TikTokLiveClient
from TikTokLive.events import ConnectEvent

WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK")
USERS = [
    user.strip().lstrip("@")
    for user in os.getenv("TIKTOK_USERS", "").split(",")
    if user.strip()
]

if not WEBHOOK_URL:
    raise ValueError("DISCORD_WEBHOOK belum diatur!")

if not USERS:
    raise ValueError("Daftar TIKTOK_USERS masih kosong!")

def send_notification(username):
    message = (
        f"🔴 **TIKTOK LIVE ALERT — SERAPHIC**\n"
        f"@{username} sekarang sedang LIVE!\n"
        f"https://www.tiktok.com/@{username}/live"
    )
    requests.post(
        WEBHOOK_URL,
        json={"content": message},
        timeout=15
    ).raise_for_status()

def monitor(username):
    client = TikTokLiveClient(unique_id=username)

    @client.on(ConnectEvent)
    async def on_connect(event):
        print(f"@{username} sedang LIVE!")
        try:
            send_notification(username)
        except Exception as error:
            print("Gagal mengirim Discord:", error)

    print(f"Memantau @{username}...")
    client.run()

def main():
    with ThreadPoolExecutor(max_workers=len(USERS)) as executor:
        list(executor.map(monitor, USERS))

if __name__ == "__main__":
    main()
  
