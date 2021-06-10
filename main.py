import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.callback_query import CallbackQuery
from time import sleep
import random
import datetime
import asyncio
import time
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.types import ReplyKeyboardRemove

from config import api,admin
from key import *
from db_user import *
from db_game import *
from db_participant import *
from pay import *
from db_pay import *


logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=api)
storage = MemoryStorage()
dp = Dispatcher(bot,storage=storage)
running_game = []
users = []

class start(StatesGroup):
	nick = State()
	phone = State()

class Mailing(StatesGroup):
	sms = State()

class pay_m(StatesGroup):
	summ = State()
	phone = State()



#@dp.message_handler(commands=['add'])
#async def start_add(message: types.Message):
	# add_game(2,'0', '90', 0, 9000)
	# print(one_game(2)[3])
	# await asyncio.sleep(int(one_game(2)[3])-10)
	# print('Пройшов таймер 1')
	# try: 
	# 	l = one_game(2)[2].split(',')
	# except:
	# 	pass
	# for i in list(l):
	# 	try:
	# 		await bot.send_message(int(i), 'Игра скоро начнется!')		
	# 	except:
	# 		continue
	# await asyncio.sleep(10)
	# print('Пройшов таймер 1')

	# #Добавляем в participant.db
	# l = one_game(2)[2].split(',')
	# game_data = one_game(2)
	# u = []
	# for i in range(len(l)):
	# 	if i in u:
	# 		continue
	# 	add_part(game_data[1],int(l[i]),int(l[i+1]))
	# 	add_part(game_data[1],int(l[i+1]),int(l[i]))
	# 	u.append(i+1)

	# #Рассылка
	# for i in list(l):
	# 	try:
	# 		await bot.send_message(int(i), 'Игра началась! Ходи!'+'\n'+f'Твой опонент: {participant(int(i))[3]}'+'\n'+f'Раунд: {participant(int(i))[7]}'+'\n'+'Счет: 0:0', reply_markup=choice())
	# 	except:
	# 		continue

	# #Цикл гри
	# while len(one_game(2)[2].split(',')) != 1 and ',' in one_game(2)[2]:
	# 	print('Цикл 1')
	# 	while one_game(2)[5] != len(one_game(2)[2].split(',')):
	# 		print('Цикл 2')
	# 		await asyncio.sleep(0.5)
	# 		upd_mark_game(2, 0)
	# 	u = []
	# 	if ',' not in one_game(2)[2]:
	# 		break
	# 	l = one_game(2)[2].split(',')
	# 	game_data = one_game(2)
	# 	for i in range(len(l)):
	# 		if i in u:
	# 			continue
	# 		delete(int(l[i]))
	# 		delete(int(l[i+1]))
	# 		try:
	# 			add_part(game_data[1],int(l[i]),int(l[i+1]))
	# 			add_part(game_data[1],int(l[i+1]),int(l[i]))
	# 		except:
	# 			await bot.send_message(int(l[i]), 'У тебя нету пары, поэтому ты проходишь во второй тур ;)')
	# 		u.append(i+1)
	# 	for i in l:
	# 		await bot.send_message(int(i), f'РАУНД {participant(int(i))[9]}')
	# 		await bot.send_message(int(i), f'Твой опонент: {participant(int(i))[3]}', reply_markup=choice())

	# winner = one_game(2)[2]
	# await bot.send_message(int(winner), 'Ты победил!')
	# upd_wallet(message.chat.id, take_user(int(winner))[3]+one_game(participant(int(winner))[1])[4])
	# try:
	# 	delete(int(winner))
	# except:
	# 	pass

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
	users.append(message.chat.id)
	g= all_game()
	f = open(f'data.tgs', 'rb')
	await bot.send_sticker(message.chat.id, f)
	print(g)
	#await message.answer(f'{message.chat.first_name}, привет!\n\nМеня зовут Арчибальд, и я организатор турнира Камень Бумага Ножницы.\n\nКаждый Четверг в 20:00 мы определяем счастливчика, который заберет главный приз!\n\nБлижайший турнир: {g[0][3]} Приз: {g[0][6]}', reply_markup=reg())
	try:
		await message.answer(f'<b>{message.chat.first_name}</b>, привет!\n\nТы попал на телеграм-турнир <b>КАМЕНЬ-БУМАГА-НОЖНИЦЫ</b>, где  каждый четверг мы определениям победителя, который забирает главный приз!\n\nБлижайший турнир:\n{g[0][3]}\n\nПриз: {g[0][6]} грн\nСтоимость участия: {g[0][4]} грн', reply_markup=reg(g[0][0]), parse_mode='html')
	except:
		await message.answer(f'<b>{message.chat.first_name}</b>, привет!\n\nТы попал на телеграм-турнир <b>КАМЕНЬ-БУМАГА-НОЖНИЦЫ</b>, где  каждый четверг мы определениям победителя, который забирает главный приз!\n\nАктуального турнира нету, мы сообщим ;)', parse_mode='html')
	if not take_user(message.chat.id):
		if message.chat.username:
			add_user(message.chat.id, '@'+str(message.chat.username))
		else:
			add_user(message.chat.id, str(message.chat.first_name))
	#await bot.send_message(message.chat.id, f'Игра: {str(i[1])}' + '\n' + f'Игроки: {i[2]}' + '\n' + f'Старт: {i[3]}' + '\n' + f'Ставка: {str(i[4])}', reply_markup=join(str(i[0])))

