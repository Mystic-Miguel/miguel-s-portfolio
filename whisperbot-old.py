from pyrogram import Client, filters, idle
from pyrogram.types import InlineQueryResultPhoto, InlineKeyboardMarkup, InlineKeyboardButton, InlineQueryResultArticle, InputTextMessageContent
from pyrogram import enums
TOKEN = 'hi'
app = Client(
'ystbot', 9398500, 'ad2977d673006bed6e5007d953301e13', bot_token=TOKEN
)
######################
LOG = -1001739761638 #
######################
@app.on_inline_query(filters.regex("@"))
async def whisper(app, iquery):
    user = iquery.query.split("@")[1]
    if " " in user: return 
    user_id = iquery.from_user.id
    query = iquery.query.split("@")[0]
    if user == "all":
      text = "🎊 This wisper for all"
      username = "all"
    else:
      get = await app.get_chat(user)
      user = get.id
      username = get.first_name
      text = f"**🔒 Secret whisper for ( {username} ) .ا**"
    send = await app.send_message(LOG, query)
    reply_markup = InlineKeyboardMarkup(
      [[
        InlineKeyboardButton("📪 Show whisper", callback_data=f"{send.id}جلب{user}from{user_id}")
      ]]
    )
    await iquery.answer(
      results=[
       InlineQueryResultArticle(
          title=f"📪 Send whisper for {username}",
          url="http://t.me/Y88F8",
          input_message_content=InputTextMessageContent(
            message_text=text,
            parse_mode=enums.ParseMode.MARKDOWN 
          ),
          reply_markup=reply_markup
       )
      ],
      cache_time=1
    )

@app.on_inline_query()
async def whisper(app, query):
    text = '''
❓ How to use this bot in inline:

@YSTBOT Hi @DevZaid
@YSTBOT Hi @all
'''
    await query.answer(
        results=[
            InlineQueryResultPhoto(
                title="🔒 Type the whisper + username",
                photo_url='https://t.me/DevZaid',
                description='@YSTBOT Hello @DevZaid',
                reply_markup=InlineKeyboardMarkup ([[InlineKeyboardButton ("🔗", url='t.me/Y88F8')]]),
                input_message_content=InputTextMessageContent(text)
            ),
        ],
        cache_time=1
    )
    
@app.on_callback_query(filters.regex("جلب"))
async def get_whisper(app,query):
    sp = query.data.split("جلب")[1]
    user = sp.split("from")[0]
    from_user = int(sp.split("from")[1])
    reply_markup = InlineKeyboardMarkup(
      [
      [
        InlineKeyboardButton("📭 Show whisper", callback_data=query.data)
      ],
      [
        InlineKeyboardButton("🗑️", callback_data=f"DELETE{from_user}")
      ],
      ]
    )
    if user == "all":
       msg = await app.get_messages(LOG, int(query.data.split("جلب")[0]))
       await query.answer(msg.text, show_alert=True)
       try:
         await query.edit_message_reply_markup(
           reply_markup
         )
       except:
         pass
       try:
         alert0 = f"📭 {query.from_user.mention} opened the @all whisper ."
         await app.send_message(from_user, alert0)
       except:
         pass
       return 
    
    else:
      if str(query.from_user.id) == user:
        msg = await app.get_messages(LOG, int(query.data.split("جلب")[0]))
        await query.answer(msg.text, show_alert=True)
        try:
         await query.edit_message_reply_markup(
           reply_markup
         )
        except:
         pass
        return 

      if query.from_user.id == from_user:
        msg = await app.get_messages(LOG, int(query.data.split("جلب")[0]))
        await query.answer(msg.text, show_alert=True)
        return
      
      else:
        get = await app.get_chat(int(user))
        touser = get.first_name
        alert = f"ℹ️ Someone trying to open your whisper with {touser}:\n\n"
        alert += f"👤 Firstname : {query.from_user.mention}\n"
        alert += f"🆔 ID : {query.from_user.id}\n"
        if query.from_user.username:
          alert += f"🔍 Username : @{query.from_user.username}\n"
        alert += "\n\n📭"
        await query.answer("🔒 This whisper it's not for you .", show_alert=True)
        try:
          await app.send_message(
            from_user,
            alert
          )
        except:
          pass
        return 

@app.on_callback_query(filters.regex("DELETE"))
async def del_whisper(app,query):
   user = int(query.data.split("DELETE")[1])
   if not query.from_user.id == user:
     return await query.answer("❓ Only the sender can use this button .")
   
   else:
     reply_markup = InlineKeyboardMarkup(
      [[
        InlineKeyboardButton("Dev. 🔗", url="https://t.me/DevZaid")
      ]]
    )
     await query.edit_message_text(f"**🗑️ This whisper was deleted by ( {query.from_user.mention} ) .**",
       reply_markup=reply_markup
     )
     

app.start()
print("🎖️")
idle()