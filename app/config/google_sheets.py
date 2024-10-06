import gspread
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build


class GoogleSheetsClient:
    def __init__(self, credentials_json, sheet_name):
        # Определяем область действия (scopes)
        scopes = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]

        # Создаем объект учетных данных
        credentials = Credentials.from_service_account_file(credentials_json, scopes=scopes)

        # Авторизуемся и открываем таблицу
        self.client = gspread.authorize(credentials)
        self.sheet = self.client.open(sheet_name).sheet1  # Используем первый лист

    async def insert_row(self, data):
        """
        Вставляет строку в конец таблицы.
        :param data: Список значений для вставки
        """
        self.sheet.append_row(data)

    async def get_all_records(self):
        """
        Получает все записи из таблицы.
        :return: Список словарей, где ключи - заголовки столбцов
        """
        return self.sheet.get_all_records()

    async def get_row(self, row_number):
        """
        Получает данные конкретной строки.
        :param row_number: Номер строки
        :return: Список значений в строке
        """
        return self.sheet.row_values(row_number)

    async def update_cell(self, row, col, value):
        """
        Обновляет значение конкретной ячейки.
        :param row: Номер строки
        :param col: Номер столбца
        :param value: Новое значение
        """
        self.sheet.update_cell(row, col, value)


class GoogleFormsClient:
    def __init__(self, credentials_json, form_id):
        scopes = ['https://www.googleapis.com/auth/forms.responses']
        credentials = Credentials.from_service_account_file(credentials_json, scopes=scopes)
        self.service = build('forms', 'v1', credentials=credentials)
        self.form_id = form_id

    def submit_form(self, answers):
        """
        Отправляет ответы в Google Form
        :param answers: Словарь с ответами, где ключ - идентификатор вопроса, значение - ответ
        """
        responses = []
        for question_id, answer in answers.items():
            responses.append({
                'questionId': question_id,
                'textAnswers': {
                    'answers': [{'value': answer}]
                }
            })

        # Формируем запрос для отправки ответов
        response = self.service.forms().responses().create(
            formId=self.form_id,
            body={
                'responses': responses
            }
        ).execute()

        return response


async def generate_prefilled_form_link(base_url, user_data, confirmation='Согласен'):
    """
    Генерирует ссылку на Google Form с предзаполненными полями.

    :param base_url: Базовый URL формы (полученный из Google Forms с "предварительно заполненной" ссылкой)
    :param user_data: Словарь с данными пользователя, где ключи соответствуют ID полей Google Forms
    :return: URL с предзаполненными значениями
    """
    # ID полей формы (entry.XXXXX) из Google Forms
    form_fields = {
        "fio": "entry.1395899189",
        "bdate": ("entry.1770352209_day", "entry.1770352209_month", "entry.1770352209_year"),
        "idcard": "entry.1838515511",
        "bplace": "entry.694891599",
        "citizen": "entry.47115566",
        "adress": "entry.86705958",
        "phone": "entry.1588341600",
        "email": "entry.441065953",
        "invsum": "entry.16217411",
        "bank": "entry.1518281458",
        "bnum": "entry.1842224689",
        "pdate": "entry.1999646169",
        "confirmation": "entry.228588528",
        "reco": "entry.1902255116",
        "recr": 'entry.1823854050'
    }

    # Генерируем предзаполненный URL
    prefilled_url = base_url + "?"

    # Обработка данных
    for field, value in user_data.items():
        if field == "bdate":
            # Разбиваем дату на день, месяц и год
            day, month, year = value.split(".")
            # Обратите внимание, что Google Forms может ожидать месяц как 1-12, а не 01-12
            prefilled_url += f"{form_fields['bdate'][0]}={day}&{form_fields['bdate'][1]}={month}&{form_fields['bdate'][2]}={year}&"
        elif field == "bank":
            bank_name = value.replace(" ", "%20")
            prefilled_url += f"{form_fields['bank']}={bank_name}&"
        elif field == "pdate":
            if value.lower() == 'да':
                prefilled_url += f"{form_fields['pdate']}=5&"
            else:
                prefilled_url += f"{form_fields['pdate']}={value}&"

        elif field == "reco":
            if value == 'От друзей или знакомых':
                value = 'От%20друзей%20или%20знакомых'
            elif value == 'Из соцсетей (фейсбук, телеграм, инстаграм и др.)':
                value = 'Из%20соцсетей%20(фейсбук,%20телеграм,%20инстаграм%20и%20др.)'
            elif value == 'Самостоятельно искал(а)':
                value = 'Самостоятельно%20искал(а)'
            else:
                value = value
            prefilled_url += f"{form_fields['reco']}={value}&"

        elif field == 'recr':
            recr_name = value.replace(" ", "%20")
            prefilled_url += f"{form_fields['recr']}={recr_name}&"
        else:
            # Обычные текстовые поля
            if field in form_fields:
                value = value.replace(" ", "%20")
                prefilled_url += f"{form_fields[field]}={value}&"

    # Обработка confirmation после цикла
    prefilled_url += f"{form_fields['confirmation']}={confirmation.replace(' ', '%20')}&"

    # Удаляем последний лишний символ '&'
    prefilled_url = prefilled_url.rstrip('&')

    return prefilled_url