async def countt(ch1,ch2,now):
	now = now.split(',')
	if ch1 == ch2:
		return str(int(now[0])+1)+','+str(int(now[1])+1)
	elif ch1 == 'k' and ch2 == 'n':
		return str(int(now[0])+1)+','+now[1]
	elif ch1 == 'k' and ch2 == 'b':
		return now[0]+','+str(int(now[1])+1)
	elif ch1 == ch2:
		return now
	elif ch1 == 'n' and ch2 == 'b':
		return str(int(now[0])+1)+','+now[1]
	elif ch1 == 'n' and ch2 == 'k':
		return now[0]+','+str(int(now[1])+1)
	elif ch1 == 'b' and ch2 == 'k':
		return str(int(now[0])+1)+','+now[1]
	elif ch1 == 'b' and ch2 == 'n':
		return now[0]+','+str(int(now[1])+1)

async def win(ch1,ch2):
	if ch1 == ch2:
		return 0
	elif ch1 == 'k' and ch2 == 'n':
		return 1
	elif ch1 == 'k' and ch2 == 'b':
		return 2
	elif ch1 == ch2:
		return now
	elif ch1 == 'n' and ch2 == 'b':
		return 1
	elif ch1 == 'n' and ch2 == 'k':
		return 2
	elif ch1 == 'b' and ch2 == 'k':
		return 1
	elif ch1 == 'b' and ch2 == 'n':
		return 2


