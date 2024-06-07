import requests, time
from telebot import TeleBot as tb
from kvsqlite.sync import Client
from telebot.types import InlineKeyboardButton as btn, InlineKeyboardMarkup as mk 
bot = tb("###BotToken###", num_threads=30, skip_pending=True, parse_mode="html")
db = Client(f"x.x")
token = "" ## Wallet Token
def gettrans():

    headers = {
    'authority': 'walletbot.me',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.9',
    'authorization': token,
    # 'cookie': '__cflb=0H28vP5G7utRAgardSRCBp9BoNgTHSyAeu34SoSZaV3',
    'referer': 'https://walletbot.me/main',
    'sec-ch-ua': '"Not)A;Brand";v="24", "Chromium";v="116"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36',
}

    params = {
    'limit': '100',
}

    response = requests.get('https://walletbot.me/api/v1/transactions/', params=params, headers=headers)
    
    if response.status_code == 200:
        return response.json()
def check(address):
    get_x = gettrans()
    
    done = None
    if get_x:
        trans_ac = get_x["transactions"]
        for t in trans_ac:
            print(t)
            if t["type"] != "deposit":
                continue
            if t["gateway"] != "top_up":
                continue
            if t["currency"] != "TON":
                continue
            status, address, amount, create = t["status"], t["input_addresses"], t["amount"], t["created_at"]
            if db.exists(f"true_{create}_{address}"):
                return dict(ok=False)
            if status == "success":
                if str(address) == str(address):
                    done = True
                    db.set(f"true_{create}_{address}", True)
                    return dict(ok=True, amount=amount)
                else:
                    return dict(ok=False)
            else:
                return dict(ok=False)
        if done:
            return dict(ok=True)
        else:
            return dict(ok=False)
    else:
        return dict(ok=False)
main_address = "" #Addresss

@bot.message_handler(commands=["start"])
def start(message):
    if not db.exists(f"user_{message.from_user.id}"):
        db.set(f"user_{message.from_user.id}", dict(donate=0, id=message.from_user.id))
    d = db.get(f"user_{message.from_user.id}")
    donate = d["donate"]
    keys = mk().add(btn("⦗ تبرع ⦘", callback_data="donate"))
    bot.reply_to(message, f"<strong>😊 اهلا بيك عزيزي،</strong>\n — — — — — —\nمن خلال هذا البوت تكدر تتبرع بعمله الـ<strong>TON</strong>، للتبرع اضغط الزر التحت ..\n — — — — — \n<strong>👤 تم صنع البوت بواسطة: @trakoss .</strong>", reply_markup=keys)
    return
@bot.callback_query_handler(func=lambda m:True)
def calls(call):
    db.cleanex()
    cid, mid, data = call.from_user.id, call.message.id, call.data
    if data == "donate":
        x = bot.edit_message_text(text="↯ قم بأرسال العنوان الذي سوف تقوم الارسال منه..", chat_id=cid, message_id=mid)
        bot.register_next_step_handler(x, getad)
    if data == "check":
        if not db.exists(f"user_{call.from_user.id}_ttl"):
            bot.edit_message_text(text="↯<strong>انتهت الجلسة الخاصة بالتحويل ..</strong>", chat_id=cid, message_id=mid)
            return
        d = db.get(f"user_{cid}_ttl")
        x = check(d)
        if x:
            if x["ok"]:
                am = x["amount"]
                return bot.edit_message_text(text=f"<strong>↯ تمت عملية التبرع بنجاح، شكرا لتبرع بـ ( $ {am} ) ربما قد يكون مبلغ قليل لك، لكنه كثير.\n — — — — — —</strong>", chat_id=cid, message_id=mid)
                return
            else:
                bot.edit_message_text(text=f"↯ لم تتم عملية التحويل، حاول مرة اخرى ..", chat_id=cid, message_id=mid, reply_markup=mk().add(btn("⦗ تحقق ⦘", callback_data="check")))
                return
        else:
            bot.edit_message_text(text=f"↯ لم تتم عملية التحويل، حاول مرة اخرى ..", chat_id=cid, message_id=mid, reply_markup=mk().add(btn("⦗ تحقق ⦘", callback_data="check"))) 
            return
def getad(message):
    address = message.text
    if len(address) < 10:
        bot.reply_to(message, "↯ الادرس وهمي او خطأ")
        return
    x = f"""
↯ العنوان الخاص بك ↫ <code>{address}</code>

↯ قم بأرسال المبلغ على هذة العنوان: <code>{main_address}</code>

↯ قم الان بعملية التحويل، بعدها اضغط على الازر في الاسفل، ملاحظة سوف تنتهي الجلسة بغضون ١٠ دقائق ..
    """
    db.setex(f"user_{message.from_user.id}_ttl", ttl=600, value=address)
    x = bot.reply_to(message, x)
    time.sleep(3)
    keys = mk().add(btn("⦗ تحقق ⦘", callback_data="check"))
    bot.edit_message_reply_markup(message_id=x.message_id, chat_id=message.from_user.id, reply_markup=keys)
    return
bot.infinity_polling()