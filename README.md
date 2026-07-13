# 🤖 Jarvis Voice Assistant

A Python-based voice assistant inspired by Iron Man's JARVIS, built with Speech Recognition, Gemini AI, and gTTS.

## ✨ Features
- 🎙️ Wake word detection ("Jarvis")
- 🌐 Open websites by voice
- 🎵 Play music from custom library
- 🌤️ Real-time weather updates
- 😂 Tell jokes
- ⏰ Current time & date
- 🤖 AI-powered responses via Gemini
- 📰 Latest news headlines
- 🔋 Battery status
- 📸 Takes screenshots (saves to desktop)

## 🛠️ Tech Stack
- Python
- SpeechRecognition + PyAudio
- Google Gemini AI
- gTTS + Pygame
- OpenWeatherMap API
- NewsAPI

## 🚀 Setup
1. Clone the repo
2. Install dependencies: `pip install -r requirements.txt`
3. Create `.env` file with your API keys
4. Run: `python main.py`

## 📝 Environment Variables
GEMINI_API_KEY=your_key,
OPENWEATHER_API_KEY=your_key,
NEWS_API_KEY=your_key

## 🗣️ Voice Commands
| Command | Action |
|---------|--------|
| "open google" | Opens Google |
| "open youtube" | Opens YouTube |
| "open github" | Opens GitHub |
| "open mail" | Opens Gmail |
| "play [song]" | Plays song from library |
| "weather in [city]" | Weather of any city |
| "latest news" | Top headlines |
| "tell me a joke" | Tells a joke |
| "what's the time" | Current time |
| "what's the date" | Today's date |
| "anything else" | Gemini AI answers |
| "battery status" | Battery percentage & charging status |
| "take a screenshot" | Takes screenshot & saves to desktop |