from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import CommandStart, Command
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from app.config.logger import logger
from app.config import aiogram_bot
from app.keyboards import main_kb
from app.crud import db

router = Router()


@router.message(Command(commands='start'))
async def process_start(message: Message, state: FSMContext):
    await state.clear()
    logger.info(f'user {message.from_user.username} connected')
    uid = message.from_user.id
    username = message.from_user.username
    db.insert_user(uid, username)
    from_chat_id = -1002313093305
    await aiogram_bot.forward_message(message.chat.id, from_chat_id=from_chat_id, message_id=2, protect_content=True)
    await message.answer(text='Добро пожаловать', reply_markup=main_kb.start_btns(uid))


@router.message(Command(commands='cancel'))
async def process_cancel(message: Message, state: FSMContext):
    await state.clear()
    uid = message.from_user.id
    from_chat_id = -1002313093305
    await aiogram_bot.forward_message(message.chat.id, from_chat_id=from_chat_id, message_id=2, protect_content=True)
    await message.answer(text='Добро пожаловать', reply_markup=main_kb.start_btns(uid))


@router.message(Command(commands='about_us'))
async def p_about_us(message: Message, state: FSMContext):
    await message.answer('\nНаш сайт: https://koryosaram.org/\nYoutube канал: https://www.youtube.com/@koryosaraminkorea')
