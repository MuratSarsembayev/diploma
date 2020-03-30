
from aiogram import types
from asyncpg import Connection, Record
from asyncpg.exceptions import UniqueViolationError
from keyboards import ListOfButtons
from load_all import bot, dp, db
from filters import *
from aiogram.types.reply_keyboard import ReplyKeyboardRemove

city_a = ""
city_b = ""
date = ""

keyboard = ListOfButtons(text=["Отправить", "Перевезти"]).reply_keyboard
class DBCommands:
    pool: Connection = db
    ADD_NEW_USER = "INSERT INTO users(chat_id, username, full_name) VALUES ($1, $2, $3)"
    ADD_NEW_SENDER = "INSERT INTO senders(username, city_a, city_b, send_date) VALUES ($1, $2, $3, $4)"
    ADD_NEW_TAKER = "INSERT INTO takers(username, city_a, city_b, take_date) VALUES ($1, $2, $3, $4)"
    SELECT_SENDERS = "SELECT * FROM senders(username, city_a, city_b, send_date)" \
                     " WHERE city_a=($1) AND city_b=($2) AND send_date=($3)"
    SELECT_TAKERS = "SELECT * FROM takers(username, city_a, city_b, take_date)" \
                     " WHERE city_a=($1) AND city_b=($2) AND take_date=($3)"

    async def add_new_user(self):
        user = types.User.get_current()
        chat_id = user.id
        username = user.username
        full_name = user.full_name
        args = chat_id, username, full_name
        command = self.ADD_NEW_USER

        try:
            record_id = await self.pool.fetchval(command, *args)
            return record_id
        except UniqueViolationError:
            pass

    async def add_new_sender(self, city_a, city_b, send_date):
        user = types.User.get_current()
        username = user.username
        args = username, city_a, city_b, send_date
        command = self.ADD_NEW_SENDER
        try:
            record_id = await self.pool.fetchval(command, *args)
            return record_id
        except UniqueViolationError:
            pass

    async def add_new_taker(self, city_a, city_b, take_date):
        user = types.User.get_current()
        username = user.username
        args = username, city_a, city_b, take_date
        command = self.ADD_NEW_TAKER
        try:
            record_id = await self.pool.fetchval(command, *args)
            return record_id
        except UniqueViolationError:
            pass

    async def show_senders(self, city_a, city_b, send_date):
        args = city_a, city_b, send_date
        command = self.SELECT_SENDERS
        try:
            data = await self.pool.fetch(command, *args)
            return data
        except UniqueViolationError:
            pass

    async def show_takers(self, city_a, city_b, take_date):
        args = city_a, city_b, take_date
        command = self.SELECT_TAKERS
        try:
            data = await self.pool.fetch(command, *args)
            return data
        except UniqueViolationError:
            pass


db = DBCommands()


@dp.message_handler(commands=["start"])
async def register_user(message: types.Message):
    chat_id = message.from_user.id
    id = await db.add_new_user()
    text = ""
    text += f"""
Добро пожаловать в систему Apar Bot.
Вы зарегистрированы.
Желаете отправить посылку или перевезти посылку?

"""

    await bot.send_message(chat_id, text, reply_markup=keyboard)


@dp.message_handler(Button("Отправить"))
async def send(message: Message):
    await message.reply("Введите название города, из которого Вы хотите отправить посылку",
                        reply_markup=ReplyKeyboardRemove())


@dp.message_handler()
async def send(message: Message):
        global city_a
        city_a = message.text
        await message.reply("Введите название города, в который Вы хотите отправить посылку")


@dp.message_handler()
async def send(message: Message):
        global city_b
        city_b = message.text
        await message.reply("Введите дату, когда вы хотите отправить посылку. Дату нужно ввести в формате ДД/ММ/ГГГГ")


@dp.message_handler()
async def send(message: Message):
        global date
        date = message.text
        await db.add_new_sender(city_a, city_b, date)
        text = f""""""
        text += str(await db.show_senders(city_a, city_b, date))
        await message.reply(text,
                        reply_markup=keyboard)



@dp.message_handler(Button("Перевезти"))
async def send(message: Message):
        await message.reply("Введите название города, из которого Вы хотите перевезти посылку",
                        reply_markup=ReplyKeyboardRemove())


@dp.message_handler()
async def send(message: Message):
        global city_a
        city_a = message.text
        await message.reply("Введите название города, в который Вы хотите перевезти посылку")


@dp.message_handler()
async def send(message: Message):
        global city_b
        city_b = message.text
        await message.reply("Введите дату, когда вы можете перевезти посылку. Дату нужно ввести в формате ДД/ММ/ГГГГ")


@dp.message_handler()
async def send(message: Message):
        global date
        date = message.text
        await db.add_new_taker(city_a, city_b, date)
        text = f""""""
        text += str(await db.show_takers(city_a, city_b, date))
        await message.reply(text,
                        reply_markup=keyboard)










