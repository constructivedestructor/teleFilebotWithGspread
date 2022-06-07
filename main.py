import gspread
import telebot
import datetime

gc = gspread.service_account()
bot = telebot.TeleBot('')
source = ""


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, '/help - Список команд'
                          '\n/download - Загрузить документы')


@bot.message_handler(commands=['download'])
def input_dt(message):
    dt = bot.send_message(message.from_user.id, "Введите дату в формате dd/mm/yyyy")
    bot.register_next_step_handler(dt, download_file)


def download_file(message):
    dt = message.text
    worksheet = gc.open_by_key(source).sheet1
    cell_list = worksheet.findall(dt)
    if len(cell_list) == 0:
        bot.send_message(message.from_user.id, 'Нет документов на указанную дату')
    else:
        for cell in cell_list:
            index = 'A%s' % cell.row
            val = worksheet.acell(index).value
            bot.send_document(message.from_user.id, val)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    bot.send_message(message.from_user.id, 'Для доступа к списку существующих команд введите /help')


@bot.message_handler(content_types=["document"])
def upload_file(message):
    if message.from_user.id not in []:
        bot.send_message(message.from_user.id, 'Вы не можете добавлять документы')
    else:
        doc_info = []
        worksheet = gc.open_by_key(source).sheet1

        id = message.document.file_id
        file_name = message.document.file_name
        file_dt = datetime.datetime.now().strftime('%d/%m/%Y')

        doc_info.append(id)
        doc_info.append(file_dt)
        doc_info.append(file_name)
        worksheet.append_row(doc_info)


bot.polling(none_stop=True, interval=0)
