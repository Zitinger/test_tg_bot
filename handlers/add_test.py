from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import sqlite3


class CreatingTest(StatesGroup):
    waiting_for_test_name = State()
    waiting_for_first_question = State()
    waiting_for_first_answers = State()
    waiting_for_first_right_answer = State()
    waiting_for_second_question = State()
    waiting_for_second_answers = State()
    waiting_for_second_right_answer = State()
    waiting_for_third_question = State()
    waiting_for_third_answers = State()
    waiting_for_third_right_answer = State()
    waiting_for_fourth_question = State()
    waiting_for_fourth_answers = State()
    waiting_for_fourth_right_answer = State()
    waiting_for_fifth_question = State()
    waiting_for_fifth_answers = State()
    waiting_for_fifth_right_answer = State()
    saving_test = State()


async def test_name(message: types.Message):
    await message.answer(f"Введите название теста:", reply_markup=types.ReplyKeyboardRemove())
    await CreatingTest.waiting_for_test_name.set()


async def get_first_question(message: types.Message, state: FSMContext):
    await state.update_data(test_name=message.text)
    await message.answer(f"Введите первый вопрос:")
    await CreatingTest.next()


async def get_first_answers(message: types.Message, state: FSMContext):
    await state.update_data(first_question=message.text)
    await message.answer(f"Введите три варианта ответа через Enter:")
    await CreatingTest.next()


async def get_first_right_answer(message: types.Message, state: FSMContext):
    if message.text.count("\n") != 2:
        await message.answer(f"Введите три варианта ответа через Enter:")
        return
    answers = message.text.split('\n')
    await state.update_data(first_answers=answers)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*['1', '2', '3'])
    await message.answer(f"Введите номер правильного варианта ответа: (1, 2 или 3)",  reply_markup=keyboard)
    await CreatingTest.next()


async def get_second_question(message: types.Message, state: FSMContext):
    if not message.text.isdigit() or message.text not in ['1', '2', '3']:
        await message.answer(f"Введите номер правильного варианта ответа: (1, 2 или 3)")
        return
    await state.update_data(first_right_answer=message.text)
    await message.answer(f"Введите второй вопрос:", reply_markup=types.ReplyKeyboardRemove())
    await CreatingTest.next()


async def get_second_answers(message: types.Message, state: FSMContext):
    await state.update_data(second_question=message.text)
    await message.answer(f"Введите три варианта ответа через Enter:")
    await CreatingTest.next()


async def get_second_right_answer(message: types.Message, state: FSMContext):
    if message.text.count("\n") != 2:
        await message.answer(f"Введите три варианта ответа через Enter:")
        return
    answers = message.text.split('\n')
    await state.update_data(second_answers=answers)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*['1', '2', '3'])
    await message.answer(f"Введите номер правильного варианта ответа: (1, 2 или 3)",  reply_markup=keyboard)
    await CreatingTest.next()


async def get_third_question(message: types.Message, state: FSMContext):
    if not message.text.isdigit() or message.text not in ['1', '2', '3']:
        await message.answer(f"Введите номер правильного варианта ответа: (1, 2 или 3)")
        return
    await state.update_data(second_right_answer=message.text)
    await message.answer(f"Введите третий вопрос:", reply_markup=types.ReplyKeyboardRemove())
    await CreatingTest.next()


async def get_third_answers(message: types.Message, state: FSMContext):
    await state.update_data(third_question=message.text)
    await message.answer(f"Введите три варианта ответа через Enter:")
    await CreatingTest.next()


async def get_third_right_answer(message: types.Message, state: FSMContext):
    if message.text.count("\n") != 2:
        await message.answer(f"Введите три варианта ответа через Enter:")
        return
    answers = message.text.split('\n')
    await state.update_data(third_answers=answers)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*['1', '2', '3'])
    await message.answer(f"Введите номер правильного варианта ответа: (1, 2 или 3)",  reply_markup=keyboard)
    await CreatingTest.next()


async def get_fourth_question(message: types.Message, state: FSMContext):
    if not message.text.isdigit() or message.text not in ['1', '2', '3']:
        await message.answer(f"Введите номер правильного варианта ответа: (1, 2 или 3)")
        return
    await state.update_data(third_right_answer=message.text)
    await message.answer(f"Введите четвертый вопрос.", reply_markup=types.ReplyKeyboardRemove())
    await CreatingTest.next()


async def get_fourth_answers(message: types.Message, state: FSMContext):
    await state.update_data(fourth_question=message.text)
    await message.answer(f"Введите три варианта ответа через Enter.")
    await CreatingTest.next()


async def get_fourth_right_answer(message: types.Message, state: FSMContext):
    if message.text.count("\n") != 2:
        await message.answer(f"Введите три варианта ответа через Enter.")
        return
    answers = message.text.split('\n')
    await state.update_data(fourth_answers=answers)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*['1', '2', '3'])
    await message.answer(f"Введите номер правильного варианта ответа. (1, 2 или 3)",  reply_markup=keyboard)
    await CreatingTest.next()


