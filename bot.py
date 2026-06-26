import telebot
import random

TOKEN = "8972821740:AAGYalqf9wsKpx4w5V8zBvWtj-kjHzQa1CA"
ADMIN_CHAT_ID = 7045368457

bot = telebot.TeleBot(TOKEN)

bot.delete_webhook()

waiting_for_message = {}
mew_mode = {}
music_pool = {}   # ذخیره موزیک‌های هر چت


# حالت /harf
@bot.message_handler(commands=['harf'])
def harf_command(message):
    waiting_for_message[message.chat.id] = True
    mew_mode.pop(message.chat.id, None)
    bot.reply_to(message, "حرفت رو میو برات میوفرستم.🩵")


# حالت /mewmew
@bot.message_handler(commands=['mewmew'])
def mewmew_command(message):
    mew_mode[message.chat.id] = True
    waiting_for_message.pop(message.chat.id, None)
    bot.reply_to(message, "میوی بی پایان فعال شد.😽")


# وقتی ربات به گروه اضافه شد
@bot.message_handler(content_types=['new_chat_members'])
def welcome_new_member(message):
    for member in message.new_chat_members:
        if member.id == bot.get_me().id:
            bot.reply_to(message, """سلام خوش اومدم.😽
من حاصل درس نخوندن و حوصله سررفتن ممسینم
اگر برید داخلم و /harf رو ارسال کنید میتونید به ممسین پیام بدید.🩵
حتما /mewmew هم تست کنید.
""")


# ذخیره موزیک‌ها
@bot.message_handler(content_types=['audio'])
def save_music(message):
    chat_id = message.chat.id

    if chat_id not in music_pool:
        music_pool[chat_id] = []

    music_pool[chat_id].append(message.audio.file_id)


# گرفتن همه پیام‌ها
@bot.message_handler(func=lambda message: True)
def handle_messages(message):

    mews = ["میو؟", "میو میو", "میوووووو"]
    adab = ["میووو🫪", "کونی مودب باش", "فداتشم اگر دوستم داری کمتر فحش بده🩵",
            "عشقم فحش نده🩵", "اینجا به ادب دهند پاداش🩵",
            "سگ ولگرد فحش نده", "عزیزم سعی کن درست صحبت کنی🩵"]

    baleh = ["بفرمایید", "جانم", "بله"]
    nazan = ["نزن بابا خوب نیست"]

    text = (message.text or "").strip().lower()

    # حالت /harf
    if message.chat.id in waiting_for_message:
        bot.forward_message(
            ADMIN_CHAT_ID,
            message.chat.id,
            message.message_id
        )
        bot.reply_to(message, "میو🧘🏽")
        del waiting_for_message[message.chat.id]
        return

    # اگر موزیک خواست
    if any(word in text for word in ["موزیک", "آهنگ", "اهنگ"]):
        if message.chat.id in music_pool and len(music_pool[message.chat.id]) > 0:
            random_music = random.choice(music_pool[message.chat.id])
            bot.send_audio(
                message.chat.id,
                random_music,
                caption=None
            )
        else:
            bot.reply_to(message, "هنوز موزیکی تو این چت ندارم 😿")
        return

    # فحش و حیوانات خاص
    if any(word in text for word in ["کیر", "کس", "کص", "شیر", "زرافه", "موش",
                                     "ملخ", "کلاغ", "کون", "کوس", "دول",
                                     "ممه", "احمق", "گایی", "میگام",
                                     "تخم", "دیوث"]):
        bot.reply_to(message, random.choice(adab))
        return

    # اسم و گربه
    if any(word in text for word in ["ممسین", "گربه", "پیشی"]):
        bot.reply_to(message, random.choice(baleh))
        return

    # میو و سگ
    if any(word in text for word in ["میو", "سگ", "هاپ", "واق"]):
        bot.reply_to(message, random.choice(mews))
        return

    # مواد
    if any(word in text for word in ["لین", "سیگار", "گل", "شیشه", "قهوه", "شیره", "تریاک"]):
        bot.reply_to(message, random.choice(nazan))
        return

    # حالت /mewmew فقط در پیوی
    if message.chat.type == "private" and message.chat.id in mew_mode:
        bot.reply_to(message, random.choice(mews))
        return


print("ربات روشن شد...")
bot.infinity_polling()