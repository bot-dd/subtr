import os, threading
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from flask import Flask
from dotenv import load_dotenv
from translator import translate_subtitle
from config import user_lang, set_user_lang, get_user_lang

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

app = Client("sub_translator", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
web = Flask(__name__)

@web.route('/')
def index():
    return "<center><h2>Sub Translator Bot</h2><p>Created by <a href='https://t.me/RahatMx'>Rahat</a><br>Powered by <a href='https://t.me/RM_Movie_Flix'>RM Movie Flix</a></p></center>"

@app.on_message(filters.command("start"))
async def start(client, message: Message):
    await message.reply(
        "**স্বাগতম সাবটাইটেল অনুবাদক বটে!**\n\n- শুধু `.srt`, `.vtt`, `.ass` ফাইল পাঠান\n- অটো অনুবাদ হয়ে যাবে বাংলায়\n\nভাষা চেঞ্জ করতে `/setlang` দিন",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("চ্যানেল", url="https://t.me/RM_Movie_Flix"),
             InlineKeyboardButton("সাপোর্ট", url="https://t.me/RM_Mirror_Leech")],
            [InlineKeyboardButton("ডেভেলপার", url="https://t.me/RahatMx")]
        ])
    )

@app.on_message(filters.command("setlang"))
async def change_lang(client, message: Message):
    await message.reply(
        "অনুগ্রহ করে ভাষার কোড দিন (যেমন: `en`, `hi`, `bn`, `ar`)\n\nসব ভাষা দেখতে এখানে যান: https://cloud.google.com/translate/docs/languages",
        quote=True
    )

@app.on_message(filters.text & filters.reply)
async def save_lang(client, message: Message):
    lang_code = message.text.strip()
    if len(lang_code) == 2 or len(lang_code) == 5:
        set_user_lang(message.from_user.id, lang_code)
        await message.reply(f"✅ আপনার ভাষা `{lang_code}` হিসেবে সংরক্ষিত হয়েছে।")
    else:
        await message.reply("❌ ভুল ভাষা কোড। দয়া করে সঠিক কোড দিন।")

@app.on_message(filters.document)
async def handle_file(client, message: Message):
    file = message.document
    if not file.file_name.endswith((".srt", ".vtt", ".ass")):
        return await message.reply("⚠️ দয়া করে একটি বৈধ সাবটাইটেল ফাইল দিন (.srt, .vtt, .ass)")
    
    lang = get_user_lang(message.from_user.id)
    sent = await message.reply("⏳ ফাইল ডাউনলোড ও অনুবাদ হচ্ছে...")
    path = await client.download_media(message.document)
    
    new_file = await translate_subtitle(path, lang)
    await message.reply_document(new_file, caption=f"✅ অনুবাদ সম্পন্ন হয়েছে → `{lang}` ভাষায়!")
    
    os.remove(path)
    os.remove(new_file)
    await sent.delete()

def run():
    app.run()

def run_web():
    web.run(host="0.0.0.0", port=8080)

if __name__ == "__main__":
    threading.Thread(target=run).start()
    threading.Thread(target=run_web).start()
