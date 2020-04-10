
from aiogram import types
from asyncpg import Connection, Record
from asyncpg.exceptions import UniqueViolationError
from keyboards import ListOfButtons
from load_all import bot, dp, db
from filters import *
from aiogram.types.reply_keyboard import ReplyKeyboardRemove
from aiogram.dispatcher.storage import FSMContext
from states import States
from datetime import datetime, date

keyboard = ListOfButtons(text=["Отправить", "Перевезти"]).reply_keyboard


class DBCommands:
    pool: Connection = db
    ADD_NEW_USER = "INSERT INTO users (chat_id, username, full_name) VALUES ($1, $2, $3)"
    ADD_NEW_SENDER = "INSERT INTO senders (username, city_a, city_b, send_date) VALUES ($1, $2, $3, $4)"
    ADD_NEW_TAKER = "INSERT INTO takers (username, city_a, city_b, take_date) VALUES ($1, $2, $3, $4)"
    SELECT_SENDERS = "SELECT (username, city_a, city_b) FROM senders " \
                     " WHERE city_a= ($1) AND city_b=($2) AND send_date=($3)"
    SELECT_TAKERS = "SELECT (username, city_a, city_b) FROM takers" \
                    " WHERE city_a= ($1) AND city_b=($2) AND take_date=($3)"

    async def add_new_user(self):
        user = types.User.get_current()
        chat_id = int(user.id)
        username = user.username
        full_name = user.full_name
        args = chat_id, username, full_name
        command = self.ADD_NEW_USER

        try:
            record_id = await self.pool.fetchval(command, *args)
            return record_id
        except UniqueViolationError:
            pass

    async def add_new_sender(self, city_a, city_b, senddate):
        user = types.User.get_current()
        username = user.username
        send_date = datetime.strptime(senddate, '%Y-%M-%d')
        args = username, city_a, city_b, send_date
        command = self.ADD_NEW_SENDER
        try:
            record_id = await self.pool.fetchval(command, *args)
            return record_id
        except UniqueViolationError:
            pass

    async def add_new_taker(self, city_a, city_b, takedate):
        user = types.User.get_current()
        username = user.username
        take_date = datetime.strptime(takedate, '%Y-M-%d')
        args = username, city_a, city_b, take_date
        command = self.ADD_NEW_TAKER
        try:
            record_id = await self.pool.fetchval(command, *args)
            return record_id
        except UniqueViolationError:
            pass

    async def show_senders(self, city_a, city_b, senddate):
        send_date = datetime.strptime(senddate, '%Y-%M-%d')
        args = city_a, city_b, send_date
        command = self.SELECT_SENDERS
        try:
            data = await self.pool.fetch(command, *args)
            return len(data)
        except UniqueViolationError:
            pass

    async def show_takers(self, city_a, city_b, takedate):
        take_date = datetime.strptime(takedate, '%Y-%M-%d')
        args = city_a, city_b, take_date
        command = self.SELECT_TAKERS
        try:
            data = await self.pool.fetch(command, *args)
            return len(data)
        except UniqueViolationError:
            pass


db = DBCommands()


@dp.message_handler(commands=["start"])
async def register_user(message: types.Message):
    chat_id = message.from_user.id
    await db.add_new_user()
    text = ""
    text += f"""
Добро пожаловать в систему Apar Bot.
Вы зарегистрированы.
Желаете отправить посылку или перевезти посылку?

"""

    await bot.send_message(chat_id, text, reply_markup=keyboard)


@dp.message_handler(Button("Отправить"))
async def send_city_a(message: Message):
    await message.reply("Введите название города, из которого Вы хотите отправить посылку",
                        reply_markup=ReplyKeyboardRemove())
    await States.Send_City_A.set()


@dp.message_handler(state=States.Send_City_A)
async def send_city_b(message: Message, state: FSMContext):
        city_a = message.text
        await state.update_data(city_a= city_a)
        await message.reply("Введите название города, в который Вы хотите отправить посылку")
        await States.Send_City_B.set()