async def get_fifth_question(message: types.Message, state: FSMContext):
    if not message.text.isdigit() or message.text not in ['1', '2', '3']:
        await message.answer(f"Введите номер правильного варианта ответа. (1, 2 или 3)")
        return
    await state.update_data(fourth_right_answer=message.text)
    await message.answer(f"Введите пятый вопрос.", reply_markup=types.ReplyKeyboardRemove())
    await CreatingTest.next()


async def get_fifth_answers(message: types.Message, state: FSMContext):
    await state.update_data(fifth_question=message.text)
    await message.answer(f"Введите три варианта ответа через Enter.")
    await CreatingTest.next()


async def get_fifth_right_answer(message: types.Message, state: FSMContext):
    if message.text.count("\n") != 2:
        await message.answer(f"Введите три варианта ответа через Enter.")
        return
    answers = message.text.split('\n')
    await state.update_data(fifth_answers=answers)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*['1', '2', '3'])
    await message.answer(f"Введите номер правильного варианта ответа. (1, 2 или 3)", reply_markup=keyboard)
    await CreatingTest.next()


async def saving_test(message: types.Message, state: FSMContext):
    if not message.text.isdigit() or message.text not in ['1', '2', '3']:
        await message.answer(f"Введите номер правильного варианта ответа. (1, 2 или 3)")
        return
    await state.update_data(fifth_right_answer=message.text)

    db = sqlite3.connect('database.db')
    cur = db.cursor()
    data = await state.get_data()
    print(data)

    # добавление теста в базу данных
    right_answers = data['first_right_answer'] + data['second_right_answer'] + data['third_right_answer'] + \
                    data['fourth_right_answer'] + data['fifth_right_answer']
    cur.execute(f"INSERT INTO tests(name, right_answers) VALUES('{data['test_name']}', '{right_answers}')")

    # добавление вопросов к нему
    questions = [data['first_question'], data['second_question'], data['third_question'],
                 data['fourth_question'], data['fifth_question']]
    for i in range(1, 6):
        cur.execute(f"INSERT INTO questions(test_id, text, question_number) "
                    f"VALUES((SELECT test_id FROM tests WHERE name='{data['test_name']}'), '{questions[i - 1]}', {i})")

    # добавление ответов
    answers = [data['first_answers'], data['second_answers'], data['third_answers'],
               data['fourth_answers'], data['fifth_answers']]
    for i in range(1, 6):
        for j in range(1, 4):
            cur.execute(f"INSERT INTO answers(question_id, text) "
                        f"VALUES((SELECT id FROM "
                        f"(SELECT * FROM tests JOIN questions ON tests.test_id = questions.test_id) "
                        f"WHERE name = '{data['test_name']}' AND question_number = {i}), '{answers[i - 1][j - 1]}')")

    db.commit()
    db.close()
    await state.finish()
    await message.answer(f"Тест добавлен ✅", reply_markup=types.ReplyKeyboardRemove())


def register_handlers_add_test(dp: Dispatcher):
    dp.register_message_handler(test_name, commands="add_test", state="*")
    dp.register_message_handler(get_first_question, state=CreatingTest.waiting_for_test_name)
    dp.register_message_handler(get_first_answers, state=CreatingTest.waiting_for_first_question)
    dp.register_message_handler(get_first_right_answer, state=CreatingTest.waiting_for_first_answers)
    dp.register_message_handler(get_second_question, state=CreatingTest.waiting_for_first_right_answer)
    dp.register_message_handler(get_second_answers, state=CreatingTest.waiting_for_second_question)
    dp.register_message_handler(get_second_right_answer, state=CreatingTest.waiting_for_second_answers)
    dp.register_message_handler(get_third_question, state=CreatingTest.waiting_for_second_right_answer)
    dp.register_message_handler(get_third_answers, state=CreatingTest.waiting_for_third_question)
    dp.register_message_handler(get_third_right_answer, state=CreatingTest.waiting_for_third_answers)
    dp.register_message_handler(get_fourth_question, state=CreatingTest.waiting_for_third_right_answer)
    dp.register_message_handler(get_fourth_answers, state=CreatingTest.waiting_for_fourth_question)
    dp.register_message_handler(get_fourth_right_answer, state=CreatingTest.waiting_for_fourth_answers)
    dp.register_message_handler(get_fifth_question, state=CreatingTest.waiting_for_fourth_right_answer)
    dp.register_message_handler(get_fifth_answers, state=CreatingTest.waiting_for_fifth_question)
    dp.register_message_handler(get_fifth_right_answer, state=CreatingTest.waiting_for_fifth_answers)
    dp.register_message_handler(saving_test, state=CreatingTest.waiting_for_fifth_right_answer)
