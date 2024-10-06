from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from app.config.logger import logger
from app.config import GoogleSheetsClient, GoogleFormsClient, generate_prefilled_form_link, aiogram_bot, config_aiogram
from app.keyboards import main_kb
from app.states import states
from datetime import datetime
router = Router()

credentials_json = 'config/my-project-korean-bot-e4662088a05e.json'
sheet_name = 'Заявление для вступления в члены АКРК  (Ответы)'
base_form_url = 'https://docs.google.com/forms/d/1t8twrK8IQ7C-qdSmTcltOVSLK3cPkMU-oQahkZk9wCU/prefill'


async def get_current_time():
    return datetime.now().strftime('%d.%m.%Y %H:%M:%S')


@router.callback_query(F.data == 'continue_form')
async def p_input_form(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.answer('Ф.И.О. (как указано в айдикарте или паспорте):')
    await state.set_state(states.InputForm.input_fio)


@router.message(states.InputForm.input_fio)
async def p_input_date(message: Message, state: FSMContext):
    fio = message.text
    await state.update_data(fio=fio)
    await message.answer('Дата рождения: \n(Например 02.08.1990)')
    await state.set_state(states.InputForm.input_date)


@router.message(states.InputForm.input_date)
async def p_input_id(message: Message, state: FSMContext):
    date = message.text
    await state.update_data(bdate=date)
    await message.answer('Номер айдикарты:')
    await state.set_state(states.InputForm.input_id)


@router.message(states.InputForm.input_id)
async def p_input_bplace(message: Message, state: FSMContext):
    idcard = message.text
    await state.update_data(idcard=idcard)
    await message.answer('Место рождения:')
    await state.set_state(states.InputForm.input_bplace)


@router.message(states.InputForm.input_bplace)
async def p_input_citizen(message: Message, state: FSMContext):
    bplace = message.text
    await state.update_data(bplace=bplace)
    await message.answer('Гражданство:')
    await state.set_state(states.InputForm.input_citizenship)


@router.message(states.InputForm.input_citizenship)
async def p_input_adress(message: Message, state: FSMContext):
    citizen = message.text
    await state.update_data(citizen=citizen)
    await message.answer('Адрес проживания в Корее:')
    await state.set_state(states.InputForm.input_adress)


@router.message(states.InputForm.input_adress)
async def p_input_phone(message: Message, state: FSMContext):
    adress = message.text
    await state.update_data(adress=adress)
    await message.answer('Контактный номер телефона\n(Для дальнейшего добавления в группу в телеграмме и возможной обратной связи):')
    await state.set_state(states.InputForm.input_phone)



@router.message(states.InputForm.input_phone)
async def p_input_email(message: Message, state: FSMContext):
    phone = message.text
    await state.update_data(phone=phone)
    await message.answer('Введите ваш E-mail адрес:')
    await state.set_state(states.InputForm.input_email)


@router.message(states.InputForm.input_email)
async def p_input_inv(message: Message, state: FSMContext):

    email = message.text
    await state.update_data(email=email)
    text = '''
<b>Оплата членских взносов обязательна, для вступления в АКРК</b>
*** Оплата членских взносов даёт следующие преимущества:
- Участие в мероприятиях проводимых только для членов АКРК (образовательные, развлекательные и т.д.) 
- Возможность пользоваться скидками предоставляемыми для членов АКРК 
- Право голоса при голосовании 

Для оформления автоматического снятия (자동이체) ежемесячного членского взноса заполните обязательные поля ниже. 
    '''
    textq = 'Сумма ежемесячного членского взноса:\n(минимальная сумма 10,000 вон)'
    await message.answer(text + '\n\n' + textq, parse_mode='HTML')
    await state.set_state(states.InputForm.input_inv)


@router.message(states.InputForm.input_inv)
async def p_input_bank(message: Message, state: FSMContext):
    inv_sum = message.text
    await state.update_data(invsum=inv_sum)
    await message.answer('Наименование банка, который вы используете: '
                         '\n1. 신한은행 (Shinhan bank)'
                         '\n2. 우리은행 (Woori bank)'
                         '\n3. IBK 기업은행 (IBK)'
                         '\n4. KB 국민은행 (Kukmin bank)'
                         '\n5. KEB 하나은행 (Hana bank)'
                         '\n6. NH 농협은행 (NH bank)'
                         '\nДругое (введите свой вариант, или одну из цифр, указанных выше):')
    await state.set_state(states.InputForm.input_bank)


@router.message(states.InputForm.input_bank)
async def p_input_bnum(message: Message, state: FSMContext):
    bank = message.text.strip()
    if bank == '1' or bank == '1.':
        bank = '신한은행 (Shinhan bank)'
    elif bank == '2':
        bank = '우리은행 (Woori bank)'
    elif bank == '3':
        bank = 'IBK 기업은행 (IBK)'
    elif bank == '4':
        bank = 'KB 국민은행 (Kukmin bank)'
    elif bank == '5':
        bank = 'KEB 하나은행 (Hana bank)'
    elif bank == '6':
        bank = 'NH 농협은행 (NH bank)'
    else:
        bank = bank

    await state.update_data(bank=bank)
    await message.answer('Номер счета:')
    await state.set_state(states.InputForm.input_pdate)


@router.message(states.InputForm.input_pdate)
async def p_input_bdate(message: Message, state: FSMContext):
    bnum = message.text
    await state.update_data(bnum=bnum)
    await message.answer('Дата снятия \n(дата снятия средств каждое 5-е число месяца)\nВведите <b>Да</b>, или удобное вам число:',
                         parse_mode='HTML')
    await state.set_state(states.InputForm.input_reco)


@router.message(states.InputForm.input_reco)
async def p_input_reco(message: Message, state: FSMContext):
    pdate = message.text.strip()
    if pdate == 'Да':
        pdate = '5'
    else:
        pdate = pdate
    await state.update_data(pdate=pdate)
    await message.answer('Как вы узнали про АКРК?'
                         '\n1. От друзей или знакомых'
                         '\n2. Из соцсетей (фейсбук, телеграм, инстаграм и др.)'
                         '\n3. Самостоятельно искал(а)')
    await state.set_state(states.InputForm.input_recr)


@router.message(states.InputForm.input_recr)
async def p_input_recr(message: Message, state: FSMContext):
    reco = message.text.strip()
    if reco == '1' or reco == '1.':
        reco = 'От друзей или знакомых'
    elif reco == '2' or reco == '2.':
        reco = 'Из соцсетей (фейсбук, телеграм, инстаграм и др.)'
    elif reco == '3' or reco == '3.':
        reco = 'Самостоятельно искал(а)'
    else:
        reco = reco
    await state.update_data(reco=reco)
    await message.answer('Если вы узнали про АКРК от друзей или знакомых, напишите, пожалуйста, от кого именно вы узнали? \n(или напишите <b>Нет</b>)',
                         parse_mode='HTML')
    await state.set_state(states.InputForm.confirmation)


@router.message(states.InputForm.confirmation)
async def p_input_conf(message: Message, state: FSMContext):
    recr = message.text
    await state.update_data(recr=recr)
    await message.answer('<b>Подтверждение</b>\n(Согласие в сборе личной информации. Если не соглашаетесь с данным пунктом, с членством могут возникнуть трудности.)',
                         reply_markup=main_kb.confirm_save(), parse_mode='HTML')


@router.callback_query(F.data == 'user_confirmed')
async def p_confirmed_save(call: CallbackQuery, state: FSMContext):
    await call.answer()
    data = await state.get_data()
    form = await generate_prefilled_form_link(base_form_url, data, confirmation='Согласен')
    await call.message.answer(f'Спасибо!\nПредпросмотр заявки: {form}\nНаш сайт: https://koryosaram.org/\nYoutube канал: https://www.youtube.com/@koryosaraminkorea')
    print(data)
    await update_gsheet(data)
    await state.clear()


@router.callback_query(F.data == 'user_declined')
async def p_declined_save(call: CallbackQuery, state: FSMContext):
    await call.answer()
    data = await state.get_data()
    uname = call.from_user.username
    form = await generate_prefilled_form_link(base_form_url, data, confirmation='Не согласен')
    await call.message.answer('Спасибо! Наш менеджер свяжется с вами в ближайшее время.'
                              f'\nПредпросмотр заявки: {form}'
                              f'\nНаш сайт: https://koryosaram.org/\nYoutube канал: https://www.youtube.com/@koryosaraminkorea')
    adm_text = f'Пользователь {uname} не дал согласия на обработку данных. Номер телефона {data['phone']}'
    admin_id = config_aiogram.admin_id[0]
    await aiogram_bot.send_message(int(admin_id), text=adm_text)
    await update_gsheet(data, confirmation='Не согласен')
    await state.clear()


async def update_gsheet(data, confirmation='Согласен'):
    current_time = await get_current_time()
    sheets_client = GoogleSheetsClient(credentials_json, sheet_name)
    await sheets_client.insert_row([current_time, data['fio'], data['bdate'], data['idcard'], data['bplace'],
                                    data['adress'], data['phone'], data['email'], data['bank'], data['bnum'],
                                    data['pdate'], confirmation, data['citizen'], data['invsum'], data['reco'], data['recr']])

