import os
import re
import requests
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# ----------------------------------------------------
# APNI DETAILS YAHAN DAALEIN:
api_id = 39808787
api_hash = "78cd2d0a2edad2ead12a5b881008a697"  
session_string = "1BVtsOI4BuwEVkqC9ZDmaUavSOUtXnwtNq9rDk7HQ6Eg7jGLlTJT5DRZWh9SRMDRKKH28kal-d8A0NkX2zHV0FZ_6q1QUDj6-YRoYvAc22X1u3dy7fZcq10i_kkeTYnhyoZBPmDxg94nlhyVJgzxUALcahaiEObTOeZVs2ePI-4jekmey-anK5rRBrFfiVavXMPV984vOaynCTZTAdf86vBAxCv-zQkZ_qWoT8VydYscye8jFoQsW0gLibtEBj4x-upQVAWEZJ7X61On3Sy_V5ZS-Ed6T9dQieeiIXIiXOWvMRYrw5s5BCKhsIyQSAc6f0WpPUPtQQdYQ7AQQZzNPe2llnpOYDTU="
# ----------------------------------------------------

RENDER_API_URL = "https://movie-time-2yfd.onrender.com"
API_SECRET_KEY = "my_secret_key_123"

SOURCE_CHANNELS = [
    "@HollywoodMoviesHub",
    "@DirectFileHub",
    "@WebseriesHub",
    "@BollywoodMoviesHub",
    "@LatestMovieHub",
    "@SouthIndianHub",
]

MY_TELEGRAM_CHANNEL = "https://t.me/latesmovies9"

# Render ke liye StringSession ka use kiya gaya hai taaki terminal input ki zaroorat na pade
client = TelegramClient(StringSession(session_string), api_id, api_hash)


async def scan_old_movies():
  print(
      "Purane messages ko scan kiya ja raha hai, kripya intezaar karein..."
  )
  for channel in SOURCE_CHANNELS:
    try:
      async for msg in client.iter_messages(channel, limit=50):
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

        requests.post(RENDER_API_URL, json=payload)
    except Exception as e:
      print(f"Error scanning channel {channel}: {e}")
  print("Purane messages ki scanning poori ho gayi hai!")


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
    requests.post(RENDER_API_URL, json=payload)
  except Exception as e:
    print("Network Error:", e)


async def main():
  print("Bot Start Ho Raha Hai...")
  await scan_old_movies()
  print("Ab Live New Messages ka Intezaar kiya ja raha hai...")


with client:
  client.loop.run_until_complete(main())
  client.run_until_disconnected()
