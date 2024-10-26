import telebot
import sqlite3
import threading
import time

bot = telebot.TeleBot('8095382958:AAF5PAfsnfaekult_LSAe30VPw-Ias_G7xI')


@bot.message_handler()
def reply(message):
    global integration, it
    it = message.text.lower() == '/start' or message.text.lower() == '/start inst' or message.text.lower() == '/start yt'
    if it:
        if message.text.lower() == '/start inst': 
            integration = 'instagram'
        if message.text.lower() == '/start yt': 
            integration = 'youtube'
        else:
            integration = '-'
        base = sqlite3.connect('Leska_Fotolife.bd')
        cur = base.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS users(id varchar(50), email varchar(50), integration varchar(50))')
        base.commit()
        cur.close()
        base.close()
        bot.send_message(message.chat.id, f'<b>Напишите, пожалуйста, адрес своей электронной почты.</b>\n\nТак вы сможете быть в курсе всех новых событий школы Leskafotolife👇', parse_mode='html')
        bot.register_next_step_handler(message, email_invalid)
        
def email_invalid(message):
    mess = message.text.strip()
    if '@' in mess and '.' in mess:
        email(message)
    else:
        bot.send_message(message.chat.id, 'Проверьте, пожалуйста, правильно ли вы указали email')
        bot.register_next_step_handler(message, email_invalid)

def email(message):
    global send_m
    tips_foto = open('G:/bot/Leska_Fotolife/files/tips_foto.jpg', 'rb')
    mail = message.text.strip()
    base = sqlite3.connect('Leska_Fotolife.bd')
    cur = base.cursor()
    user_exists = cur.execute("SELECT * FROM users WHERE id = ?", (message.chat.id,)).fetchone()
    if not user_exists:
        cur.execute("INSERT INTO users(id, email, integration) VALUES (?, ?, ?)", (message.chat.id, mail, integration))
    base.commit()
    cur.close()
    base.close()
    bot.send_photo(message.chat.id, tips_foto)
    bot.send_message(message.chat.id, '<b>Отлично!</b> Ловите ваш подарок:\n🎁 <a href="https://drive.google.com/file/d/1IYitU3PYNrYxdxRxLY5e7TkPUR4GdyPA/view?usp=drivesdk">Памятка "9 советов для съёмки качественного видео"</a>\n(👆нажмите, чтобы скачать)', parse_mode='html', disable_web_page_preview=True)
    tips_foto.close()
    send_m = False
    threading.Thread(target=wait_p, args=(message,), daemon=True).start()
    bot.register_next_step_handler(message, wait_m)

def wait_m(message):
    global send_m
    if it:
        reply(message)
    else:
        send_m = True
        polez = open('G:/bot/Leska_Fotolife/files/polez_0.jpg', 'rb')
        bot.send_photo(message.chat.id, polez)
        bot.send_message(message.chat.id, f'<b>Уже успели изучить памятку?</b>\n\nЛюбая новая информация, которую мы получаем, начинает работать только если её сразу применять на практике! Иначе всё быстро забывается…\n\nРезультат мы получаем лишь тогда, когда начинаем сразу внедрять новое.\n\n<b><em>Если готовы ещё учиться новому, посмотрите полезные каналы:</em></b>\n\n✔️ <a href="https://t.me/+urZO7nIWINw4NmNi">Винокурня контента</a> - советы по ведению соцсетей, музыка для видео, закадровая жизнь фотографа\n✔️<a href="https://t.me/+m5EQ9zoqQ3RlZjQy">ФотоМуза</a> - идеи для фото, вдохновение, позирование\n✔️<a href="https://t.me/+6G0hbUVYY7M2Mjdi">Сами с руками</a> - копилка мастер-классов по декору для дома и рукоделию', parse_mode='html', disable_web_page_preview=True)
        polez.close()
def wait_p(message):
    global send_m
    if not send_m:
        time.sleep(86400)
        polez = open('G:/bot/Leska_Fotolife/files/polez_0.jpg', 'rb')
        bot.send_photo(message.chat.id, polez)
        bot.send_message(message.chat.id, f'<b>Уже успели изучить памятку?</b>\n\nЛюбая новая информация, которую мы получаем, начинает работать только если её сразу применять на практике! Иначе всё быстро забывается…\n\nРезультат мы получаем лишь тогда, когда начинаем сразу внедрять новое.\n\n<b><em>Если готовы ещё учиться новому, посмотрите полезные каналы:</em></b>\n\n✔️ <a href="https://t.me/+urZO7nIWINw4NmNi">Винокурня контента</a> - советы по ведению соцсетей, музыка для видео, закадровая жизнь фотографа\n✔️<a href="https://t.me/+m5EQ9zoqQ3RlZjQy">ФотоМуза</a> - идеи для фото, вдохновение, позирование\n✔️<a href="https://t.me/+6G0hbUVYY7M2Mjdi">Сами с руками</a> - копилка мастер-классов по декору для дома и рукоделию', parse_mode='html', disable_web_page_preview=True)
        polez.close()
        send_m = True
bot.polling(none_stop=True, timeout=90)