@dp.message_handler()
async def mmm(message: types.Message):
	global count, win

	print(message.text)
	if not take_user(message.chat.id):
		await message.answer('Нажми сначало /start', reply_markup=list_game(message.chat.id))
		return 0	
	try:
		if 'Камень' in message.text or 'Ножницы' in message.text or 'Бумага' in message.text:
			try:
				await bot.delete_message(message.chat.id, message.message_id)
			except:
				pass
	except:
		pass

	if 'Профиль' in message.text:
		data = take_user(message.chat.id)
		await bot.send_message(message.chat.id, f'Твой ID: {data[1]}'+'\n'+f'Сыграно игр: {data[2]}'+'\n'+f'Баланс: {data[3]} грн'+'\n'+f'Активная игра: {data[5]}', reply_markup=back)

	elif 'Пополнить' in message.text:
		await pay_m.summ.set()
		await bot.send_message(message.chat.id, 'Напиши сумму пополнения', reply_markup=back)		

	elif 'Назад' in message.text:
		try:
			await bot.delete_message(message.chat.id, message.message_id)
			await bot.delete_message(message.chat.id, message.message_id-1)
		except:
			pass
		await bot.send_message(message.chat.id, 'Выбери из меню нужный пункты', reply_markup=list_game(message.chat.id))

	#elif '2' == message.text:
		#aaa = await bot.send_message(message.chat.id, 'Выбери из меню нужный пункты', reply_markup=list_game(message.chat.id))
		#await bot.delete_message(message.chat.id, aaa.message_id)

	elif 'Камень' in message.text or 'Ножницы' in message.text or 'Бумага' in message.text:
		try:
			await bot.delete_message(message.chat.id, message.message_id)
			try:					
				await bot.delete_message(message.chat.id, message.message_id-1)
			except:
				pass
			try:
				await bot.delete_message(message.chat.id, message.message_id-2)
			except:
				pass
			try:
				await bot.delete_message(message.chat.id, message.message_id-3)
			except:
				pass
		except:
			pass

		try:
			await bot.delete_message(message.chat.id, participant(message.chat.id)[10])
		except Exception as ex:
			print(str(ex))
			
		

		if not participant(message.chat.id):
			await message.answer('Сначало зарегистрируйтесь!', reply_markup=list_game(message.chat.id))
			return 0		

		elif participant(message.chat.id)[8] == 1:
			await message.answer('Ты уже походил, ждем ход оппонент!')
			return 0		

		elif 'Камень' in message.text:
			ch = 'k'
		elif 'Ножницы' in message.text:
			ch = 'n'
		elif 'Бумага' in message.text:
			ch = 'b'

		if participant(message.chat.id)[8] == 2:
			await asyncio.sleep(1)
			if ch == 'k':
				f = open(f'{ch}-n-v.tgs', 'rb')
				await bot.send_sticker(message.chat.id, f)
				upd_round(message.chat.id, int(participant(message.chat.id)[7])+1)
				count = participant(message.chat.id)[4].split(',')
				upd_score_user(message.chat.id, str(int(count[0])+1)+',0')
				f = open(f'{participant(message.chat.id)[4]}.tgs', 'rb')
				await bot.send_sticker(message.chat.id, f)
				await bot.send_message(message.chat.id, f'Ходи, у тебя 15 сек', reply_markup=choice())
			elif ch == 'n':
				f = open(f'{ch}-b-v.tgs', 'rb')
				await bot.send_sticker(message.chat.id, f)
				upd_round(message.chat.id, int(participant(message.chat.id)[7])+1)
				count = participant(message.chat.id)[4].split(',')
				upd_score_user(message.chat.id, str(int(count[0])+1)+',0')
				f = open(f'{participant(message.chat.id)[4]}.tgs', 'rb')
				await bot.send_sticker(message.chat.id, f)
				await bot.send_message(message.chat.id, f'Ходи, у тебя 15 сек', reply_markup=choice())
			elif ch == 'b':
				f = open(f'{ch}-k-v.tgs', 'rb')
				await bot.send_sticker(message.chat.id, f)
				upd_round(message.chat.id, int(participant(message.chat.id)[7])+1)
				count = participant(message.chat.id)[4].split(',')
				upd_score_user(message.chat.id, str(int(count[0])+1)+',0')
				f = open(f'{participant(message.chat.id)[4]}.tgs', 'rb')
				await bot.send_sticker(message.chat.id, f)
				await bot.send_message(message.chat.id, f'Ходи, у тебя 15 сек', reply_markup=choice())
			count = participant(message.chat.id)[4].split(',')
			
			if count[0] == '3':
				f = open('ты выиграл.tgs', 'rb')
				await bot.send_sticker(message.chat.id, f)
				await bot.send_message(message.chat.id, 'Ждем остальных ;)', reply_markup=ReplyKeyboardRemove(True))
				current_game = participant(message.chat.id)[1]
				upd_mark_game(current_game, one_game(current_game)[5]+1)
				upd_code(message.chat.id, 1)
			return 0


		upd_choice(message.chat.id, ch)
		upd_round(message.chat.id, int(participant(message.chat.id)[7])+1)
		upd_code(message.chat.id, 1)   
		c = 0
		print(f'{participant(message.chat.id)} -- {participant(participant(message.chat.id)[3])}')
		##############################################################################################################################################################################
		# ПОФІКСИТИ ЦИКЛ while @ ПОФІКСИТИ ЦИКЛ while @ ПОФІКСИТИ ЦИКЛ while @ ПОФІКСИТИ ЦИКЛ while @ ПОФІКСИТИ ЦИКЛ while @ ПОФІКСИТИ ЦИКЛ while @ ПОФІКСИТИ ЦИКЛ while @ ПОФІКСИТИ ЦИКЛ while @ 
		try:
			while participant(message.chat.id)[7] != participant(participant(message.chat.id)[3])[7]:
				c+=1
				await asyncio.sleep(1)
				if participant(message.chat.id)[7] == 1:
					if c == 60:
						current_game = participant(message.chat.id)[1]
						now = one_game(current_game)[2].split(',')
						now.remove(str(message.chat.id))
						print(f'This is now: {now}')
						if len(now) == 1:
							upd_user_game_ind_if(current_game, now[0])
						else:
							upd_user_game_ind_if(current_game, ','.join(now))
						upd_current_game(participant(message.chat.id)[3],0)
						upd_code(message.chat.id, 1)
						delete(participant(message.chat.id)[3])
						f = open('ты выиграл.tgs', 'rb')
						await bot.send_sticker(message.chat.id, f)
						await bot.send_message(message.chat.id, 'Ждем остальных ;)', reply_markup=ReplyKeyboardRemove(True))
						f = open('ты проиграл.tgs', 'rb')
						await bot.send_sticker(participant(message.chat.id)[3], f)
						await bot.send_message(participant(message.chat.id)[3], f'Ты не успел, поэтому ты проиграл. К сожалению, в этот раз тебе не удалось добраться до заветной победы, но следующая возможность взять реванш уже совсем скоро!', reply_markup=ReplyKeyboardRemove(True))
				else:						
					if c == 15:
						current_game = participant(message.chat.id)[1]
						now = one_game(current_game)[2].split(',')
						now.remove(str(message.chat.id))
						print(f'This is now: {now}')
						if len(now) == 1:
							upd_user_game_ind_if(current_game, now[0])
						else:
							upd_user_game_ind_if(current_game, ','.join(now))
						upd_current_game(participant(message.chat.id)[3],0)
						upd_code(message.chat.id, 1)
						delete(participant(message.chat.id)[3])
						f = open('ты выиграл.tgs', 'rb')
						await bot.send_sticker(message.chat.id, f)
						await bot.send_message(message.chat.id, 'Ждем остальных ;)', reply_markup=ReplyKeyboardRemove(True))
						f = open('ты проиграл.tgs', 'rb')
						await bot.send_sticker(participant(message.chat.id)[3], f)
						await bot.send_message(participant(message.chat.id)[3], f'Ты не успел, поэтому ты проиграл. К сожалению, в этот раз тебе не удалось добраться до заветной победы, но следующая возможность взять реванш уже совсем скоро!', reply_markup=ReplyKeyboardRemove(True))
		except Exception as Ex:
			print(Ex)
			pass

		upd_code(message.chat.id, 0)
		#Обновляємо все
		u_ch = participant(message.chat.id)[6]
		o_ch = participant(participant(message.chat.id)[3])[6]
		if participant(message.chat.id)[0] >participant(participant(message.chat.id)[3])[0]:
			kkk = participant(message.chat.id)[4]
			#kkk = kkk.split(".")
			c = await countt(u_ch, o_ch, kkk)
			upd_score_user(message.chat.id, c)  #print(f'Кількість ел: {len(c)}, looks like: {c}, another one: {"".join(list(reversed(c)))}')
			upd_score_user(participant(message.chat.id)[3], ''.join(list(reversed(c))))
			print(f'SCORE OF OPONENT: {participant(participant(message.chat.id)[3])[4]}')
			if await win(u_ch,o_ch)==1:
				f = open(f'{u_ch}-{o_ch}-v.tgs', 'rb')
				await bot.send_sticker(message.chat.id, f)
				s = open(f'{u_ch}-{o_ch}-p.tgs', 'rb')
				await bot.send_sticker(participant(message.chat.id)[3], s)
			elif await win(u_ch,o_ch)==2:
				f = open(f'{u_ch}-{o_ch}-p.tgs', 'rb')
				await bot.send_sticker(message.chat.id, f)
				s = open(f'{u_ch}-{o_ch}-v.tgs', 'rb')
				await bot.send_sticker(participant(message.chat.id)[3], s)
			elif await win(u_ch,o_ch)==0:
				f = open(f'{u_ch}-{o_ch}-d.tgs', 'rb')
				await bot.send_sticker(message.chat.id, f)
				s = open(f'{u_ch}-{o_ch}-d.tgs', 'rb')
				await bot.send_sticker(participant(message.chat.id)[3], s)

			f = open(f'{participant(message.chat.id)[4]}.tgs', 'rb')
			await bot.send_sticker(message.chat.id, f)
			if participant(message.chat.id)[7] != 4 or participant(participant(message.chat.id)[3])[7] != 4:
				m_id_u = await bot.send_message(message.chat.id, 'Ходи, у тебя 15 сек', reply_markup=choice())
				upd_last_sms(message.chat.id, m_id_u.message_id)

			f = open(f'{participant(participant(message.chat.id)[3])[4]}.tgs', 'rb')
			await bot.send_sticker(participant(message.chat.id)[3], f)
			if participant(message.chat.id)[7] != 4 or participant(participant(message.chat.id)[3])[7] != 4:
				m_id_o = await bot.send_message(participant(message.chat.id)[3], 'Ходи, у тебя 15 сек', reply_markup=choice())		
				upd_last_sms(participant(message.chat.id)[3], m_id_o.message_id)

		#Якщо більше 3-ох рундів
		if participant(message.chat.id)[7] >= 4 or participant(participant(message.chat.id)[3])[7] >= 4:
			res = participant(message.chat.id)[4].split(',')
			if participant(message.chat.id)[0] >participant(participant(message.chat.id)[3])[0]:
				try:
					await bot.delete_message(message.chat.id, participant(message.chat.id)[10])
					await bot.delete_message(participant(message.chat.id)[3], participant(participant(message.chat.id)[3])[10])
				except Exception as ex:
					print(str(ex))
				if int(res[0]) > int(res[1]):
					f = open('ты выиграл.tgs', 'rb')
					await bot.send_sticker(message.chat.id, f)
					await bot.send_message(message.chat.id, 'Ждем остальных ;)', reply_markup=ReplyKeyboardRemove(True))
					fl = open('ты проиграл.tgs', 'rb')
					await bot.send_sticker(participant(message.chat.id)[3], fl)
					await bot.send_message(participant(message.chat.id)[3], 'К сожалению, в этот раз тебе не удалось добраться до заветной победы, но следующая возможность взять реванш уже совсем скоро!', reply_markup=ReplyKeyboardRemove(True))
					#Видаляєм пацика
					current_game = participant(message.chat.id)[1]
					now = one_game(current_game)[2].split(',')
					now.remove(str(participant(message.chat.id)[3]))
					if len(now) == 1:
						upd_user_game_ind_if(current_game, now[0])
					else:
						upd_user_game_ind_if(current_game, ','.join(now))
					upd_current_game(participant(message.chat.id)[3],0)
					delete(participant(message.chat.id)[3])
					#Вітаємо пацика і робимо mark +1
					upd_mark_game(current_game, one_game(current_game)[5]+1)
					upd_code(message.chat.id, 1)

				elif int(res[0]) < int(res[1]):
					f = open('ты проиграл.tgs', 'rb')
					await bot.send_sticker(message.chat.id, f)
					await bot.send_message(message.chat.id, 'К сожалению, в этот раз тебе не удалось добраться до заветной победы, но следующая возможность взять реванш уже совсем скоро!)', reply_markup=ReplyKeyboardRemove(True))
					fl = open('ты выиграл.tgs', 'rb')
					await bot.send_sticker(participant(message.chat.id)[3], fl)
					await bot.send_message(participant(message.chat.id)[3], 'Ждем остальных ;)', reply_markup=ReplyKeyboardRemove(True))
					#Видаляєм пацика
					current_game = participant(message.chat.id)[1]
					now = one_game(current_game)[2].split(',')
					now.remove(str(message.chat.id))
					print(f'This is now: {now}')
					if len(now) == 1:
						upd_user_game_ind_if(current_game, now[0])
					else:
						upd_user_game_ind_if(current_game, ','.join(now))
					upd_current_game(message.chat.id,0)
					upd_code(participant(message.chat.id)[3], 1)
					delete(message.chat.id)
					#Вітаємо пацика і робимо mark +1
					upd_mark_game(current_game, one_game(current_game)[5]+1)


				elif int(res[0]) == int(res[1]):
					current_game = participant(message.chat.id)[1]
					now = one_game(current_game)[2].split(',')
					if len(now) == 2:				
						fl = open('ничья.tgs', 'rb')
						await bot.send_sticker(message.chat.id, fl)
						await bot.send_message(message.chat.id, 'Еще один бой!', reply_markup=choice())
						fl = open('ничья.tgs', 'rb')
						await bot.send_sticker(participant(message.chat.id)[3], fl)
						await bot.send_message(participant(message.chat.id)[3], 'Еще один бой!', reply_markup=choice())
						upd_score_user(message.chat.id, '0,0')
						upd_score_user(participant(message.chat.id)[3], '0,0')
						#upd_round(message.chat.id, 1)
						#upd_round(participant(message.chat.id)[3], 0)

					else:
						fl = open('ничья.tgs', 'rb')
						await bot.send_sticker(message.chat.id, fl)			
						await bot.send_message(message.chat.id, 'В следующий раунд вы проходите вдвоем.', reply_markup=ReplyKeyboardRemove(True))
						fl = open('ничья.tgs', 'rb')
						await bot.send_sticker(participant(message.chat.id)[3], fl)	
						await bot.send_message(participant(message.chat.id)[3], 'В следующий раунд вы проходите вдвоем.', reply_markup=ReplyKeyboardRemove(True))
						upd_mark_game(current_game, one_game(current_game)[5]+2)


	elif 'Создать' in message.text and message.chat.id in admin:
		await bot.send_message(message.chat.id, 'Напиши когда старт для игры, размер ставки, главный приз. Пример:' +'\n'+'Дата(формат мм.дд)/Время(20:0)/Стоимость для юзера/Сумма главного приза ', reply_markup=back)

	elif 'Расылка' in message.text and message.chat.id in admin:	
		await Mailing.sms.set()
		await bot.send_message(message.chat.id, 'Напиши смс, которое нужно отправлять', reply_markup=back_k)
	
	elif 'Удалить все игры' == message.text:
		print(all_game())
		for i in range(4):
			c = True
			try:
				l = one_game_id(i)[2].split(',')
			except:
				l = ''
				c = False
			for i in l:
				if c:
					upd_current_game(int(i),0)
		delete_all_game()
		await message.answer('Удалено', reply_markup=list_game(message.chat.id))

	# ЗМІНИТИ ПОТІМ, БО ЦЕ ДЛЯ ТЕСТУ (elif ..  на else)
	else:
		if message.chat.id in admin:
			#if '\n' not in message.text and ' ' not in message.text:
				#await bot.send_message(message.chat.id, 'Неверно написал! Пример:' +'\n'+'Дата(формат мм.дд)/Время(20:0)/Стоимость для юзера/Сумма главного приза ', reply_markup=list_game(message.chat.id))
				#return 0
			if '/' in message.text:
				listt = message.text.split('/')
			else:
				listt = message.text.split('\n')
			try:
				#print(int(listt[0]))
				print(int(listt[2]))
				print(int(listt[3]))
			except:
				await bot.send_message(message.chat.id, 'Неверно написал! Пример:' +'\n'+'Дата(формат мм.дд)/Время(20:0)/Стоимость для юзера/Сумма главного приза ', reply_markup=list_game(message.chat.id))
				return 0

			bots = ['@babechills','@volkiz_gorky','@nikita_yatsuba','@Markfromdnepr','@Zikoko','@bizzobonjo','@Aleksey_Belokurov','@ksenia_sobolieva','@hello','@mykola']
			idd = random.randint(100,1000000)
			textt = listt[0].split('.')
			textt = f'{str(textt[1])}.{str(textt[0])} | {listt[1]}'
			
			#textt = "".join(list(reversed(listt[0])))
			print(f'DATA {textt}')
			add_game(idd,'0', textt, listt[2], listt[3])
			i = one_game(idd)
			await bot.send_message(message.chat.id, 'Твоя игра создана, зови друзей!', reply_markup=list_game(message.chat.id))
			#await bot.send_message(message.chat.id, f'ID игры: {str(i[1])}' + '\n' + f'Количество игроков: 0' + '\n' + f'Старт: {i[3]}' + '\n' + f'Ставка: {str(i[4])} грн', reply_markup=reg(str(i[0])))

			all_u = take_user_all()
			for u in all_u:
				try:
					await bot.send_message(u[1], f'Ближайший Турнир:\n{i[3]}\n\nГлавный приз: {str(i[6])} грн\nСтоимость участия: {str(i[4])} грн', reply_markup=reg(i[0]))
				except Exception as E:
					continue
				#await bot.send_message(message.chat.id, f'ID игры: {str(i[1])}' + '\n' + f'Количество игроков: 0' + '\n' + f'Старт: через {i[3]} минут' + '\n' + f'Ставка: {str(i[4])} грн', reply_markup=reg())

			timee = listt[1].split(':')
			now  = datetime.datetime.now()
			dat = listt[0].split('.')
			month = dat[0]
			day = dat[1]
			if str(timee[1][0]) == '0':
				will = datetime.datetime(2021,int(month), int(day), int(timee[0]), int(timee[1][1]),0)
			else:
				will = datetime.datetime(2021,int(month), int(day), int(timee[0]),int(timee[1]),0)
			print(datetime.datetime.now())
			print(will)
			duration = will - now
			duration_in_s = duration.total_seconds()
			print(duration_in_s)

			###print(f'Start timer of {int(one_game(idd)[3])*60-int(one_game(idd)[3])*60/5}')

			#await asyncio.sleep(duration_in_s-55*60)

			last_55_min = duration_in_s-60*60
			print(f'Таймер до 55 хвилин: {duration_in_s}')
			print('')
			print('')
			await asyncio.sleep(duration_in_s)
			print('Пройшов таймер 1day')
			try: 
				l = one_game(idd)[2].split(',')
			except:
				l = '1'
			for i in list(l):
				try:
					await bot.send_message(int(i), 'До начала турнира осталось 60 минут')		
				except:
					continue

			#await asyncio.sleep(int(one_game(idd)[3])*60/5)
			await asyncio.sleep(10) #55*60
			#print(f'Пройшов таймер {int(one_game(idd)[3])*60/5}')


			#print(f'Start timer of {int(one_game(idd)[3])*60-int(one_game(idd)[3])*60/5}')
			#await asyncio.sleep(5*60)
			await asyncio.sleep(5)
			print('Пройшов таймер 1')
			try: 
				l = one_game(idd)[2].split(',')
			except:
				l = '1'
			for i in list(l):
				try:
					await bot.send_message(int(i), 'Осталось 5 минут')		
				except:
					continue

			#Добавляем в participant.db
			l = one_game(idd)[2].split(',')
			game_data = one_game(idd)
			u = []
			if one_game(idd)[2] == '0':
				delete_game(idd)
				return 0

			
			elif ',' not in one_game(idd)[2]:
				await bot.send_message(int(one_game(idd)[2]), 'К сожелению, недостаточно игроков', reply_markup=list_game(433))
				upd_current_game(int(one_game(idd)[2]), 0)
				delete_game(idd)
				return 0
			#print('СМС КОЖНОМУ ГРАВЦЮ, ХТО ЧИЙ ОПОНЕНТ start')
			for i in range(len(l)):

				if i in u:
					continue
				try:
					delete(int(l[i]))
					delete(int(l[i+1]))
				except:
					pass
				try:
					add_part(game_data[1],int(l[i]),int(l[i+1]))
					add_part(game_data[1],int(l[i+1]),int(l[i]))
				except:
					#await bot.send_message(int(l[i]), 'У тебя нету пары, поэтому ты проходишь во второй тур ;)')
					add_part(game_data[1],int(l[i]),0)
					#upd_mark_game(idd, one_game(idd)[5]+1)
					upd_code(int(l[i]),2)
					upd_current_game(int(l[i]),1)

				u.append(i+1)

			#Рассылка
			for i in list(l):
				#print('СМС КОЖНОМУ ГРАВЦЮ, ХТО ЧИЙ ОПОНЕНТ')
				try:    					
					#await bot.send_message(int(i), f'РАУНД {participant(int(i))[9]}')
					#await bot.send_message(int(i), f'РАУНД 1')
					f = open('раунд1.tgs', 'rb')
					await bot.send_sticker(int(i), f)
					try:
						await bot.send_message(int(i), f'Твой оппонент: {take_user(participant(int(i))[3])[6]}', reply_markup=choice())
					except:
						await bot.send_message(int(i), f'Твой оппонент: {random.choice(bots)}', reply_markup=choice())
					upd_played_game(int(i),take_user(int(i))[2]+1)
				except Exception as ex:
					print(str(ex))
					continue
			running_game.append(idd)

			k = 2
			#Цикл гри
			while len(one_game(idd)[2].split(',')) != 1 and ',' in one_game(idd)[2]:
				print('Цикл 1')
				while one_game(idd)[5]+1 < len(one_game(idd)[2].split(',')): # and ',' in one_game(idd)[2]
					print('Цикл 2')
					#print(one_game(idd)[2].split(','))
					print(f"{str(one_game(idd)[5])} != {str(len(one_game(idd)[2].split(',')))}")
					await asyncio.sleep(0.5)
				upd_mark_game(idd, 0)
				u = []
				if ',' not in one_game(idd)[2]:
					break
				l = one_game(idd)[2].split(',')
				l = random.shuffle(l)
				print(f'SHUFFLED LIST {l}')
				try:
					print(len(l))
				except:
					l = one_game(idd)[2].split(',')
				game_data = one_game(idd)
				for i in range(len(l)):
					if i in u:
						continue
					delete(int(l[i]))
					try:
						delete(int(l[i+1]))
					except:
						pass
					try:
						add_part(game_data[1],int(l[i]),int(l[i+1]))
						add_part(game_data[1],int(l[i+1]),int(l[i]))
					except:
						#await bot.send_message(int(l[i]), 'У тебя нету пары, поэтому ты проходишь во второй тур ;)')
						add_part(game_data[1],int(l[i]),0)
						#upd_mark_game(idd, one_game(idd)[5]+1)
						upd_code(int(l[i]),2)
						#upd_current_game(int(l[i]),1)
					u.append(i+1)

				for i in l:
					print('СМС КОЖНОМУ ГРАВЦЮ, ХТО ЧИЙ ОПОНЕНТ')
					#await bot.send_message(int(i), f'РАУНД {k}')
					if len(one_game(idd)[2].split(',')) == 2:
						f = open('финиал.tgs', 'rb')
						await bot.send_sticker(int(i), f)
					elif len(one_game(idd)[2].split(',')) == 4:
						f = open('полуфинал.tgs', 'rb')
						await bot.send_sticker(int(i), f)
					print(f'{k}.tgs')
					if len(one_game(idd)[2].split(',')) != 2 and len(one_game(idd)[2].split(',')) != 4:
						f = open(f'раунд{k}.tgs', 'rb')
						await bot.send_sticker(int(i), f)
					if participant(int(i))[3] == 0:
						await bot.send_message(int(i), f'Твой оппонент: {random.choice(bots)}', reply_markup=choice())
						continue
					await bot.send_message(int(i), f'Твой оппонент: {take_user(participant(int(i))[3])[6]}', reply_markup=choice())
				k += 1

			winner = one_game(idd)[2]
			f = open('ты чемпион.tgs', 'rb')
			await bot.send_sticker(int(winner), f)
			await bot.send_message(int(winner), 'Ты победил! Чтобы забрать виигрыш - напиши ему @arthur_belousov')
			delete_game(idd)
			upd_current_game(int(winner),0)
			try:
				delete(int(winner))
			except:
				pass


