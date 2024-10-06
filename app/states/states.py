from aiogram.fsm.state import StatesGroup, State


class InputForm(StatesGroup):
    input_fio = State()
    input_date = State()
    input_id = State()
    input_bplace = State()
    input_citizenship = State()
    input_adress = State()
    input_phone = State()
    input_email = State()
    input_fee = State()
    input_bank = State()
    input_inv = State()
    input_pdate = State()
    input_reco = State()
    input_recr = State()
    confirmation = State()


class InputPhone(StatesGroup):
    input_phone = State()


class AdmMailing(StatesGroup):
    input_message = State()
