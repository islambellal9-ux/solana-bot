import requests
import time
import telegram

# بياناتك
HELIUS_API_KEY = "8805dbfe-a481-439c-9ee8-24a8a7cc372a"
WALLET_ADDRESS = "H8KTT1e3F4u9Mw4cn4byAS4Uv1LZJv7QRDr46UPKAMe7"
BOT_TOKEN = "8417421895:AAFMr6SyURp4CZfRSxCGMPdGJBMJhJ12QQU"
CHAT_ID = "6629971568"

bot = telegram.Bot(token=BOT_TOKEN)
bot.send_message(chat_id=CHAT_ID, text="✅ Bot started successfully!")  # رسالة تأكيد عند التشغيل

seen_signatures = set()

while True:
    try:
        url = f"https://api.helius.xyz/v0/addresses/{WALLET_ADDRESS}/transactions?api-key={HELIUS_API_KEY}&limit=1"
        r = requests.get(url)
        data = r.json()

        if isinstance(data, list) and data:
            tx = data[0]
            sig = tx.get("signature")

            if sig and sig not in seen_signatures:
                seen_signatures.add(sig)

                # نلتقط نوع العملية إذا موجود
                tx_type = tx.get("type", "Unknown")
                
                msg = f"💰 New transaction detected!\nType: {tx_type}\nSignature: {sig}\nExplorer: https://solscan.io/tx/{sig}"
                bot.send_message(chat_id=CHAT_ID, text=msg)

    except Exception as e:
        print(f"Error: {e}")

    time.sleep(10)  # يتحقق كل 10 ثواني
