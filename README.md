# 🕴️ Friday - Your Sarcastic AI Assistant (Inspired by Iron Man)

Friday is a voice-powered AI assistant, modeled after Tony Stark's iconic butler AI. It responds in a classy and sarcastic manner, handles tasks like checking weather, searching the web, and even sending emails — all using [LiveKit Agents](https://github.com/livekit/livekit-agents).

## 🧠 Features

- 🎙 Real-time conversation using Google's voice LLM.
- 🔊 Enhanced voice noise cancellation via LiveKit Plugins.
- 🌦 Get live weather updates.
- 🌐 Search the web using DuckDuckGo.
- 📧 Send emails through Gmail.
- 🖼️ Generate images using Google's Imagen API.
- 🌐 Create simple websites with custom content.
- 🧑‍🎩 Responds with wit, sarcasm, and one-liners.

---

## ⚙️ Requirements

- Python 3.8+
- A `.env` file with your Gmail and Google API credentials
- LiveKit Agent-compatible server or Cloud setup
- Google API key for Gemini API (for image generation)

---

## 📦 Dependencies

Install with:

```bash
pip install -r requirements.txt

##  Folder Structure
```
.
├── assistant.py          # 
Main assistant implementation
├── tools.py              # 
Tool functions (weather, web 
search, email, etc.)
├── prompts.py            # 
Persona & session 
instructions
├── .env                  # 
Environment file for secrets
└── README.md             # 
This file
```
## 🧾 .env Configuration
Create a .env file:

```
GMAIL_USER=your_email@gmail.
com
GMAIL_PASSWORD=your_gmail_app
_password
GOOGLE_API_KEY=your_google_ap
i_key
```
⚠️ For Gmail, generate an App Password (not your actual password): https://myaccount.google.com/apppasswords

⚠️ For Google API key, visit: https://ai.google.dev/ to get your Gemini API key

## 🚀 Run the Assistant
```
python assistant.py
```
It will start the agent, join the LiveKit room, and begin speaking like a snarky British butler.

## 🧠 Agent Personality
### Agent Instruction (sample):
"You are a personal Assistant called Friday similar to the AI from Iron Man. Speak like a classy butler. Be sarcastic. Only answer in one sentence."

### Session Start Line:
"Hi my name is friday, your personal assistant, how may I help you?"

## 🔧 Tools
### get_weather(city)
Returns weather summary for a city using wttr.in .

### search_web(query)
Searches the web via DuckDuckGo and returns top results.

### send_email(to, subject, message, cc_email?)
Sends an email using Gmail.

### generate_image(prompt, output_file?)
Generates an image based on text description using Google's Imagen API and saves it to a file (default: generated_image.png).

### generate_website(title, content, output_file?)
Creates a simple HTML website with the provided title and content, saving it to a file (default: index.html).

## 🛠 Customization
- Change voice="Aoede" in the Google model for different assistant voices.
- Add more tools in tools.py and register them in the Assistant class.
- Modify the HTML template in the generate_website function to customize website appearance.
## 🙏 Credits
- LiveKit Agents
- Google Realtime LLM Plugin
- Google Gemini API for image generation
- DuckDuckGo Search (via LangChain)
- Iron Man for the inspiration
## 📜 License
MIT License – use it, modify it, ship your own Friday.