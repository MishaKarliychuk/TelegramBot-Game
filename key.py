from aiogram.types.inline_keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, KeyboardButton
from config import admin
import random
#from db import *

back = InlineKeyboardMarkup()
bb1 = InlineKeyboardButton(text='Назад', callback_data='back')
back.insert(bb1)

back_k = ReplyKeyboardMarkup(resize_keyboard=True)
bb2 = KeyboardButton('Назад')
back_k.insert(bb2)


def join(id):
	key = InlineKeyboardMarkup()
	b1 = InlineKeyboardButton(text='Присоединится', callback_data=f'join:{id}')
	key.row(b1)
	return key



def list_game(id_):
	global admin
	key = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
	if id_ in admin:
		b5 = KeyboardButton('Создать игру')
		key.insert(b5)
		b6 = KeyboardButton('Расылка')
		key.insert(b6)
		b7 = KeyboardButton('Удалить все игры')
		key.row(b7)
		#b7 = KeyboardButton('Статистика')
		#key.insert(b7)
	else:
		#1 = KeyboardButton('Найти игру')
		#key.insert(b1)
		b3 = KeyboardButton('Профиль')
		key.insert(b3)
		#b4 = KeyboardButton('Пополнить')
		#key.insert(b4)
	return key

def choice():
	key = ReplyKeyboardMarkup(resize_keyboard=True)
	b1 = KeyboardButton('Камень')
	key.row(b1)
	b1 = KeyboardButton('Ножницы')
	key.row(b1)
	b1 = KeyboardButton('Бумага')
	key.row(b1)
	return key

def pay(url,id_order,id_g):
	key = InlineKeyboardMarkup()
	b1 = InlineKeyboardButton(text='Регистрация', url=url)
	key.row(b1)
	b2 = InlineKeyboardButton(text='Подтвердить оплату', callback_data=f'check:{id_order}:{id_g}')
	key.row(b2)
	return key

def reg(id_):
	key = InlineKeyboardMarkup()
	b1 = InlineKeyboardButton(text='Зарегистрироваться', callback_data=f'reg:{id_}')
	key.row(b1)
	b2 = InlineKeyboardButton(text='Публичная оферта', url='https://docs.google.com/document/d/1dlEm7K6mTajl3Tvkc989jmIY3jDG52MiRzNMWRknNtA/edit?usp=drivesdk')
	key.row(b2)
	return key