@dp.callback_query_handler()
async def main(call: CallbackQuery):
	if not take_user(call.message.chat.id):
		await call.message.answer('Нажми сначало /start', reply_markup=list_game(call.message.chat.id))
		return 0	
	print(call.data)
	
	if 'join' in call.data:
		if current_game_user(call.message.chat.id)[5] == 1:
			await call.message.answer('Ты уже зарегистрировался в игру', reply_markup=list_game(call.message.chat.id))
		elif one_game_id(int(call.data.split(':')[1]))[4] > take_user(call.message.chat.id)[3]:
			await call.message.answer('Недостаточно средста на кошельке', reply_markup=list_game(call.message.chat.id))
		else:
			current_game = one_game_id(int(call.data.split(':')[1]))
			if current_game[2] == '0':
				upd_user_game(current_game[0],str(call.message.chat.id))
			else:
				upd_user_game(current_game[0], current_game[2]+','+str(call.message.chat.id))
			await call.message.answer('Ты успешно зарегистрировался в игру')
			upd_current_game(call.message.chat.id,1)
			upd_wallet(call.message.chat.id, take_user(call.message.chat.id)[3]-one_game(current_game[1])[4])

	elif 'back' in call.data or 'back' == call.data:
		await bot.send_message(call.message.chat.id, 'Выбери из меню нужный пункты', reply_markup=list_game(call.message.chat.id))
		try:
			await bot.delete_message(call.message.chat.id, call.message.message_id)
			await bot.delete_message(call.message.chat.id, call.message.message_id-1)
		except:
			pass
	
	elif 'check' in call.data:
		res = await check(call.data.split(':')[1])
		#res = await get_result(call.data.split(':')[1])
		current_game = one_game_id(int(call.data.split(':')[2]))
		print(f'Result of payment: {res}')
		if res == 'success' or res == 'wait_accept':
			await bot.send_message(call.message.chat.id, f'Поздравляю ты успешно зарегистрировался! \n Ждём тебя {current_game[3]}')
			#upd_wallet(call.message.chat.id, take_user(call.message.chat.id)[3]+take_user_pay(call.message.chat.id)[3])
			delete_pay(call.message.chat.id)
			for i in range(6):
				try:
					await bot.delete_message(call.message.chat.id, call.message.message_id-i)
				except:
					continue
			if current_game[2] == '0':
				upd_user_game(current_game[0],str(call.message.chat.id))
			else:
				upd_user_game(current_game[0], current_game[2]+','+str(call.message.chat.id))
			#await call.message.answer('Ты успешно зарегистрировался в игру')
			upd_current_game(call.message.chat.id,1)
			#upd_wallet(call.message.chat.id, take_user(call.message.chat.id)[3]-one_game(current_game[1])[4])

		else:
			await bot.send_message(call.message.chat.id, 'Оплата не прошла', reply_markup=list_game(call.message.chat.id))

	elif 'reg' in call.data: #add_user(message.chat.id, str(message.chat.first_name))
		if current_game_user(call.message.chat.id)[5] == 1:
			await call.message.answer('Ты уже зарегистрировался в игру')		
			return 0
		if one_game_id(int(call.data.split(':')[1])):
			current_game = one_game_id(int(call.data.split(':')[1]))
			if one_game_id(int(call.data.split(':')[1]))[4] == 0:
				if current_game[2] == '0':
					upd_user_game(current_game[0],str(call.message.chat.id))
				else:
					upd_user_game(current_game[0], current_game[2]+','+str(call.message.chat.id))
				await call.message.answer('Ты успешно зарегистрировался в игру')
				upd_current_game(call.message.chat.id,1)
				return 0
			current_game = one_game_id(int(call.data.split(':')[1]))
			id_order = random.randint(100000,10000000000)
			phone = '38099'+ str(random.randint(1000000,9999999))
			
			url = await create_pay(id_order,int(current_game[4])*100)
			#url = await make_req(current_game[4], phone, id_order)
			await call.message.answer('Для принятия участия нажми "Регистрация"', reply_markup=pay(url,id_order,current_game[0]))
			add_user_pay(call.message.chat.id, int(phone), current_game[4])
		else:
			await call.message.answer('К сожелению, игра была удалена, мы сообщим о новом турнире ;)')

	elif 'doc' == call.data:
		f = open('ДОГОВОР.docx', 'rb')
		await bot.send_document(call.message.chat.id, f)

	try:
		if 'check' in call.data or 'reg' in call.data:
			return 0
		await bot.delete_message(call.message.chat.id, call.message.message_id)
	except:
		pass
		













