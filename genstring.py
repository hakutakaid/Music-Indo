# Credits to Akshay


from pyrogram import Client as c

API_ID = 27396410
API_HASH = "175dd5dc67ce353d41d7aefd5a104d9c"

print("\n\n Enter Phone number when asked.\n\n")

i = c("MusicIndo", api_id=API_ID, api_hash=API_HASH, in_memory=True)

with i:
    ss = i.export_session_string()
    print("\nHERE IS YOUR STRING SESSION, COPY IT, DON'T SHARE!!\n")
    print(f"\n{ss}\n")
