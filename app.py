import os
import telebot
from telebot.types import WebAppInfo
from telebot.types import InlineKeyboardMarkup
from telebot.types import InlineKeyboardButton
API_TOKEN = "TOKEN HERE"
bot = telebot.TeleBot(API_TOKEN, parse_mode="HTML")

# طيب هنا تكدر تحط اكثر من موقع ولموقع حسب لتحب اني حطيت كوكل
# زين اريد احط موقع لاخ شسوي؟؟؟
web_apps = [
	{"label" : "Google", "link" : "https://google.com"},
	{"label" : "youtube", "link" : "https://youtube.com"},
]
# زين هسه حطينه موقع جديد

# هسه هنا رساله لستارت لخاصه بالبوت 
# رتبها حسب لتحبه ..
@bot.message_handler(commands=["start"])
def start(message):
	# هنا الازرار وشغلهن كلش مهم حاول تفهمم
	prev_button = InlineKeyboardButton("⬅️", callback_data="web-app:0")
	next_button = InlineKeyboardButton("➡️", callback_data="web-app:2")
	web_app_btn = InlineKeyboardButton(web_apps[0]["label"],
		web_app=WebAppInfo(web_apps[0]["link"]))

	bot.send_message(message.chat.id, "hi",
		reply_markup=InlineKeyboardMarkup().row(
			prev_button, web_app_btn, next_button))
# هنا اي ضفطه زر حيشوفها وحيتحقق منها
# يعني لامحاله وحينفذ الامر ..
@bot.callback_query_handler(func=lambda call: True)
def callback_listener(call):
    
	_id, data = call.id, call.data
	# هنا شرطت عليه انو اذا ضغط ع الزر الي داتا مالته هيجي ف ينفذ .
	if data[:7] == "web-app":
		index = int(data[8:])
		# وهنا بحال خلصوا الازرار او انتهت اللست حيكيلك Nothing Here
		# تكدر تغيرها حسب ماتحب :(
		if index == 0:
			bot.answer_callback_query(_id, "Nothing here", show_alert=True)
		elif index > len(web_apps):
			bot.answer_callback_query(_id, "None", show_alert=True)
		else:
			prev_button = InlineKeyboardButton("⬅️", callback_data=f"web-app:{index-1}")
			next_button = InlineKeyboardButton("➡️", callback_data=f"web-app:{index+1}")
			# هنا الزر الي حيفتح الويب اب ولازم تركز بي ومهم اكثر منك ....
			web_app_btn = InlineKeyboardButton(web_apps[index-1]["label"],
				web_app=WebAppInfo(web_apps[index-1]["link"]))		
			# هنا بحال سويت التالي او فتت للصفحه الاخ ح يعدل رساله ويرجع ينطيك الازرار..
			bot.edit_message_reply_markup(call.message.chat.id, call.message.id,
				reply_markup=InlineKeyboardMarkup().row(
					prev_button, web_app_btn, next_button))
				
	elif data[:7] == "confirm":
		#هنا من تكمل ف يبستسلمك :()
		bot.send_message(int(data[8:]), ":)")
		bot.edit_message_reply_markup(inline_message_id=call.inline_message_id)

bot.infinity_polling(skip_pending=True)