@dp.message_handler(commands=['show'])
async def start(message: types.Message):
	for i in all_game():
		await bot.send_message(message.chat.id, f'Игра: {str(i[1])}' + '\n' + f'Игроки: {i[2]}' + '\n' + f'Старт: {i[3]}' + '\n' + f'Ставка: {str(i[4])}', reply_markup=join(str(i[0])))

@dp.message_handler(state= pay_m.summ)
async def process_summ(message: types.Message, state: FSMContext):
	async with state.proxy() as data:
		data['summ'] = message.text
	print(data['summ'])
	await pay_m.next()
	await message.answer('Напиши номер телефона!')

@dp.message_handler(state= pay_m.phone)
async def process_phone(message: types.Message, state: FSMContext):
	await pay_m.next()
	await state.update_data(phone=int(message.text))
	async with state.proxy() as data:
		print(data)
	await state.finish()

	id_order = random.randint(100000,10000000000)
	url = await make_req(data['summ'], data['phone'], id_order)
	await message.answer('Оплати и начинай играть!', reply_markup=pay(url,id_order))
	add_user_pay(message.chat.id, int(data['phone']), int(data['summ']))


@dp.message_handler(state=Mailing.sms)
async def process_sms(message: types.Message, state: FSMContext):
	if message.text == 'Назад':
		await state.finish()
		await message.answer('Меню', reply_markup=list_game(message.chat.id))
		return 0

	async with state.proxy() as data:
		data['sms'] = message.text
	users = take_user_all()
	for i in users:
		await bot.send_message(i[1], data['sms'])
	await bot.send_message(message.chat.id, 'Рассылка закончена', reply_markup=back)
	await state.finish()

# if 'Найти' in message.text:
# 		await bot.send_message(message.chat.id, 'Все игры:', reply_markup=back_k)
# 		for i in all_game():
# 			if i[1] in running_game:
# 				continue
# 			else:
# 				if '0' == i[2]:
# 					await bot.send_message(message.chat.id, f'ID игры: {str(i[1])}' + '\n' + 'Количество игроков: 0' + '\n' + f'Старт: {i[3]}' + '\n' + f'Главный выигрыш: {i[6]}.', reply_markup=reg(str(i[0])))
# 				else:
# 					await bot.send_message(message.chat.id, f'ID игры: {str(i[1])}' + '\n' + f'Количество игроков: {len(i[2].split(","))}' + '\n' + f'Старт: {i[3]}' + '\n' + f'Главный выигрыш: {i[6]}.', reply_markup=reg(str(i[0])))

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)