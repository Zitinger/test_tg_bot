from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import sqlite3
import aiogram.utils.markdown as fmt


class SolvingTest(StatesGroup):
    waiting_for_choose_test = State()
    waiting_for_first_answer = State()
    waiting_for_second_answer = State()
    waiting_for_third_answer = State()
    waiting_for_fourth_answer = State()
    waiting_for_fifth_answer = State()


async def choose_test(message: types.Message):
    db = sqlite3.connect('database.db')
    cur = db.cursor()
    res = cur.execute(f'SELECT test_id, name FROM tests').fetchall()
    res.sort(key=lambda x: x[0])
    await message.answer(f"Выберите тест:  (выберите его ID)\n\n" +
                         "\n".join([f"{n}. {name}" for n, name in res]), reply_markup=types.ReplyKeyboardRemove())
    await SolvingTest.waiting_for_choose_test.set()
    db.close()


async def first_question(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Пожалуйста, укажите номер теста.")
        return
    db = sqlite3.connect('database.db')
    cur = db.cursor()
    res = cur.execute(f'SELECT rowid, name FROM tests').fetchall()
    right_answers = cur.execute(f"SELECT right_answers FROM tests WHERE test_id={int(message.text)}").fetchone()[0]
    if int(message.text) not in [n[0] for n in res]:
        await message.answer("Пожалуйста, укажите номер теста.")
        return
    await state.update_data(right_answers=str(right_answers))
    await state.update_data(chosen_test=int(message.text))

    res = cur.execute(f"SELECT id, text FROM questions "
                      f"WHERE test_id = {int(message.text)} AND question_number = 1").fetchone()
    question_id, question = res
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

    res = cur.execute(f"SELECT text FROM answers WHERE question_id={question_id}").fetchall()
    answers = [str(obj[0]) for obj in res]

    keyboard.add(*['1', '2', '3'])
    db.close()

    await SolvingTest.next()
    await message.answer(f"Вопрос 1\n\n{question}\n\n· " +
                         "\n· ".join(answers), reply_markup=keyboard)


async def second_question(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Пожалуйста, укажите вариант ответа (1-3).")
        return
    if int(message.text) not in [1, 2, 3]:
        await message.answer("Пожалуйста, укажите вариант ответа (1-3).")
        return
    db = sqlite3.connect('database.db')
    cur = db.cursor()
    await state.update_data(first_answer=message.text)
    data = await state.get_data()
    res = cur.execute(f"SELECT id, text FROM questions "
                      f"WHERE test_id = {data['chosen_test']} AND question_number = 2").fetchone()
    question_id, question = res

    res = cur.execute(f"SELECT text FROM answers WHERE question_id={question_id}").fetchall()
    answers = [str(obj[0]) for obj in res]
    print(answers)
    db.close()

    await SolvingTest.next()
    await message.answer(f"Вопрос 2\n\n{question}\n\n· " +
                         "\n· ".join(answers))


async def third_question(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Пожалуйста, укажите вариант ответа (1-3).")
        return
    if int(message.text) not in [1, 2, 3]:
        await message.answer("Пожалуйста, укажите вариант ответа (1-3).")
        return
    db = sqlite3.connect('database.db')
    cur = db.cursor()
    await state.update_data(second_answer=message.text)
    data = await state.get_data()
    res = cur.execute(f"SELECT id, text FROM questions "
                      f"WHERE test_id = {data['chosen_test']} AND question_number = 3").fetchone()
    question_id, question = res

    res = cur.execute(f"SELECT text FROM answers WHERE question_id={question_id}").fetchall()
    answers = [str(obj[0]) for obj in res]

    db.close()

    await SolvingTest.next()
    await message.answer(f"Вопрос 3\n\n{question}\n\n· " +
                         "\n· ".join(answers))


async def fourth_question(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Пожалуйста, укажите вариант ответа (1-3).")
        return
    if int(message.text) not in [1, 2, 3]:
        await message.answer("Пожалуйста, укажите вариант ответа (1-3).")
        return
    db = sqlite3.connect('database.db')
    cur = db.cursor()
    await state.update_data(third_answer=message.text)
    data = await state.get_data()
    res = cur.execute(f"SELECT id, text FROM questions "
                      f"WHERE test_id = {data['chosen_test']} AND question_number = 4").fetchone()
    question_id, question = res

    res = cur.execute(f"SELECT text FROM answers WHERE question_id={question_id}").fetchall()
    answers = [str(obj[0]) for obj in res]

    db.close()

    await SolvingTest.next()
    await message.answer(f"Вопрос 4\n\n{question}\n\n· " +
                         "\n· ".join(answers))


async def fifth_question(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Пожалуйста, укажите вариант ответа (1-3).")
        return
    if int(message.text) not in [1, 2, 3]:
        await message.answer("Пожалуйста, укажите вариант ответа (1-3).")
        return
    db = sqlite3.connect('database.db')
    cur = db.cursor()
    await state.update_data(fourth_answer=message.text)
    data = await state.get_data()
    res = cur.execute(f"SELECT id, text FROM questions "
                      f"WHERE test_id = {data['chosen_test']} AND question_number = 5").fetchone()
    question_id, question = res

    res = cur.execute(f"SELECT text FROM answers WHERE question_id={question_id}").fetchall()
    answers = [str(obj[0]) for obj in res]

    db.close()

    await SolvingTest.next()
    await message.answer(f"Вопрос 5\n\n{question}\n\n· " +
                         "\n· ".join(answers))


async def show_results(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Пожалуйста, укажите вариант ответа (1-3).")
        return
    if int(message.text) not in [1, 2, 3]:
        await message.answer("Пожалуйста, укажите вариант ответа (1-3).")
        return
    await state.update_data(fifth_answer=message.text)
    data = await state.get_data()
    my_answers = [data['first_answer'], data['second_answer'], data['third_answer'], data['fourth_answer'],
                  data['fifth_answer']]
    right_answers = list(data['right_answers'])
    k = 0
    for i in range(5):
        if my_answers[i] == right_answers[i]:
            k += 1

    await state.finish()
    if k in range(3):
        reaction = 'Не расстраивайся! Попробуй еще раз.'
    elif k in range(3, 5):
        reaction = 'Хороший результат! Ты можешь попробовать еще раз.'
    elif k == 5:
        reaction = 'Ничего себе! Попробуй тесты посложнее...'
    else:
        reaction = 'ERROR'

    await message.answer(f"<b><u>{fmt.quote_html(k)}/5</u></b> правильных ответов.\n" + reaction,
                         reply_markup=types.ReplyKeyboardRemove())


def register_handlers_solve_test(dp: Dispatcher):
    dp.register_message_handler(choose_test, commands="solve_test", state="*")
    dp.register_message_handler(first_question, state=SolvingTest.waiting_for_choose_test)
    dp.register_message_handler(second_question, state=SolvingTest.waiting_for_first_answer)
    dp.register_message_handler(third_question, state=SolvingTest.waiting_for_second_answer)
    dp.register_message_handler(fourth_question, state=SolvingTest.waiting_for_third_answer)
    dp.register_message_handler(fifth_question, state=SolvingTest.waiting_for_fourth_answer)
    dp.register_message_handler(show_results, state=SolvingTest.waiting_for_fifth_answer)
