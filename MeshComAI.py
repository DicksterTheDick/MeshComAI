import meshtastic
import meshtastic.serial_interface
from pubsub import pub
import time
import requests
import textwrap

# === CONFIGURATION ===
# Replace with your actual API key from OpenRouter or other AI service
API_KEY = "YOUR_API_KEY_HERE"  
# Safe character limit for Meshtastic messages (228 is max, but using 200 for safety)
CHAR_LIMIT = 200  

# === FUNCTION TO TALK TO AI ===
def ask_ai(prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        # Replace with your app's reference if using OpenRouter
        "HTTP-Referer": "YOUR_APP_URL",  
        "X-Title": "YOUR_APP_NAME"  # Replace with your app name
    }

    # You can change the model to any supported by your AI provider
    # Options: "gpt-3.5-turbo", "claude-instant-v1", "deepseek/deepseek-chat-v3-0324:free", etc.
    data = {
        "model": "deepseek/deepseek-chat-v3-0324:free",
        "messages": [
            {"role": "system", "content": "Respond in 1-2 sentences max. Be clear, friendly and concise. Don't exceed 228 characters."},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        # Replace with your AI provider's API endpoint if not using OpenRouter
        r = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        r.raise_for_status()
        return r.json()['choices'][0]['message']['content']
    except Exception as e:
        return f"[AI Error] {e}"

# === SPLIT LONG MESSAGES ===
def split_message(msg, limit):
    return textwrap.wrap(msg, limit)

# === CALLBACK WHEN MESSAGE IS RECEIVED ===
def onReceive(packet):
    try:
        print(f"🔍 Debugging packet content: {packet}")

        if 'decoded' in packet and 'text' in packet['decoded']:
            message = packet['decoded']['text']
            from_id = packet['fromId']
            print(f"\n📥 Received from {from_id}: {message}")

            # Send to AI
            response = ask_ai(message)
            print(f"🤖 AI response: {response}")

            # Split response into parts if too long
            parts = split_message(response, CHAR_LIMIT)
            total_parts = len(parts)

            for i, part in enumerate(parts):
                prefix = f"[{i+1}/{total_parts}] "
                if i > 0:
                    part = f"(...continued) {part}"
                full_msg = prefix + part

                if len(full_msg) > 228:
                    # Trim to not exceed limit
                    full_msg = full_msg[:227]

                print(f"📤 Sending DM to {from_id}: {full_msg}")
                try:
                    interface.sendText(full_msg, destinationId=from_id)
                except Exception as e:
                    print(f"❌ Error sending part {i+1}: {e}")
                time.sleep(2)

        else:
            print("⚠️ Non-text message received, skipping.")

    except Exception as e:
        print(f"❌ Error handling packet: {e}")

# === MESHTASTIC INTERFACE SETUP ===
print("🔌 Connecting to Meshtastic device...")
interface = meshtastic.serial_interface.SerialInterface()

pub.subscribe(onReceive, "meshtastic.receive")
print("✅ Listening for messages...")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("👋 Exiting...")
    interface.close()
