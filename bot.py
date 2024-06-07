from threads import Threads
import re, telebot
from telebot.types import InlineKeyboardButton as b, InlineKeyboardMarkup as mk 
from kvsqlite.sync import Client 
db = Client("stupid.gay")
if not db.exists('banlist'):
    db.set('banlist', [])
if not db.exists('status'):
    db.set('status', {'e':'❌', 's':False})
if not db.exists('force'):
    db.set('force', [])
logs = ['creator', 'member', 'administrator']
def force(user_id, channel):
  b = bot.get_chat_member(chat_id='@'+str(channel), user_id=user_id)
  if str(b.status) in logs:
    return True
  else:
    return False
admins = [1485149817, 1558668590] #admins 
# استخراج الكود من الرابط
def getCode(url):
	regex_pattern = r"/(\w+)/\?"
	match = re.search(regex_pattern, url)
	if match:
	   try:
	       abs_value = match.group(1)
	   except:
	       return None
	   return (abs_value)
	else:
		return None
# جلب معلومات الفيد
def getVideo(id):
	try:
	    threads = Threads()
	except Exception as e:
		print(e)
		return None
	x = (threads.get_post(id))
	if not x["data"]:
		return None
	else:
		vid = None
		for y in x["data"]["data"]["containing_thread"]["thread_items"]:
			p = y["post"]["video_versions"]
			cap = y["post"]["caption"]["text"]
			user = y["post"]["user"]
			return dict(vid=p[0], text=cap, user=user)
#خوارزمية التحويل 
def convert_instagram_shortcode(shortcode):
    try:
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"
        media_id = 0
        for char in shortcode:
            media_id = media_id * 64 + alphabet.index(char)
        return str(media_id)
    except Exception as e:
        print(e)
        return None
bot = telebot.TeleBot("###TOKEN###", num_threads=29, skip_pending=True )
@bot.message_handler(commands=["start"])
def startm(message):
	
    if not db.get(f"user_{message.from_user.id}"):
        d = {"id": message.from_user.id, "users":[]}
        db.set(f"user_{message.from_user.id}", d)
        pass
    user_id = message.from_user.id
    if user_id in admins:
        keyss = mk(row_width=2)
        d = db.get('status')
        t = 'معطل ❌' if not d['s'] else 'مفعل ✅'
        btn, btn1, btn2, btn3, btn4, btn5, btn6 = b('الاحصائيات', callback_data='stats'), b('اذاعة', callback_data='brod'), b('حظر شخص', callback_data='ban'), b('فك حظر ', callback_data='unban'), b('تعيين قنوات اشتراك', callback_data='sub'), b('قائمة المحظورين ..', callback_data='listofban'), b(f'اشعار لدخول: {t}', callback_data='dis')
        keyss.add(btn); keyss.add(btn1, btn2); keyss.add(btn3, btn4); keyss.add(btn5); keyss.add(btn6)
        bot.reply_to(message,text='اهلا بك عزيزي الادمن ..', reply_markup=keyss)
    if user_id in db.get('banlist'): return
    chs = db.get('force')
    if chs != None:
        for i in chs:
            try:
           
                s = force(user_id=user_id, channel=i)
            except:
                s = True
                
            if not s:
                bot.reply_to(message, f'عذرا يجب عليك الاشتراك بقناة البوت:\n- @{i} .\n⎯ ⎯ ⎯ ⎯\nاشترك وأرسل [/start] ..')
                return
    bot.reply_to(message, f"اهلا بك، قم بأرسال رابط فيديو ثريد لأقوم بتحميله ..\nHello, Send me a Threads link so im going to download it..")
@bot.message_handler(content_types=["text"])
def getlink(message):
	url = message.text
	user_id = message.from_user.id
	if user_id in db.get('banlist'): return
	chs = db.get('force')
	if chs != None:
	   for i in chs:
            try:
           
                s = force(user_id=user_id, channel=i)
            except:
                s = True
                
            if not s:
                bot.reply_to(message, f'عذرا يجب عليك الاشتراك بقناة البوت:\n- @{i} .\n⎯ ⎯ ⎯ ⎯\nاشترك وأرسل [/start] ..')
                return
	code = getCode(url)
	bot.reply_to(message, "جاري التحميل.. انتظر")
	print(code)
	if code:
		id = convert_instagram_shortcode(code)
		print(id)
		if id:
			video = getVideo(id)
			print(video)
			id, username = video["user"]["pk"], video["user"]["username"]
			if video:
				x = bot.send_video(message.chat.id, video=video["vid"]["url"], caption=video['text'])
				bot.reply_to(x, f"معلومات صاحب المقطع:\nيوزر: @{username} .\nايدي: {id}.")
				return
			else:
				bot.reply_to(message, "حدثت مشكله، حاول مجددا ..")
				return
		else:
			bot.reply_to(message, "الرابط غير صحيح..")
			return
	else:
		bot.reply_to(message, "الرابط غير صحيح..")