@dp.message_handler(state=States.Send_City_B)
async def send_date_day(message: Message, state: FSMContext):
        city_b = message.text
        await state.update_data(city_b=city_b)
        await message.reply("Введите день, когда вы хотите отправить посылку(1-31)")
        await States.Send_Day.set()


@dp.message_handler(state= States.Send_Day)
async def send_date_month(message: Message, state: FSMContext):
        day = message.text
        await state.update_data(day=day)
        await message.reply("Введите месяц, когда вы хотите отправить посылку(1-12)")
        await States.Send_Month.set()


@dp.message_handler(state=States.Send_Month)
async def send_date_year(message: Message, state: FSMContext):
        month = message.text
        await state.update_data(month=month)
        await message.reply("Введите год, когда вы хотите отправить посылку(1-9999)")
        await States.Send_Year.set()


@dp.message_handler(state=States.Send_Year)
async def send_show_takers(message: Message, state: FSMContext):
        year = int(message.text)
        data = await state.get_data()
        city_a = data.get("city_a")
        city_b = data.get("city_b")
        day = int(data.get("day"))
        month = int(data.get("month"))
        send_date = date(year, month, day).isoformat()
        await db.add_new_sender(city_a, city_b, send_date)
        takers = await db.show_takers(city_a, city_b, send_date)
        #for i in takers:
         #   text = " ".join(takers[i])
          #  await message.answer(text)
        text = str(takers)
        await message.answer(text)
        await state.reset_state()


@dp.message_handler(Button("Перевезти"))
async def take_city_a(message: Message):
        await message.reply("Введите название города, из которого Вы хотите перевезти посылку",
                        reply_markup=ReplyKeyboardRemove())
        await States.Take_City_A.set()


@dp.message_handler(state=States.Take_City_A)
async def take_city_b(message: Message, state: FSMContext):
        city_a = message.text
        await state.update_data(city_a=city_a)
        await message.reply("Введите название города, в который Вы хотите перевезти посылку")
        await States.Take_City_B.set()


@dp.message_handler(state=States.Take_City_B)
async def take_date_day(message: Message, state: FSMContext):
        city_b = message.text
        await state.update_data(city_b=city_b)
        await message.reply("Введите день, когда вы можете перевезти посылку(1-31)")
        await States.Take_Day.set()


@dp.message_handler(state=States.Take_Day)
async def take_date_month(message: Message, state: FSMContext):
        day = message.text
        await state.update_data(day=day)
        await message.reply("Введите месяц, когда вы можете перевезти посылку(1-12)")
        await States.Take_Month.set()


@dp.message_handler(state=States.Take_Month)
async def take_date_year(message: Message, state: FSMContext):
        month = message.text
        await state.update_data(month= month)
        await message.reply("Введите год, когда вы можете перевезти посылку(1-9999)")
        await States.Send_Year.set()


@dp.message_handler(state=States.Take_Year)
async def send_show_senders(message: Message, state: FSMContext):
        year = int(message.text)
        data = await state.get_data()
        city_a = data.get("city_a")
        city_b = data.get("city_b")
        day = int(data.get("day"))
        month = int(data.get("month"))
        take_date = date(year, month, day).isoformat()
        await db.add_new_taker(city_a, city_b, take_date)
        senders = await db.show_senders(city_a, city_b, take_date)
        #for i in senders:
         #   text = " ".join(senders[i])
          #  await message.answer(text)
        text = str(senders)
        await message.answer(text)
        await state.reset_state()


@dp.message_handler()
async def default_message(message: Message):
    text = ""
    text += f"""
    Добро пожаловать в систему Apar Bot.
    Вы зарегистрированы.
    Желаете отправить посылку или перевезти посылку?

    """
    await bot.send_message(text, reply_markup=keyboard)









