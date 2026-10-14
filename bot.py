import os
import re
import json
import asyncio
import threading
import requests
from flask import Flask, request, jsonify
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# ----------------------------------------------------
# APNI REAL DETAILS YAHAN DAALEIN:
api_id = 39808787
api_hash = "78cd2d0a2edad2ead12a5b881008a697" 
session_string = "1BVtsOI4BuwEVkqC9ZDmaUavSOUtXnwtNq9rDk7HQ6Eg7jGLlTJT5DRZWh9SRMDRKKH28kal-d8A0NkX2zHV0FZ_6q1QUDj6-YRoYvAc22X1u3dy7fZcq10i_kkeTYnhyoZBPmDxg94nlhyVJgzxUALcahaiEObTOeZVs2ePI-4jekmey-anK5rRBrFfiVavXMPV984vOaynCTZTAdf86vBAxCv-zQkZ_qWoT8VydYscye8jFoQsW0gLibtEBj4x-upQVAWEZJ7X61On3Sy_V5ZS-Ed6T9dQieeiIXIiXOWvMRYrw5s5BCKhsIyQSAc6f0WpPUPtQQdYQ7AQQZzNPe2llnpOYDTU="
# ----------------------------------------------------

RENDER_API_URL = "https://movie-time-1-ygfk.onrender.com/api.php"
API_SECRET_KEY = "my_secret_key_123"
MOVIES_FILE = "movies.json"

SOURCE_CHANNELS = [
    "@HollywoodMoviesHub",
    "@DirectFileHub",
    "@WebseriesHub",
    "@BollywoodMoviesHub",
    "@LatestMovieHub",
    "@SouthIndianHub",
]

MY_TELEGRAM_CHANNEL = "https://t.me/latesmovies9"

# Flask Server Setup
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot and Movie API is active and running 24/7!"

@app.route('/api.php', methods=['POST', 'GET'])
def handle_api():
    if request.method == 'POST':
        data = request.json
        if not data or data.get("secret") != API_SECRET_KEY:
            return jsonify({"status": "error", "message": "Unauthorized"}), 403
        
        movies = []
        if os.path.exists(MOVIES_FILE):
            try:
                with open(MOVIES_FILE, 'r') as f:
                    movies = json.load(f)
            except:
                movies = []
        
        new_movie = {
            "title": data.get("title", "Movie Release"),
            "quality": data.get("quality", "HD / Hindi Dubbed"),
            "embed_link": data.get("embed_link", ""),
            "telegram_link": data.get("telegram_link", ""),
            "poster": data.get("poster", "https://via.placeholder.com/300x450?text=PRMovie")
        }
        
        movies.insert(0, new_movie)
        movies = movies[:100]
        
        with open(MOVIES_FILE, 'w') as f:
            json.dump(movies, f, indent=4)
            
        resp = jsonify({"status": "success", "message": "Saved successfully!"})
        resp.headers.add("Access-Control-Allow-Origin", "*")
        return resp
    
    elif request.method == 'GET':
        movies = []
        if os.path.exists(MOVIES_FILE):
            try:
                with open(MOVIES_FILE, 'r') as f:
                    movies = json.load(f)
            except:
                movies = []
        resp = jsonify(movies)
        resp.headers.add("Access-Control-Allow-Origin", "*")
        return resp

@app.route('/movies.json', methods=['GET'])
def get_movies_json():
    movies = []
    if os.path.exists(MOVIES_FILE):
        try:
            with open(MOVIES_FILE, 'r') as f:
                movies = json.load(f)
        except:
            movies = []
    resp = jsonify(movies)
    resp.headers.add("Access-Control-Allow-Origin", "*")
    return resp

# Telethon Client Setup
client = TelegramClient(StringSession(session_string), api_id, api_hash)

async def scan_old_movies():
  print("Purane messages ko scan kiya ja raha hai...")
  RENDER_LOCAL_URL = "http://127.0.0.1:10000/api.php"
  
  for channel in SOURCE_CHANNELS:
    try:
      async for msg in client.iter_messages(channel, limit=10):
        text = msg.text or msg.caption or ""
        if not text:
          continue

        lines = text.split("\n")
        movie_title = lines[0].strip() if lines else "PRMovie Release"

        urls = re.findall(r"(https?://[^\s]+)", text)
        direct_embed_link = urls[0] if urls else ""
        telegram_post_link = f"https://t.me/{channel.replace('@','')}/{msg.id}"

        payload = {
            "secret": API_SECRET_KEY,
            "title": movie_title,
            "quality": "HD / Hindi Dubbed",
            "embed_link": direct_embed_link,
            "telegram_link": telegram_post_link,
        }

        requests.post(RENDER_LOCAL_URL, json=payload)
    except Exception as e:
      print(f"Error scanning channel {channel}: {e}")
  print("Scanning poori ho gayi hai!")

@client.on(events.NewMessage(chats=SOURCE_CHANNELS))
async def movie_listener(event):
  msg = event.message
  text = msg.text or msg.caption or ""
  if not text:
    return

  lines = text.split("\n")
  movie_title = lines[0].strip() if lines else "PRMovie Release"

  urls = re.findall(r"(https?://[^\s]+)", text)
  direct_embed_link = urls[0] if urls else ""

  forwarded_msg = None
  try:
    forwarded_msg = await client.forward_messages(MY_TELEGRAM_CHANNEL, msg)
  except Exception as e:
    print("Forward Error:", e)

  my_channel_username_clean = MY_TELEGRAM_CHANNEL.replace("@", "")
  telegram_post_link = (
      f"https://t.me/{my_channel_username_clean}/{forwarded_msg.id}"
      if forwarded_msg
      else "https://t.me/" + my_channel_username_clean
  )

  payload = {
      "secret": API_SECRET_KEY,
      "title": movie_title,
      "quality": "HD / Hindi Dubbed",
      "embed_link": direct_embed_link,
      "telegram_link": telegram_post_link,
  }

  try:
    requests.post("http://127.0.0.1:10000/api.php", json=payload)
  except Exception as e:
    print("Network Error:", e)

def run_telegram_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    async def main():
        print("Telegram Bot Start Ho Raha Hai...")
        await scan_old_movies()
        print("Ab Live New Messages ka Intezaar kiya ja raha hai...")

    with client:
        client.loop.run_until_complete(main())
        client.run_until_disconnected()

if __name__ == "__main__":
    threading.Thread(target=run_telegram_bot, daemon=True).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
