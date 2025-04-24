<<<<<<< HEAD
# MeshComAI 🤖📡

MeshComAI is a decentralized LoRa-to-AI bridge that lets you send messages from a phone to an AI (like ChatGPT or DeepSeek) using two Heltec V3 devices running Meshtastic and a Python script.

No internet on the phone required — just mesh magic ⚡

---

## 🔗 How It Works

[Phone] ⇄ [Heltec #1] ⇄ [Heltec #2] ⇄ [Raspberry Pi] ⇄ [AI API]

1. You send a message from your phone via Meshtastic  
2. It travels over LoRa to a second Heltec connected to a Raspberry Pi  
3. The Pi script relays the message to an AI using OpenRouter/OpenAI  
4. The response is split into multiple 228-char LoRa packets if needed  
5. Messages return to your phone via the same LoRa path

---

## 🚀 Features

✅ Send messages to AI without a direct internet connection  
✅ Works over long-range LoRa (Heltec + Meshtastic)  
✅ Auto-splits AI responses over multiple messages  
✅ Respects Meshtastic 228-char limit with pagination  
✅ Brayon-style friendly tone 🧢

---

## ⚙️ Requirements

- 2x Heltec WiFi LoRa 32 V3 (flashed with Meshtastic)
- Raspberry Pi (or any Linux box)
- Python 3.9+
- OpenRouter/OpenAI API Key

---

## 📦 Installation

```bash
git clone https://github.com/votre-user-name/MeshComAI.git
cd MeshComAI
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 🧠 Usage

```bash
python3 MeshComAI.py
```

You'll be prompted to paste your OpenRouter/OpenAI API key.

---

## 💬 Example

> 📥 From phone: What's the Big Bang?  
> 🤖 AI responds:
[1/3] The Big Bang theory says the universe started with a rapid expansion...
[2/3] (...suite) Matter formed, temperatures dropped, and galaxies appeared...
[3/3] (...suite) And here we are today. 🌌

---

## 🛣 Roadmap

- [x] DM responses with pagination
- [x] Safe character-split for Meshtastic
- [ ] Save chat logs to file
- [ ] Let user switch AI model on the fly
- [ ] Add optional speech/voice output (for fun)
- [ ] Possibly run headless on a Pi Zero?

---

## 📄 License

MIT

---

> Made in the woods of New Brunswick 🪵⚡ by a Brayon and a bot.
