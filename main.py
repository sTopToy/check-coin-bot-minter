import time
import telebot
from telebot import types
import re
from mintersdk.minterapi import MinterAPI
from telebot.types import InlineKeyboardButton
import json
import requests

token = 'ваш токен'
bot = telebot.TeleBot(token)

digits_pattern = re.compile(r'^[0-9]+ [0-9]+$', re.MULTILINE)

minter = MinterAPI(api_url="http://api-02.minter.store:8841")

canal = "@json_coin"

coin_check = "JSONCOIN"

@bot.message_handler(commands=['start'])
def find_file_ids(message):
	keyboard = types.InlineKeyboardMarkup(row_width=5)
	keyboard.add(InlineKeyboardButton(text="Обновить", callback_data="reset"))
	coin = minter.get_coin_info(coin_check)
	cost = int(json.loads(requests.get("http://api-02.minter.store:8841" + "/estimate_coin_buy?coin_to_sell=BIP&value_to_buy=100000000&coin_to_buy=" + str(coin_check)).text)["result"]["will_pay"]) / 100000000
	send = "Монета: " + coin["result"]["symbol"] + "\nЦена: " + str(cost) + "\nCRR: " + str(coin["result"]["crr"]) + "\nTime: " + str(int(time.time())) + "\n@json_coin"
	bot.send_message(canal, str(send),reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
	try:
		if call.message:
			coin = minter.get_coin_info(coin_check)
			keyboard = types.InlineKeyboardMarkup(row_width=5)
			keyboard.add(InlineKeyboardButton(text="Обновить", callback_data="reset"))
			cost = int(json.loads(requests.get("http://api-02.minter.store:8841" + "/estimate_coin_buy?coin_to_sell=BIP&value_to_buy=100000000&coin_to_buy=" + str(coin_check)).text)["result"]["will_pay"]) / 100000000
			send = "Монета: " + coin["result"]["symbol"] + "\nЦена: " + str(cost) + "\nCRR: " + str(coin["result"]["crr"]) + "\nTime: " + str(int(time.time())) + "\n@json_coin"
			bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=str(send),reply_markup=keyboard)
	except:
		pass
if __name__ == '__main__':
	bot.polling(none_stop=True)