@bot.callback_query_handler(func=lambda m:True)
def query(call):
    data, cid, mid = call.data, call.from_user.id, call.message.id
    if cid in db.get('banlist'): return
    
    if data == 'dis':
        d = db.get('status')
        if d['s'] == False:
            db.set('status', {'e':'✅', 's':True})
        else:
            db.set('status', {'e':'❌', 's':False})
        d = db.get('status')
        z = 'معطل ❌' if not d['s'] else 'مفعل ✅'
        bot.edit_message_text(f'حالة الاشعارات: {z}', chat_id=cid, message_id=mid)
        return
    if data == 'listofban':
        d = db.get('banlist')
        
        if not d or len(d) <1:
            bot.edit_message_text(text='مافي محظورين ياحب .', chat_id=cid, message_id=mid)
            return
        k = ''
        for i, x in enumerate(d, 1):
            k+=f'{i}. {x}'
        bot.edit_message_text(text=f'المحظورين:\n{k}\nعددهم: {len(d)} .', chat_id=cid, message_id=mid)
    if data == 'ban':
        x = bot.edit_message_text(text='ارسل ايدي العضو الورع الي تريد تحظره ..', chat_id=cid, message_id=mid)
        bot.register_next_step_handler(x, banone)
    if data == 'unban':
        x = bot.edit_message_text(text='ارسل ايدي العضو الورع الي تريد تفك حظره ..', chat_id=cid, message_id=mid)
        bot.register_next_step_handler(x, unbanone)
    if data == 'sub':
        ss = "\n".join(db.get('force'))
        x = bot.edit_message_text(text=f'ارسل قنوات الاشتراك الاجباري بهاي لطريقة:\n@first @second @third ..\n\nالقنوات الحالية:\n{ss}', chat_id=cid, message_id=mid)
        bot.register_next_step_handler(x, set_s)
    if data == 'brod':
        x = bot.edit_message_text(text='ارسل الرسالة لتريد ترسلها للاعضاء.. ', message_id=mid, chat_id=cid)
        bot.register_next_step_handler(x, brod_pro)
    if data == 'stats':
        c = 0
        h = 0
        users = db.keys('user_%')
        bot.answer_callback_query(call.id, 'يتم العد الان ..', cache_time=10, show_alert=True)
        for user in users:
            try:
                d = db.get(user[0])["id"]
                c+=1
                
            except:
                continue
        bot.edit_message_text(text=f"عدد الاعضاء: {c}", chat_id=cid, message_id=mid)
        return
def banone(message):
    user_id = message.text
    try:
        id = int(user_id)
    except: return
    d = db.get('banlist')
    if d != None and id in d:
        bot.reply_to(message, 'العضو محظور من قبل !!')
        return
    else:
        d.append(id)
        db.set('banlist', d)
        bot.reply_to(message, 'تم اضافته للمحظورين ..')
        try:
            bot.send_message(chat_id=id, text='تم حظرك حب .')
        except: pass
def unbanone(message):
    user_id = message.text
    try:
        id = int(user_id)
    except: return
    d = db.get('banlist')
    if d != None and id not in d:
        bot.reply_to(message, 'العضو مو محظور من قبل !!')
        return
    else:
        d.remove(id)
        db.set('banlist', d)
        bot.reply_to(message, 'تم مسحه من المحظورين ..')
        try:
            bot.send_message(chat_id=id, text='تم فك حظرك حب .')
        except: pass
def brod_pro(message):
    users = db.keys('user_%')
    mid = message.message_id
    dones = 0
    for user in users:
        try:
            user = db.get(user[0])
            id = user['id']
            bot.copy_message(id, message.chat.id, mid)
            dones+=1
        except: continue
    bot.reply_to(message, f'تم بنجاح الارسال لـ{dones}')
    return
def set_s(message):
    channels = message.text.replace('@', '').replace('https://t.me', '').split(' ')
    db.set('force', channels)
    t = '\n'.join(channels)
    bot.reply_to(message, f'تم تعيين القنوات:\n{t} ')
    return

bot.infinity_polling()