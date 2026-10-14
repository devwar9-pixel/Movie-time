from telethon import TelegramClient
from telethon.sessions import StringSession

# Yahan apni real API ID aur API Hash dalein
api_id = 39808787
api_hash = '78cd2d0a2edad2ead12a5b881008a697' 

# Client start karenge jo session string banayega
with TelegramClient(StringSession(), api_id, api_hash) as client:
    print("\n==============================")
    print("AAPKA SESSION CODE NEECHE HAI:")
    print("==============================\n")
    print(client.session.save())
    print("\n==============================\n")
