# ============================================================
# Group Manager Bot (FINAL DEBUG VERSION)
# ============================================================

import os
import logging
import threading
import traceback
from http.server import BaseHTTPRequestHandler, HTTPServer

logging.basicConfig(level=logging.INFO)

print("🚀 Starting bot...")

# ============================================================
# 🔍 ENV DEBUG
# ============================================================

try:
    print("🔍 Checking ENV variables...")
    print("API_ID:", os.getenv("API_ID"))
    print("API_HASH:", os.getenv("API_HASH"))
    print("BOT_TOKEN:", os.getenv("BOT_TOKEN"))
    print("MONGO_URI:", os.getenv("MONGO_URI"))
except Exception as e:
    print("❌ ENV ERROR:", e)
    traceback.print_exc()

# ============================================================
# 🔐 SECURITY CHECK
# ============================================================

try:
    from security import verify_integrity, get_runtime_key

    verify_integrity()
    RUNTIME_KEY = get_runtime_key()

    if not RUNTIME_KEY:
        raise Exception("🚫 Security validation failed!")

    print("✅ Security passed")

except Exception as e:
    print("❌ SECURITY ERROR:", e)
    traceback.print_exc()
    raise

# ============================================================
# 🌐 WEB SERVER (FOR RENDER)
# ============================================================

PORT = int(os.environ.get("PORT", 10000))

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Nomade Bot is running")

    # 🔥 FIX: Prevent 501 error spam
    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()

def start_web_server():
    try:
        server = HTTPServer(("0.0.0.0", PORT), HealthHandler)
        logging.info(f"🌐 Web server running on port {PORT}")
        server.serve_forever()
    except Exception as e:
        print("❌ WEB SERVER ERROR:", e)
        traceback.print_exc()

threading.Thread(target=start_web_server, daemon=True).start()

# ============================================================
# 🤖 BOT START (MAIN FIX AREA)
# ============================================================

try:
    from pyrogram import Client, idle
    from config import API_ID, API_HASH, BOT_TOKEN
    from handlers import register_all_handlers

    print("🔧 Initializing bot client...")

    app = Client(
        "group_manager_bot",
        api_id=API_ID,
        api_hash=API_HASH,
        bot_token=BOT_TOKEN
    )

    register_all_handlers(app)

    print("🚀 Starting bot now...")

    app.start()

    print("✅ BOT STARTED SUCCESSFULLY 🔥")

    # 👇 This keeps bot alive properly
    idle()

    print("🛑 Bot stopped")

except Exception as e:
    print("💥 BOT CRASHED:", e)
    traceback.print_exc()
