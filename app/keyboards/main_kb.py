from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.config import config_aiogram


def start_btns(uid):
    admin_id = config_aiogram.admin_id
    kb_builder = InlineKeyboardBuilder()
    print(uid, admin_id, type(uid), type(admin_id))
    if str(uid) in admin_id:
        kb_builder.button(text='Продолжить', callback_data='continue_form')
        kb_builder.button(text='Рассылка', callback_data='adm_mailing')
    else:
        kb_builder.button(text='Продолжить', callback_data='continue_form')
    kb_builder.adjust(2)
    return kb_builder.as_markup(resize_keyboard=True)


def confirm_form():
    kb_builder = InlineKeyboardBuilder()
    kb_builder.button(text='Продолжить', callback_data='confirm_form')
    kb_builder.button(text='Изменить данные', callback_data='continue_form')
    kb_builder.adjust(2)
    return kb_builder.as_markup(resize_keyboard=True)


def confirm_save():
    kb_builder = InlineKeyboardBuilder()
    kb_builder.button(text='Да', callback_data='user_confirmed')
    kb_builder.button(text='Нет', callback_data='user_declined')
    kb_builder.adjust(2)
    return kb_builder.as_markup(resize_keyboard=True)


def confirm_mailig():
    kb_builder = InlineKeyboardBuilder()
    kb_builder.button(text='Отправить', callback_data='confirm_mailing')
    kb_builder.button(text='Изменить', callback_data='edit_mailing')
    kb_builder.adjust(2)
    return kb_builder.as_markup(resize_keyboard=True)
