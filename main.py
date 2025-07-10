# telegram-downloader-botimport telebot
import yt_dlp
import os

BOT_TOKEN = '7911948105:AAGrkoYCrPGkMeLwwuC7jMkXqF8ZQGH9-h4'
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Привет! Отправь мне ссылку на видео с YouTube, TikTok или Instagram, и я его скачаю 📥")

@bot.message_handler(func=lambda message: True)
def download_video(message):
    url = message.text.strip()

    if not url.startswith("http"):
        bot.send_message(message.chat.id, "❌ Пожалуйста, отправь корректную ссылку.")
        return

    msg = bot.send_message(message.chat.id, "🔄 Скачиваю видео, подожди немного...")

    try:
        ydl_opts = {
            'outtmpl': 'video.%(ext)s',
            'format': 'mp4',
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            video_path = ydl.prepare_filename(info)

        with open(video_path, 'rb') as video:
            bot.send_video(message.chat.id, video)

        os.remove(video_path)

    except Exception as e:
        bot.send_message(message.chat.id, f"⚠️ Ошибка при загрузке: {e}")

bot.polling(non_stop=True)
