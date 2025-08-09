from flask import Flask
import threading
import os
import sys

# Import and run the main bot in a separate thread
def run_bot():
    print("🤖 Bot thread initialized")
    from main import scrape_qasa, get_random_delay, is_active_hours, get_sleep_until_active
    import time
    
    # Run the main bot loop
    while True:
        try:
            if is_active_hours():
                print("🔍 Starting Qasa check...")
                scrape_qasa()
                delay = get_random_delay()
                print(f"⏰ Next check in {int(delay)} minutes...")
                time.sleep(delay * 60)
            else:
                sleep_minutes = get_sleep_until_active()
                start_hour = int(os.getenv('ACTIVE_START_HOUR', 7))
                print(f"😴 Outside active hours (7:00 - 23:00). Sleeping until {start_hour}:00...")
                print(f"💤 Sleeping for {int(sleep_minutes)} minutes...")
                time.sleep(sleep_minutes * 60)
        except Exception as e:
            print(f"❌ Error in bot loop: {e}")
            time.sleep(60)  # Wait 1 minute before retrying

app = Flask(__name__)

@app.route('/')
def health_check():
    return "Qasa Bot is running! 🏠"

@app.route('/health')
def health():
    return {"status": "healthy", "service": "qasa-bot"}

if __name__ == '__main__':
    print("🚀 Starting Qasa Bot...")
    
    # Start the bot in a background thread
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    print("✅ Bot thread started successfully")
    
    # Start the web server
    port = int(os.environ.get('PORT', 8080))
    print(f"🌐 Starting web server on port {port}")
    app.run(host='0.0.0.0', port=port) 