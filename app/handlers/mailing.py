from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from app.config.logger import logger
from app.config import GoogleSheetsClient, GoogleFormsClient, aiogram_bot
from app.keyboards import main_kb
from app.states import states
from datetime import datetime
from app.filters import IsAdmin
from app.crud import db
router = Router()
router.message.filter(
    IsAdmin(F)
)


async def process_mailing(users_list, mailing_text):
    for u in users_list:
        try:
            await aiogram_bot.send_message(u[0], text=mailing_text)
        except Exception as e:
            logger.error(e)
            continue


@router.callback_query(F.data == 'adm_mailing')
async def p_mailing(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.answer('Введите текст рассылки: ')
    await state.set_state(states.AdmMailing.input_message)


@router.message(states.AdmMailing.input_message)
async def send_mail(message: Message, state: FSMContext):
    text = message.text
    await state.update_data(text=text)
    await message.answer(f'Предпросмотр: \n{text}', reply_markup=main_kb.confirm_mailig())


@router.callback_query(F.data == 'confirm_mailing')
async def p_conf_mailing(call: CallbackQuery, state: FSMContext):
    await call.answer()
    data = await state.get_data()
    text = data['text']
    await state.clear()
    users = db.get_all_users()
    await process_mailing(users, text)
    await call.message.answer('Рассылка завершена.')


@router.callback_query(F.data == 'edit_mailing')
async def p_edit_mailing(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await p_mailing()

