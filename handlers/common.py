from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram import Dispatcher, types
import aiogram.utils.markdown as fmt


async def cmd_help(message: types.Message):
    await message.answer(f"Список комманд:\n\n<b>{fmt.quote_html('/add_test')}</b>  —  создать тест\n"
                         f"<b>{fmt.quote_html('/solve_test')}</b>  —  решить тест\n"
                         f"<b>{fmt.quote_html('/cancel')}</b>  —  отменить текущее действие\n")


async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Действие отменено", reply_markup=types.ReplyKeyboardRemove())


def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(cmd_help, commands="help")
    dp.register_message_handler(cmd_cancel, commands="cancel", state="*")
    dp.register_message_handler(cmd_cancel, Text(equals="отмена", ignore_case=True), state="*")


