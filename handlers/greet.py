from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import aiogram.utils.markdown as fmt
import sqlite3



class Greeting(StatesGroup):
    waiting_for_the_name = State()


async def ask_name(message: types.Message):
    db = sqlite3.connect('database.db')
    cur = db.cursor()
    res = cur.execute(f"SELECT * FROM users_names WHERE id = '{message['from']['id']}'").fetchall()
    if res:
        await message.answer(f'Привет, {res[0][-1]}! '
                             f'Чтобы узнать список комманд введите <b>{fmt.quote_html("/help")}</b>')
    else:
        await message.answer("Привет! Как тебя зовут?")
        await Greeting.waiting_for_the_name.set()
    db.close()


async def save_name(message: types.Message, state: FSMContext):
    username = message.text
    db = sqlite3.connect('database.db')
    cur = db.cursor()
    cur.execute(f"INSERT INTO users_names(id, name) VALUES({message['from']['id']}, '{username}')")
    db.commit()
    await message.answer(
        f'Приятно познакомиться, {username}! Я Никита.\n'
        f'Чтобы узнать список комманд введите <b>{fmt.quote_html("/help")}</b>')
    await state.finish()
    db.close()


def register_handlers_greet(dp: Dispatcher):
    dp.register_message_handler(ask_name, commands="start", state="*")
    dp.register_message_handler(save_name, state=Greeting.waiting_for_the_name)
