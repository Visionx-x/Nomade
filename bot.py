# ============================================================
#Group Manager Bot
# Author: LearningBotsOfficial (https://github.com/LearningBotsOfficial) 
# Support: https://t.me/LearningBotsCommunity
# Channel: https://t.me/learning_bots
# YouTube: https://youtube.com/@learning_bots
# License: Open-source (keep credits, no resale)
# ============================================================

import os
import logging
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN
from handlers import register_all_handlers

# 🔐 Import security (IMPORTANT)
from security import verify_integrity, get_runtime_key

logging.basicConfig(level=logging.INFO)

verify_integrity()
RUNTIME_KEY = get_runtime_key()

if not RUNTIME_KEY:
    raise Exception("🚫 Security validation failed!")

PORT = int(os.environ.get("PORT", 10000))

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Nomade Help Bot is running")

def start_web_server():
    server = HTTPServer(("0.0.0.0", PORT), HealthHandler)
    logging.info(f"🌐 Web server running on port {PORT}")
    server.serve_forever()

threading.Thread(target=start_web_server, daemon=True).start()

app = Client(
    "group_manager_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

register_all_handlers(app)

print("✅ Bot is starting securely on Render...")

app.run()
