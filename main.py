import config as cfg
import markup as nav
import classes as cl
import classes_mark as cl_m
from imports import *



logging.basicConfig(level=logging.INFO)
config = configparser.ConfigParser()
config.read("settings.ini")
bot = Bot(token=config["Initialization"]["token"])
dp = Dispatcher(storage=MemoryStorage())


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    link = InlineKeyboardBuilder()
    link.add(types.InlineKeyboardButton(
        text="Наш канал 📺",
        url="https://t.me/")
    )
    link.add(types.InlineKeyboardButton(
        text="Наш чат 💬",
        url="https://t.me/")
    )

    await message.answer(f'Мультивалютный криптокошелёк. Покупайте, продавайте, храните, отправляйте и платите криптовалютой, когда хотите.',
        reply_markup = nav.main_menu)
    await bot.send_message(message.chat.id,'Подписывайтесь на наш канал и вступайте в наш чат!',
        reply_markup=link.as_markup())
    await check_user_login(message.from_user.username, message.from_user.id)


@dp.message(Command("admin"))
async def cmd_reset_verifi(message: types.Message, state: FSMContext):
    request = await read_db(f'users WHERE login="{message.from_user.username}"', 'access')
    if int(request[0][0]) == 1:
        await message.answer(f'Введите пароль')
        await state.set_state(cl.Adm.status)

@dp.message(cl.Adm.status)
async def verification_valid(message: types.Message, state: FSMContext):
    request = await read_db(f'users WHERE login="{message.from_user.username}"', 'adm_pass')
    if request and request[0][0] == message.text:
        await state.update_data(status=1)
        await bot.send_message(message.from_user.id,'Панель администратора.', reply_markup=nav.inline_adm_main_menu)
    else:
        await message.add_answer(f'Ошибка, неверный пароль.')


@dp.message(Command("reset_verifi"))
async def cmd_reset_verifi(message: types.Message, state: FSMContext):
    request = await read_db(f'users WHERE login="{message.from_user.username}"', 'name')
    if request[0][0] == None or not request[0][0]:
        await message.answer(f'Пройдите верификацию по кнопке в главном меню')
    else:
        await message.answer(f'Внимание!\n'
                             f'Отправляя данные вы подтверждаете ваши личные данные и при оплате в чеке будут указанны ваши указанные данные, '
                             f'в случае несоответсвия продавец имеет право откланить выплату.\n Введите ваше имя, фамилию и отчество')
        await state.set_state(cl.Verifi.name)


@dp.message(cl.Verifi.name)
async def verification_valid(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    date = await state.get_data()
    request_date = date['name']
    await bot.send_message(message.chat.id, f'Верификация пройдена! Ваше ФИО - {date['name']}'
                                            f'\n\nСовершите более 3 сделок и ваша верификация станет подтвержденной ✅',reply_markup=nav.main_menu)
    await write_db(f"UPDATE users SET name='{request_date}' WHERE login='{message.from_user.username}'")
    await state.clear()


@dp.message(cl.Addwallets.number)
async def add_wallets(message: types.Message, state: FSMContext):
    await state.update_data(number=message.text)
    request = await read_db(f'users_purses WHERE login="{message.from_user.username}"', 'saved_wallets_1, saved_wallets_2, saved_wallets_3')
    date = await state.get_data()
    request_date = date['number']
    if request[0][0] is None or not request[0][0]:
        await write_db(f"UPDATE users_purses SET saved_wallets_1='{request_date}' WHERE login='{message.from_user.username}'")
        await bot.send_message(message.chat.id, f'Кошелек {request_date} добавлен!',reply_markup=nav.bot_address_book_menu)
    elif request[0][1] is None or not request[0][1]:
        await write_db(f"UPDATE users_purses SET saved_wallets_2='{request_date}' WHERE login='{message.from_user.username}'")
        await bot.send_message(message.chat.id, f'Кошелек {request_date} добавлен!',reply_markup=nav.bot_address_book_menu)
    elif request[0][2] is None or not request[0][2]:
        await write_db(f"UPDATE users_purses SET saved_wallets_3='{request_date}' WHERE login='{message.from_user.username}'")
        await bot.send_message(message.chat.id, f'Кошелек {request_date} добавлен!',reply_markup=nav.bot_address_book_menu)
    else:
        await bot.send_message(message.chat.id, f'У вас нет свободных мест в адресной книге, удалите не нужные адреса.',reply_markup=nav.bot_address_book_menu)
    await state.clear()


@dp.message(cl.Deletewallets.number)
async def deletewallet(message: types.Message, state: FSMContext):
    request = await read_db(f'users_purses WHERE login="{message.from_user.username}"',
                            'saved_wallets_1, saved_wallets_2, saved_wallets_3')
    try:
        index = int(message.text)
        if request[0][index-1] == '' or None or not request[0][index-1]:
            await bot.send_message(message.chat.id, f'Выбраный вами слот для счета пуст.',reply_markup=nav.bot_address_book_menu)
        elif message.text == '1' or message.text == '2' or message.text == '3':
            await write_db(f"UPDATE users_purses SET saved_wallets_{index}='' WHERE login='{message.from_user.username}'")
            await bot.send_message(message.chat.id, f'Кошелек {request[0][index-1]} успешно удален из адресной книги',reply_markup=nav.bot_address_book_menu)
    except:
        await bot.send_message(message.chat.id, f'Внимание! Нужно вводить цифры от 1 до 3.\nНажмите "удалить номер кошелька" и попробуйте еще раз',reply_markup=nav.bot_address_book_menu)
    await state.clear()


@dp.message(cl.Withdraw.number)
async def withdraw_handler(message: types.Message, state: FSMContext):
    request = await read_db(f'users_purses WHERE login="{message.from_user.username}"',
                            'saved_wallets_1, saved_wallets_2, saved_wallets_3')
    try:
        if message.text == '1' or message.text == '2' or message.text == '3':
            index = int(message.text)
            await bot.send_message(message.chat.id, f'Вывод средств на кошелек {request[0][index-1]}',
                                   reply_markup=nav.bot_address_book_menu)
            await state.update_data(number=message.text)
            await state.set_state(cl.Withdraw.check)
        else:
            await bot.send_message(message.chat.id,f'Вывод средств на кошелек {message.text}.',reply_markup=nav.wallet_menu)
            await state.update_data(number=message.text)
            await state.set_state(cl.Withdraw.check)
    except:
        await bot.send_message(message.chat.id,f'Обнаружена кириллица, используйте номер кошелька без нее.'
                                               f'\nНажмите кнопку "Вывести" и попробуйте еще раз.',reply_markup=nav.wallet_menu)
        await state.clear()


@dp.message(cl.Withdraw.check)
async def withdraw(message: Message, state: FSMContext):
    if message.text == 'Да':
        await bot.send_message(message.chat.id, f'Вывод средств на кошелек {message.text} подтвержден.',
                               reply_markup=nav.wallet_menu)
        await state.clear()
    elif message.text == 'Нет':
        await bot.send_message(message.chat.id, f'Вывод средств на кошелек {message.text} отменен.',
                               reply_markup=nav.wallet_menu)
        await state.clear()
    else:
        await bot.send_message(message.chat.id, f'Вывод средств на кошелек {message.text} отменен.',
                               reply_markup=nav.wallet_menu)
    await state.clear()


@dp.message(cl.Buycrypt.amount)
async def buycrypt_count(message: Message, state: FSMContext):
    try:
        data = await state.get_data()
        respt_count = ((message.text).replace(',', '.'))
        count = float(respt_count)
        request_main = await read_db(f'users WHERE login="{message.from_user.username}"', 'currency')
        await state.update_data(type_user=cfg.coins_index[request_main[0][0]])
        data = await state.get_data()
        request = await read_db(f'users_purses WHERE login="{message.from_user.username}"', f'{data["type_user"]}, {data['type']}')
        request_rate = await read_db(f'exchange_rates WHERE currency_1="{data['type']}" && currency_2="{cfg.coins_index[request_main[0][0]]}"','rate, minimum_exchange_amount')
        count_balance = float(request[0][0])
        amount = float(count * float(request_rate[0][0]))
        if count % 1 == 0:
            count = int(respt_count)
        await state.update_data(type_user_hard=request_main[0][0])
        await state.update_data(course=request_rate[0][0])
        await state.update_data(min=request_rate[0][1])
        await state.update_data(count=count)
        await state.update_data(amount=amount)
        await state.update_data(balance=count_balance)
        await state.update_data(balance_crypt=request[0][1])
        data = await state.get_data()
        if count >= data['min']:
            if float(count_balance) >= float(data['amount']):
                await bot.send_message(message.chat.id, f'🪐 Подтверждение\n\nПокупка {data['type']} за {data['type_user']} по рыночной цене.\n\nСредная цена: {data['course']} {data['type_user']}\n\n Количество: {data['count']} {data['type']}\n Сумма: {data['amount']} {data['type_user']}', reply_markup=nav.inlnine_exchange_menu_create_application)
            else:
                await bot.send_message(message.chat.id,f'{'-' * 70}\n⚠️Недостаточно средств. Поплните баланс.\n{'-' * 70}\n\nВыберите валюту, которую вы хотите купить:',reply_markup=nav.builder.as_markup())
        else:
            await bot.send_message(message.chat.id,f'{'-' * 70}\n⚠️Минимальная сумма обмена {data['min']} {data['type']}\n{'-' * 70}\n\n Выберите валюту, которую вы хотите купить:',
                                   reply_markup=nav.builder.as_markup())
    except ValueError:
        pass


@dp.message(cl.Sellcrypt.amount)
async def sell_crypt_count(message: Message, state: FSMContext):
    try:
        data = await state.get_data()
        respt_count = ((message.text).replace(',', '.'))
        count = float(respt_count)
        request_main = await read_db(f'users WHERE login="{message.from_user.username}"', 'currency')
        await state.update_data(type_user=cfg.coins_index[request_main[0][0]])
        data = await state.get_data()
        request = await read_db(f'users_purses WHERE login="{message.from_user.username}"', f'{data["type_user"]}, {data['type']}')
        request_rate = await read_db(f'exchange_rates WHERE currency_2="{cfg.coins_index[request_main[0][0]]}" && currency_1="{data['type']}"','rate, minimum_exchange_amount')
        count_balance = float(request[0][1])
        if count % 1 == 0:
            count = int(respt_count)
        await state.update_data(type_user_hard=request_main[0][0])
        await state.update_data(course=request_rate[0][0])
        await state.update_data(min=request_rate[0][1])
        await state.update_data(count=count)
        await state.update_data(amount=count * float(request_rate[0][0]))
        await state.update_data(balance=count_balance)
        await state.update_data(balance_crypt=request[0][1])
        data = await state.get_data()
        if count >= data['min']:
            if count_balance >= data['count']:
                await bot.send_message(message.chat.id, f'🪐 Подтверждение\n\nПродажа {data['type']} за {data['type_user']} по рыночной цене.\n\nСредная цена: {data['course']} {data['type_user']}\n\nКоличество: {data['count']} {data['type']}\nСумма: {data['amount']} {data['type_user']}', reply_markup=nav.inlnine_exchange_menu_create_application_sell)
            else:
                await bot.send_message(message.chat.id,f'{'-' * 70}\n⚠️Недостаточно {data['type']} для продажи.\n{'-' * 70}\n\nВыберите валюту, которую вы хотите продать:',reply_markup=nav.builder_sell.as_markup())
        else:
            await bot.send_message(message.chat.id,f'{'-' * 70}\n⚠️Минимальное количество для продажи {data['min']} {data['type_user']}\n{'-' * 70}\n\n Выберите валюту, которую вы хотите продать:',
                                   reply_markup=nav.builder.as_markup())
    except ValueError:
        pass


@dp.message(cl.Sellcrypt.count)
async def trade_crypt(message: types.Message, state: FSMContext):
    try:
        data = await state.get_data()
        respt_count = ((message.text).replace(',', '.'))
        count = float(respt_count)
        if count % 1 == 0:
            count = int(respt_count)
        data = await state.get_data()
        request = await read_db(f'users_purses WHERE login="{message.from_user.username}"',
                                f'{data["type"]}, {data['type_user']}')
        count_balance = float(request[0][0])
        count_balance_crypt = float(request[0][1])
        await state.update_data(count=count)
        await state.update_data(amount=count * float(data['course']))
        await state.update_data(balance=count_balance)
        await state.update_data(balance_crypt=count_balance_crypt)
        data = await state.get_data()
        if count >= data['min']:
            if count_balance >= data['count']:
                await bot.send_message(message.chat.id,
                                       f'🪐 Подтверждение\n\nОбмен {data['type']} на {data['type_user']} по рыночной цене.'
                                       f'\n\nСредная цена: {data['course']} {data['type_user']}\n\n Количество: {data['count']} {data['type']}'
                                       f'\n Сумма: {(data['amount'])} {data['type_user']}',reply_markup=nav.inlnine_exchange_menu_create_application_trade)
            else:
                await bot.send_message(message.chat.id,
                                       f'{'-' * 70}\n⚠️Недостаточно {data['type']} для обмена.\n{'-' * 70}\n\nВыберите валюту, которую вы хотите обменять:',
                                       reply_markup=nav.builder_sell.as_markup())
        else:
            await bot.send_message(message.chat.id,
                                   f'{'-' * 70}\n⚠️Минимальная сумма обмена {data['min']} {data['type']}\n{'-' * 70}\n\nВыберите валюту, которую вы хотите обменять:',
                                   reply_markup=nav.builder.as_markup())
    except ValueError:
        pass


@dp.callback_query(F.data == 'create_application_buy')
async def exchange_create_application(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    d = datetime.now()
    number = random.randint(10000, 9999999)
    request = await read_db(f'users_purses WHERE login="{callback.from_user.username}"',
                            f'{data["type_user"]}, {data['type']}')
    count_type = float(request[0][1]) - float(data['count'])
    count_type_user = float(request[0][0]) + float(data['amount'])
    await callback.message.edit_text(
        text=f'🛍️ Рыночная заявка #{number}\n\nПокупка {data['type']} за {data['type_user']} по рыночной цене.\n\nСредняя цена: {data['course']} {data['type_user']}\n\nКоличество: {data['count']} {data['type']}\nСумма: {data['amount']} {data['type_user']}\n\nПолучено: {data['count']} {data['type']} из 1 сделки.\n\n✅ Заявка была исполнена {d.strftime("%d-%m-%Y, %H.%M.%S (UTC)")}.')
    await write_db(f"INSERT INTO exchange_logs (login, currency_1, currency_2, count, type, number) VALUES ('{callback.from_user.username}', '{data['type_user']}', '{data['type']}', {data['count']}, 'purchase', {number})")
    await write_db(f"UPDATE users_purses SET {data['type_user']}={data['balance']-data['amount']}, {data['type']}={data['type']}+{data['count']} WHERE login='{callback.from_user.username}'")
    await callback.message.answer(
        f"{'-' * 100}\n👌 Заявка #{number} на покупку {data['count']} {data['type']} за {data['type_user']} исполнена.\n{'-' * 100}",
        reply_markup=nav.inlnine_exchange_menu_back_2)
    await state.clear()

@dp.callback_query(F.data == 'create_application_trade')
async def exchange_create_application(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    d = datetime.now()
    number = random.randint(10000,9999999)
    await callback.message.edit_text(
        text=f'🛍️ Рыночная заявка #{number}\n\nОбмен {data['type']} на {data['type_user']} по рыночной цене.\n\nСредняя цена: {data['course']} {data['type_user']}\n\nКоличество: {data['count']} {data['type']}\nСумма: {data['amount']} {data['type_user']}\n\nПолучено: {data['amount']} {data['type_user']} из 1 сделки.\n\n✅ Заявка была исполнена {d.strftime("%d-%m-%Y, %H.%M.%S")}.')
    await write_db(f"INSERT INTO exchange_logs (login, currency_1, currency_2, count, type, number) VALUES ('{callback.from_user.username}', '{data['type']}', '{data['type_user']}', {data['count']}, 'trade', {number})")
    await write_db(f"UPDATE users_purses SET {data['type_user']}={data['balance_crypt']+data['amount']}, {data['type']}={data['balance']}-{data['count']} WHERE login='{callback.from_user.username}'")
    await callback.message.answer(f"{'-' * 100}\n👌 Заявка #{number} на обмен {(data['amount'])} {data['type_user']} за {data['type']} исполнена.\n{'-' * 100}", reply_markup=nav.inlnine_exchange_menu_back_2)
    await state.clear()


@dp.callback_query(F.data == 'adm_back')
async def exchange_create_application(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(f'Панель администратора.', reply_markup=nav.inline_adm_main_menu)


@dp.callback_query(F.data == 'course')
async def exchange_create_application(callback: CallbackQuery, state: FSMContext):
    request = await read_db(f'exchange_rates', '*')
    course = ''
    count = 1
    for i in request:
        course += str(count) + '. ' '1' + str(i[1]) + ' = ' + str(i[3]) + str(i[2]) +'\n'
        count+=1
    await callback.message.answer(f'На данный момент установленны следующие курсы:\n{course}',
                                  reply_markup=nav.inline_p2p_course_menu)


@dp.callback_query(F.data == 'change_couse')
async def exchange_create_application(callback: CallbackQuery, state: FSMContext):
    await state.set_state(cl.Adm.count_course)
    await callback.message.answer(f'Что бы изменить курс введите название валюты или криптовалюты, поставьте дефис, '
                                  f'введите название второй валюты или криптовалюты и через пробел введите курс'
                                  f'\n\nНапример, введя такой запрос: BTC-RUB 5646953 вы установить курс 1BTC = 5646953RUB',
                                  reply_markup=nav.inline_change_couse_menu)


@dp.callback_query(F.data == 'p2p_tickets_delete')
async def exchange_create_application(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await write_db(f"DELETE FROM support_tickets WHERE number_tik={data['id']}")
    await callback.message.answer(f'Вы удалили обращение #D{data['id']}',
                                  reply_markup=nav.inline_p2p_tickets_back_menu)


@dp.message(cl.Adm.count_course)
async def percentage_edit(message: types.Message, state: FSMContext):
    try:
        course_1 = message.text.split('-')[0]
        course_2 = message.text.split('-')[1]
        course_count = course_2.split(' ', 1)[1]
        course_2 = course_2.split(' ', 1)[0]
        try:
            await write_db(f"UPDATE exchange_rates SET rate={course_count} WHERE currency_1='{course_1}' && currency_2='{course_2}'")
        except:
            await write_db(f"INSERT INTO exchange_logs (currency_1, currency_2, rate) VALUES ('{course_1}', '{course_2}', {course_count})")
        await bot.send_message(message.chat.id,f'Успешно установлен курс 1{course_1} = {course_count} {course_2}', reply_markup=nav.inline_change_couse_2_menu)
    except:
        await bot.send_message(message.chat.id,
            f'Что-то пошло не так.\n\nЧто бы изменить курс введите название валюты или криптовалюты, поставьте дефис, '
            f'введите название второй валюты или криптовалюты и через пробел введите курс'
            f'\n\nНапример, введя такой запрос: BTC-RUB 5646953 вы установить курс 1BTC = 5646953RUB',
            reply_markup=nav.inline_change_couse_menu)


@dp.callback_query(F.data == 'p2p_tickets')
async def exchange_create_application(callback: CallbackQuery, state: FSMContext):
    request = await read_db(f'support_tickets')
    count, mass = 0, []
    text = 'Активные обращения в поддержку:'
    for i in request:
        mass.append(InlineKeyboardButton(
            text=f'Обращение номер {request[count][6]} по объявлению #{request[count][1]}',
            callback_data=cl_m.Advertisements(action='select_ticket',number=f'{request[count][6]}').pack())),
        count += 1
    if not mass:
        text = 'Нет обращений в поддержку'
    builder = InlineKeyboardBuilder()
    for button in mass:
        builder.row(button)
    builder.row(
        InlineKeyboardButton(text='Назад', callback_data='adm_back'),
        width=1
    )
    builder.as_markup()
    await callback.message.answer(f'{text}',reply_markup=builder.as_markup())


@dp.callback_query(F.data == 'balance_bot')
async def exchange_create_application(callback: CallbackQuery, state: FSMContext):
    request = await read_db(f'users_purses',f'SUM(USDT), SUM(TON), SUM(GRAM), SUM(BTC), SUM(LTC), SUM(ETH), SUM(BNB), SUM(TRX), SUM(USDC), SUM(NOT_C)')
    request_2 = await read_db(f'freezing_of_funds', 'SUM(USDT), SUM(TON), SUM(GRAM), SUM(BTC), SUM(LTC), SUM(ETH), SUM(BNB), SUM(TRX), SUM(USDC), SUM(NOT_C)')
    curr, count, curr_freeze = '', 1, ''
    for j in request[0]:
        curr += str(count) + '. ' + str(cfg.coins_2[count-1] + ': '+ str(j) + ' ' + str(cfg.coins_index[count-1])) + '\n'
        count += 1
    count = 1
    for i in request_2[0]:
        if i == None:
            i = 0
        curr_freeze += str(count) + '. ' + str(cfg.coins_2[count-1]) + ': '+ str(i) + ' ' + str(cfg.coins_index[count-1]) + '\n'
        count += 1
    await callback.message.answer(f'Общий баланс площадки:\n{curr}\nБаланс находящийся в стадии активной сделки:\n{curr_freeze}', reply_markup=nav.inline_adm_balance_menu)


@dp.callback_query(F.data == 'balance_bot')
async def exchange_create_application(callback: CallbackQuery, state: FSMContext):
    request = await read_db(f'users_purses',f'SUM(USDT), SUM(TON), SUM(GRAM), SUM(BTC), SUM(LTC), SUM(ETH), SUM(BNB), SUM(TRX), SUM(USDC), SUM(NOT_C)')
    request_2 = await read_db(f'freezing_of_funds', 'SUM(USDT), SUM(TON), SUM(GRAM), SUM(BTC), SUM(LTC), SUM(ETH), SUM(BNB), SUM(TRX), SUM(USDC), SUM(NOT_C)')
    curr, count, curr_freeze = '', 1, ''
    for j in request[0]:
        curr += str(count) + '. ' + str(cfg.coins_2[count-1] + ': '+ str(j) + ' ' + str(cfg.coins_index[count-1])) + '\n'
        count += 1
    count = 1
    for i in request_2[0]:
        curr_freeze += str(count) + '. ' + str(cfg.coins_2[count-1]) + ': '+ str(i) + ' ' + str(cfg.coins_index[count-1]) + '\n'
        count += 1
    await callback.message.answer(f'Общий баланс площадки:\n{curr}\nБаланс находящийся в стадии активной сделки:\n{curr_freeze}', reply_markup=nav.inline_adm_balance_menu)



@dp.callback_query(F.data == 'create_application_sell')
async def exchange_create_application(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    d = datetime.now()
    number = random.randint(10000, 9999999)
    request = await read_db(f'users_purses WHERE login="{callback.from_user.username}"',
                            f'{data["type_user"]}, {data['type']}')
    count_type = float(request[0][1]) - float(data['count'])
    count_type_user = float(request[0][0]) + float(data['amount'])
    await callback.message.edit_text(
        text=f'🛍️ Рыночная заявка #{number}\n\nПродажа {data['type']} за {data['type_user']} по рыночной цене.\n\nСредняя цена: {data['course']} {data['type_user']}\n\nКоличество: {data['count']} {data['type']}\nСумма: {data['amount']} {data['type_user']}\n\nПолучено: {data['amount']} {data['type_user']} из 1 сделки.\n\n✅ Заявка была исполнена {d.strftime("%d-%m-%Y, %H.%M.%S")}.')
    await write_db(f"INSERT INTO exchange_logs (login, currency_2, currency_1, count, type, number) VALUES ('{callback.from_user.username}', '{data['type_user']}', '{data['type']}', {data['count']}, 'sell', {number})")
    await write_db(f"UPDATE users_purses SET {data['type_user']}={count_type_user}, {data['type']}={count_type} WHERE login='{callback.from_user.username}'")
    await callback.message.answer(
        f"{'-' * 100}\n👌 Заявка #{number} на продажу {data['count']} {data['type']} за {data['type_user']} исполнена.\n{'-' * 100}",
        reply_markup=nav.inlnine_exchange_menu_back_2)
    await state.clear()

@dp.callback_query(F.data == 'total_balance_currency')
async def back_exchange_buy_crypt(callback: CallbackQuery, state: FSMContext):
    request = await read_db(f'users WHERE login="{callback.from_user.username}"', 'currency')
    await callback.message.edit_text(
        text=f'Выберите валюту общего баланса.\n\n{'-' * 50}\nСейчас выбрана:{cfg.coins[request[0][0]]}\n{'-' * 50}\n', reply_markup=nav.builder_balance_currency.as_markup())


@dp.callback_query(F.data == 'back_exchange_buy_crypt')
async def back_exchange_buy_crypt(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text=f'Выберите валюту, которую вы хотите купить:', reply_markup=nav.builder.as_markup())
    await state.set_state(cl.Buycrypt.type)


@dp.callback_query(F.data == 'back_exchange_sell_crypt')
async def back_exchange_buy_crypt(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text=f'Выберите валюту, которую вы хотите продать:', reply_markup=nav.builder_sell.as_markup())
    await state.set_state(cl.Buycrypt.type)


@dp.callback_query(F.data == 'back_exchange')
async def back_exchange(callback: CallbackQuery, state: FSMContext):
    request = await read_db(f'users_purses WHERE login="{callback.from_user.username}"', '*')
    request_2 = await read_db(f'users WHERE login="{callback.from_user.username}"', 'currency')
    await callback.message.answer(f' 🐬 Здесь вы можете торговать криптовалютой как на обычной бирже.\n'
                                     f'⚡️ Все заявки на обмен выполняются автоматически.\n{'-' * 40}\nID пользователя: '
                                     f'{callback.from_user.username}\nОбщий баланс {cfg.coins_2[request_2[0][0]]}: {request[0][request_2[0][0]+2]} {cfg.coins_index[request_2[0][0]]} \n{'-' * 40}\n '
                                     f'{cfg.coins_2[0]}: {request[0][2]} {cfg.coins_index[0]} \n{cfg.coins_2[1]}: {request[0][3]} {cfg.coins_index[1]} \n{cfg.coins_2[2]}: {request[0][4]} {cfg.coins_index[2]} \n{cfg.coins_2[3]}: {request[0][5]} {cfg.coins_index[3]} '
                                     f'\n{cfg.coins_2[4]}: {request[0][6]} {cfg.coins_index[4]} \n{cfg.coins_2[5]}: {request[0][7]} {cfg.coins_index[5]} \n '
                                     f'{cfg.coins_2[6]}: {request[0][8]} {cfg.coins_index[6]} \n {cfg.coins_2[7]}: {request[0][9]} {cfg.coins_index[7]} \n '
                                     f'{cfg.coins_2[8]}: {request[0][10]} {cfg.coins_index[8]}\n{cfg.coins_2[9]}: {request[0][10]} {cfg.coins_index[9]}',reply_markup=nav.inlnine_exchange_menu_show_zero)


@dp.callback_query(cl_m.Balance_currency.filter())
async def buy_crypt_exchange(callback: CallbackQuery, callback_data: cl_m.Balance_currency, state: FSMContext):
    if callback_data.action == 'select_balance_currency':
        type = int(callback_data.value)
        await write_db(f"UPDATE users SET currency={type} WHERE login='{callback.from_user.username}'")
        request_2 = await read_db(f'users WHERE login="{callback.from_user.username}"', 'currency')
        await callback.message.edit_text(text=f'Валюта общего баланса успешно изменена.\n\n{'-' * 50}\nСейчас выбрана: {cfg.coins[request_2[0][0]]}\n{'-' * 50}\n',reply_markup=nav.builder_balance_currency.as_markup())
    elif callback_data.action == 'back_exchange':
        request = await read_db(f'users_purses WHERE login="{callback.from_user.username}"', '*')
        request_2 = await read_db(f'users WHERE login="{callback.from_user.username}"', 'currency')
        await callback.message.edit_text(f' 🐬 Здесь вы можете торговать криптовалютой как на обычной бирже.\n'
                                         f'⚡️ Все заявки на обмен выполняются автоматически.\n{'-' * 40}\nID пользователя: '
                                         f'{callback.from_user.username}\nОбщий баланс в {cfg.coins_2[request_2[0][0]]}: {request[0][request_2[0][0]+2]} {cfg.coins_index[request_2[0][0]]} \n{'-' * 40}\n '
                                         f'🔹Tether: {request[0][2]} USDT \n🔹Toncoin: {request[0][3]} TON \n🔹Gram: {request[0][4]} GRAM \n '
                                         f'🔹Bitcoin: {request[0][5]} BTC '
                                         f'\n🔹Litecoin: {request[0][6]} LTC \n🔹Ethereum: {request[0][7]} ETH \n '
                                         f'🔹Binance Coin: {request[0][8]} BNB \n🔹TRON: {request[0][9]} TRX \n '
                                         f'🔹USD Coin: {request[0][10]} USDC',
                                         reply_markup=nav.inlnine_exchange_menu_hide_zero)


@dp.callback_query(F.data == 'p2p_buy')
async def p2p_buy(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(f'Выберите криптовалюту, которую вы хотите купить.', reply_markup=nav.builder_crypt_p2p.as_markup())
    await state.set_state(cl.Buy_p2p.type)
    await state.update_data(type=1)
    await state.set_state(cl.Buyp2p.crypto)


@dp.callback_query(F.data == 'p2p_sell')
async def p2p_buy(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(f'Выберите криптовалюту, которую вы хотите продать.', reply_markup=nav.builder_crypt_p2p.as_markup())
    await state.set_state(cl.Buy_p2p.type)
    await state.update_data(type=0)
    await state.set_state(cl.Buyp2p.crypto)


@dp.callback_query(F.data == 'p2p_buy_fix_edit')
async def p2p_buy_fix_edit(callback: CallbackQuery, state: FSMContext):
    data = await state.update_data()
    word = 'покупки'
    if data['type'] == 0:
        word = 'продажи'
    request = await read_db(f'p2p_advertisements WHERE number="{data['number']}"', '*')
    request_rate = await read_db(
        f'exchange_rates WHERE currency_1="{cfg.coins_index[int(request[0][6])]}" && currency_2="{cfg.bot_currency_2[int(request[0][3])]}"',
        'rate')
    if request[0][15] == 1:
        with suppress(TelegramBadRequest):
            await callback.message.edit_text(f'Отправьте фиксированную цену в {cfg.bot_currency_2[int(request[0][3])]} для {word} {cfg.coins_index[int(request[0][6])]}.\n\nБиржевой курс: {request_rate[0][0]} {cfg.bot_currency_2[int(request[0][3])]}\n\nЦена за 1 {cfg.coins_index[int(request[0][6])]} = {request_rate[0][0]} {cfg.bot_currency_2[int(request[0][3])]}\n\n{'-' * 60}\n⚠️ В цене объявления должны быть учтены все возможные комиссии платёжных систем. Правилами сервиса запрещено взимать дополнительные комиссии с пользователей - покупатели должны переводить точную сумму сделки.\n{'-' * 60}',
                                             reply_markup=nav.inline_p2p_fix_menu_edit)
    elif request[0][15] == 0:
        with suppress(TelegramBadRequest):
            await callback.message.edit_text(f'Отправьте фиксированную цену в {cfg.bot_currency_2[int(request[0][3])]} для {word} {cfg.coins_index[int(request[0][6])]}.\n\nБиржевой курс: {request_rate[0][0]} {cfg.bot_currency_2[int(request[0][3])]}\n\nЦена за 1 {cfg.coins_index[int(request[0][6])]} = {request_rate[0][0]} {cfg.bot_currency_2[int(request[0][3])]}\n\n{'-' * 60}\n⚠️ В цене объявления должны быть учтены все возможные комиссии платёжных систем. Правилами сервиса запрещено взимать дополнительные комиссии с пользователей - покупатели должны переводить точную сумму сделки.\n{'-' * 60}',
                                             reply_markup=nav.inline_p2p_fix_menu_edit)
    await state.set_state(cl.Announcement.fix_count_sell)

@dp.callback_query(F.data == 'p2p_bank_floating_edit')
async def p2p_bank_floating_edit(callback: CallbackQuery, state: FSMContext):
    data = await state.update_data()
    word = 'покупки'
    if data['type'] == 0:
        word = 'продажи'
    request = await read_db(f'p2p_advertisements WHERE number="{int(data['number'])}"', '*')
    request_rate = await read_db(
        f'exchange_rates WHERE currency_1="{cfg.coins_index[int(request[0][6])]}" && currency_2="{cfg.bot_currency_2[int(request[0][3])]}"',
        'rate')
    if int(request[0][15]) == 1:
        with suppress(TelegramBadRequest):
            await callback.message.edit_text(f'Отправьте процент от биржевого курса для {word} {cfg.coins_index[int(request[0][6])]}.\n(например, +4% или -2.5%)\n\nБиржевой курс: {float(request_rate[0][0])} {cfg.bot_currency_2[int(request[0][3])]}\n\nЦена за 1 {cfg.coins_index[int(request[0][6])]} = {float(request_rate[0][0])} {cfg.bot_currency_2[int(request[0][3])]}\n\n{'-'*60}\n⚠️ В курсе объявления должны быть учтены все возможные комиссии платёжных систем. Правилами сервиса запрещено взимать дополнительные комиссии с пользователей - покупатели должны переводить точную сумму сделки.\n{'-'*60}',
                                             reply_markup=nav.inline_p2p_floating_menu_edit)
    elif int(request[0][15]) == 0:
        with suppress(TelegramBadRequest):
            await callback.message.edit_text(f'Отправьте процент от биржевого курса для {word} {cfg.coins_index[int(request[0][6])]}.\n\nБиржевой курс: {float(request_rate[0][0])} {cfg.bot_currency_2[int(request[0][3])]}\n\nЦена за 1 {cfg.coins_index[int(request[0][6])]} = {float(request_rate[0][0])} {cfg.bot_currency_2[int(request[0][3])]}\n\n{'-' * 60}\n⚠️ В цене объявления должны быть учтены все возможные комиссии платёжных систем. Правилами сервиса запрещено взимать дополнительные комиссии с пользователей - покупатели должны переводить точную сумму сделки.\n{'-' * 60}',
                                             reply_markup=nav.inline_p2p_floating_menu_edit)
    await state.set_state(cl.Announcement.percentage)

@dp.message(cl.Announcement.fix_count_sell)
async def fix_count_sell_edit(message: types.Message, state: FSMContext):
    data = await state.update_data()
    request = await read_db(f'p2p_advertisements WHERE number="{int(data['number'])}"', '*')
    request_rate = await read_db(
        f'exchange_rates WHERE currency_1="{cfg.coins_index[int(request[0][6])]}" && currency_2="{cfg.bot_currency_2[int(request[0][3])]}"',
        'rate')
    word = 'покупки'
    if data['type'] == 0:
        word = 'продажи'
    try:
        text = float((message.text).replace(',', '.'))
        await write_db(f"UPDATE p2p_advertisements SET fix_count_sell={text}, percentage = 0 WHERE number='{int(data['number'])}'")
        request = await read_db(f'p2p_advertisements WHERE number="{data['number']}"', '*')
        await bot.send_message(message.chat.id,f'Отправьте фиксированную цену в {cfg.bot_currency_2[int(request[0][3])]} для {word} {cfg.coins_index[int(request[0][6])]}.\n\nБиржевой курс: {float(request_rate[0][0])} {cfg.bot_currency_2[int(request[0][3])]}\n\nЦена за 1 {cfg.coins_index[int(request[0][6])]} = {request[0][13]} {cfg.bot_currency_2[int(request[0][3])]}\n\n{'-'*60}\n⚠️ В цене объявления должны быть учтены все возможные комиссии платёжных систем. Правилами сервиса запрещено взимать дополнительные комиссии с пользователей - покупатели должны переводить точную сумму сделки.\n{'-'*60}',
                               reply_markup=nav.inline_p2p_fix_menu_edit)
    except:
        await bot.send_message(message.chat.id,
                               f'Отправьте фиксированную цену в {cfg.bot_currency_2[int(request[0][3])]} для {word} {cfg.coins_index[int(request[0][6])]}.\n\nБиржевой курс: {float(request_rate[0][0])} {cfg.bot_currency_2[int(request[0][3])]}\n\nЦена за 1 {cfg.coins_index[int(request[0][6])]} = {request[0][13]} {cfg.bot_currency_2[int(request[0][3])]}\n\n{'-' * 60}\n⚠️ В цене объявления должны быть учтены все возможные комиссии платёжных систем. Правилами сервиса запрещено взимать дополнительные комиссии с пользователей - покупатели должны переводить точную сумму сделки.\n{'-' * 60}',
                               reply_markup=nav.inline_p2p_fix_menu_edit)
    await state.set_state(cl.Announcement.fix_count_sell)

@dp.message(cl.Announcement.percentage)
async def percentage_edit(message: types.Message, state: FSMContext):
    data = await state.update_data()
    request = await read_db(f'p2p_advertisements WHERE number="{int(data['number'])}"', '*')
    request_rate = await read_db(
        f'exchange_rates WHERE currency_1="{cfg.coins_index[int(request[0][6])]}" && currency_2="{cfg.bot_currency_2[int(request[0][3])]}"',
        'rate')
    word = 'покупки'
    if data['type'] == 0:
        word = 'продажи'
    try:
        text = float((message.text).replace(',', '.'))
        await write_db(f"UPDATE p2p_advertisements SET percentage={text}, fix_count_sell = 0 WHERE number='{int(data['number'])}'")
        request = await read_db(f'p2p_advertisements WHERE number="{data['number']}"', '*')
        await bot.send_message(message.chat.id,f'Отправьте процент от биржевого курса для {word} {cfg.coins_index[int(request[0][6])]}.\n(например,+4% или -2.5%)\n\nБиржевой курс: {float(request_rate[0][0])} {cfg.bot_currency_2[int(request[0][3])]}\n\nЦена за 1 {cfg.coins_index[int(request[0][6])]} = {float(request_rate[0][0]) + (float(request_rate[0][0]) * float(request[0][12]) / 100)} {cfg.bot_currency_2[int(request[0][3])]}\nПроцент биржевого курса: {request[0][12]}%\n\n{'-'*60}\n⚠️ В курсе объявления должны быть учтены все возможные комиссии платёжных систем. Правилами сервиса запрещено взимать дополнительные комиссии с пользователей - покупатели должны переводить точную сумму сделки.\n{'-'*60}',
                               reply_markup=nav.inline_p2p_floating_menu_edit)
    except:
        await bot.send_message(message.chat.id,f'Отправьте процент от биржевого курса для {word} {cfg.coins_index[int(request[0][6])]}.\n(например,+4% или -2.5%)\n\nБиржевой курс: {float(request_rate[0][0])} {cfg.bot_currency_2[int(request[0][3])]}\n\nЦена за 1 {cfg.coins_index[int(request[0][6])]} = {float(request_rate[0][0]) + (float(request_rate[0][0]) * float(request[0][12]) / 100)} {cfg.bot_currency_2[int(request[0][3])]}\nПроцент биржевого курса: {request[0][12]}%\n\n{'-' * 60}\n⚠️ В курсе объявления должны быть учтены все возможные комиссии платёжных систем. Правилами сервиса запрещено взимать дополнительные комиссии с пользователей - покупатели должны переводить точную сумму сделки.\n{'-' * 60}',
                               reply_markup=nav.inline_p2p_floating_menu_edit)
    await state.set_state(cl.Announcement.percentage)


@dp.callback_query(cl_m.Coins.filter())
async def buy_crypt_exchange(callback: CallbackQuery, callback_data: cl_m.Coins, state: FSMContext):
    if callback_data.action == 'select_coin':
        await state.set_state(cl.Buycrypt.type)
        type = callback_data.value
        request = await read_db(f'users WHERE login="{callback.from_user.username}"', 'currency')
        request_rate = await read_db(f'exchange_rates WHERE currency_1="{type}" && currency_2="{cfg.coins_index[request[0][0]]}"', 'rate, minimum_exchange_amount')
        await callback.message.edit_text(text=f'Купить: 🔹{type}\n{'-' * 30}\n🔹{cfg.coins_index[request[0][0]]} → 🔹{type}\n{'-' * 30}\nКурс: 1 {type} = {request_rate[0][0]} {cfg.coins_index[request[0][0]]}\n\nВведите количество валюты для покупки:\n\n{'-' * 70}\n⚠️Минимальная сумма покупки: {request_rate[0][1]} {type}.\n{'-' * 70}', reply_markup=nav.inlnine_exchange_menu_back)
        await state.set_state(cl.Buycrypt.amount)
        await state.update_data(type=type)
    elif callback_data.action == 'back_exchange':
        request = await read_db(f'users_purses WHERE login="{callback.from_user.username}"', '*')
        request_2 = await read_db(f'users WHERE login="{callback.from_user.username}"', 'currency')
        await callback.message.edit_text(f' 🐬 Здесь вы можете торговать криптовалютой как на обычной бирже.\n'
                                         f'⚡️ Все заявки на обмен выполняются автоматически.\n{'-' * 40}\nID пользователя: '
                                         f'{callback.from_user.username}\nОбщий баланс в {cfg.coins_2[request_2[0][0]]}: {request[0][request_2[0][0]+2]} {cfg.coins_index[request_2[0][0]]}\n{'-' * 40}\n '
                                         f'🔹Tether: {request[0][2]} USDT \n🔹Toncoin: {request[0][3]} TON \n🔹Gram: {request[0][4]} GRAM \n '
                                         f'🔹Bitcoin: {request[0][5]} BTC '
                                         f'\n🔹Litecoin: {request[0][6]} LTC \n🔹Ethereum: {request[0][7]} ETH \n '
                                         f'🔹Binance Coin: {request[0][8]} BNB \n🔹TRON: {request[0][9]} TRX \n '
                                         f'🔹USD Coin: {request[0][10]} USDC',
                                         reply_markup=nav.inlnine_exchange_menu_hide_zero)
    elif callback_data.action == 'select_coin_sell':
        await state.set_state(cl.Sellcrypt.type)
        type = callback_data.value
        request = await read_db(f'users WHERE login="{callback.from_user.username}"', 'currency')
        await state.update_data(type_user=cfg.bot_currency_2[request[0][0]])
        request_rate = await read_db(
            f'exchange_rates WHERE currency_1="{type}" && currency_2="{cfg.coins_index[request[0][0]]}"',
            'rate, minimum_exchange_amount')
        await callback.message.edit_text(
            text=f'Продать: 🔹{type}\n{'-' * 50}\n 🔹{type} → 🔹{cfg.coins_index[request[0][0]]}\n{'-' * 50} \nКурс: 1 {type} = {request_rate[0][0]} {cfg.coins_index[request[0][0]]}\n\nВведите количество валюты для продажи:\n\n{'-' * 80}\n⚠️Минимальное количество для продажи {request_rate[0][1]} {type}\n{'-' * 80}',
            reply_markup=nav.inlnine_exchange_menu_back_3)
        await state.update_data(type=type)
        await state.set_state(cl.Sellcrypt.amount)
    elif callback_data.action == 'select_coin_trade':
        await state.set_state(cl.Tradecrypt.type)
        type = callback_data.value
        await callback.message.edit_text(text=f'{'-' * 30}\nВыбрано: 🔹{type}\n{'-' * 30}\n\n Теперь выберите направление для обмена:',reply_markup=nav.builder_trade_2.as_markup())
        await state.update_data(type=type)
        await state.set_state(cl.Sellcrypt.amount)
    elif callback_data.action == 'select_coin_trade_2':
        type = callback_data.value
        data = await state.get_data()
        request = await read_db(
            f'exchange_rates WHERE currency_1="{data['type']}" && currency_2="{type}"',
            'rate, minimum_exchange_amount')
        await state.update_data(type_user=type)
        await state.update_data(course=request[0][0])
        await state.update_data(min=request[0][1])
        data = await state.get_data()
        await callback.message.edit_text(
            text=f'{'-' * 90}\nОбмен 🔹{data['type']} → 🔹{type}\n{'-' * 90}\nКурс: 1 {data['type']} - {request[0][0]}{type} {type}\n\nВведите количество {data['type']} которое хотите обменять:\n\n{'-' * 90}\n⚠️Минимальное количество для обмена {request[0][1]} {data['type']}\n{'-' * 90}',
            reply_markup=nav.inline_back_exchange_menu_trade_crypt)
        await state.set_state(cl.Sellcrypt.count)


@dp.callback_query(F.data == 'hide_zero_balance')
async def hide_zero_balance(callback: CallbackQuery):
    request = await read_db(f'users_purses WHERE login="{callback.from_user.username}"', 'USDT, TON, GRAM, BTC, LTC, ETH, BNB, TRX, USDC, NOT_C')
    request_2 = await read_db(f'users WHERE login="{callback.from_user.username}"', 'currency')
    await callback.answer(text='Нулевые балансы скрыты.')
    answer = str('')
    count = 0
    for i in request[0]:
        if float(i) != 0:
            answer += cfg.coins_2[count] + ': ' + str(i) + ' ' + cfg.coins_index[count] + '\n'
        count += 1
    await callback.message.edit_text(text=f' 🐬 Здесь вы можете торговать криптовалютой как на обычной бирже.'
                                          f'\n⚡️ Все заявки на обмен выполняются автоматически.\n{'-'*40}'
                                          f'\nID пользователя: {callback.from_user.username}\nОбщий баланс в '
                                          f'{cfg.coins_2[request_2[0][0]]} {request[0][request_2[0][0]]} '
                                          f'{cfg.coins_index[request_2[0][0]]}\n{'-' * 40}\n{answer}'
                                     ,reply_markup=nav.inlnine_exchange_menu_show_zero)


@dp.callback_query(F.data == 'story_exchange')
async def exchange_menu_story(callback: CallbackQuery):
    await callback.message.edit_text(f'🐬 Здесь вы можете посмотреть историю покупок, продаж и обменов.', reply_markup=nav.inline_exchange_menu_story)


@dp.callback_query(F.data == 'story_exchange_buy')
async def exchange_menu_story(callback: CallbackQuery):
    request = await read_db(f'exchange_logs WHERE login="{callback.from_user.username}" && type="purchase"', 'currency_1, currency_2, count, date, number')
    output, count = '', 0
    for i in request:
        output += ('-' * 100) + '\n' + '#' + str(request[count][4]) + ' ' + str(request[count][3]) + ' ' + str(request[count][0]) + ' → ' + str(request[count][1]) + ' ' + 'Cумма: ' + str(request[count][2]) + ' ' + str(request[count][1]) + '\n' +('-' * 100) + '\n'
        count += 1
    await callback.message.edit_text(f'История ваших покупок в обменнике:\n\n{output}', reply_markup=nav.inline_exchange_menu_story)


@dp.callback_query(F.data == 'story_exchange_trade')
async def exchange_menu_story(callback: CallbackQuery):
    request = await read_db(f'exchange_logs WHERE login="{callback.from_user.username}" && type="trade"', 'currency_1, currency_2, count, date, number')
    output, count = '', 0
    for i in request:
        output += ('-' * 100) + '\n' + '#' + str(request[count][4]) + ' ' + str(request[count][3]) + ' ' + str(request[count][0]) + ' → ' + str(request[count][1]) + ' ' + 'Cумма: ' + str(request[count][2]) + ' ' + str(request[count][1]) + '\n' + ('-' * 100) + '\n'
        count += 1
    await callback.message.edit_text(f'История ваших обменов в обменнике:\n\n{output}', reply_markup=nav.inline_exchange_menu_story)


@dp.callback_query(F.data == 'story_exchange_sell')
async def exchange_menu_story(callback: CallbackQuery):
    request = await read_db(f'exchange_logs WHERE login="{callback.from_user.username}" && type="sell"', 'currency_1, currency_2, count, date, number')
    output, count = '', 0
    for i in request:
        output += ('-' * 100) + '\n' + '#' +str(request[count][4]) + ' '+ str(request[count][3]) + ' ' + str(request[count][0]) + ' → ' + str(request[count][1]) + 'Cумма: ' + str(request[count][2]) + ' ' + str(request[count][1]) + '\n'+ ('-' * 100) + '\n'
        count += 1
    await callback.message.edit_text(f'История ваших продаж в обменнике:\n\n{output}', reply_markup=nav.inline_exchange_menu_story)


@dp.callback_query(F.data == 'show_zero_balance')
async def show_zero_balance(callback: CallbackQuery):
    request = await read_db(f'users_purses WHERE login="{callback.from_user.username}"', '*')
    request_2 = await read_db(f'users WHERE login="{callback.from_user.username}"', 'currency')
    await callback.answer(text='Нулевые балансы показаны.')
    await callback.message.edit_text(text=f'🐬 Здесь вы можете торговать криптовалютой как на обычной бирже.'
                                          f'\n⚡️ Все заявки на обмен выполняются автоматически.\n{'-'*40}'
                                          f'\nID пользователя: {callback.from_user.username}\nОбщий баланс '
                                          f'{cfg.coins_2[request_2[0][0]]}: {request[0][request_2[0][0]+2]} '
                                          f'{cfg.coins_index[request_2[0][0]]} \n{'-' * 40}\n{cfg.coins_2[0]}: {request[0][2]} '
                                          f'{cfg.coins_index[0]} \n{cfg.coins_2[1]}: {request[0][3]} {cfg.coins_index[1]} '
                                          f'\n{cfg.coins_2[2]}: {request[0][4]} {cfg.coins_index[2]} \n{cfg.coins_2[3]}: '
                                          f'{request[0][5]} {cfg.coins_index[3]} \n{cfg.coins_2[4]}: {request[0][6]} '
                                          f'{cfg.coins_index[4]} \n{cfg.coins_2[5]}: {request[0][7]} {cfg.coins_index[5]} '
                                          f'\n{cfg.coins_2[6]}: {request[0][8]} {cfg.coins_index[6]} \n{cfg.coins_2[7]}: '
                                          f'{request[0][9]} {cfg.coins_index[7]} \n{cfg.coins_2[8]}: {request[0][10]} '
                                          f'{cfg.coins_index[8]}\n{cfg.coins_2[9]}: {request[0][11]} {cfg.coins_index[9]}',
                                     reply_markup=nav.inlnine_exchange_menu_hide_zero)


@dp.callback_query(F.data == 'buy_crypt')
async def buy_crupt(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text=f'Выберите валюту, которую вы хотите купить:',reply_markup=nav.builder.as_markup())


@dp.callback_query(F.data == 'trade_cpypt')
async def buy_crupt(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text=f'Выберите валюту, которую вы хотите использовать для обмена:',reply_markup=nav.builder_trade.as_markup())


@dp.callback_query(F.data == 'sell_crypt')
async def buy_crupt(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text=f'Выберите валюту, которую вы хотите продать:',reply_markup=nav.builder_sell.as_markup())


@dp.callback_query(F.data == 'p2p_deactivate')
async def p2p_trade_deactiveate(callback: CallbackQuery, state: FSMContext):
    await write_db(f"UPDATE users SET active_user=0 WHERE login='{callback.from_user.username}'")
    await write_db(f"UPDATE p2p_advertisements SET status=0 WHERE login='{callback.from_user.username}'")
    request = await read_db(f'users WHERE login="{callback.from_user.username}"', 'active_user')
    request_2 = await read_db(f'exchange_rates WHERE currency_1="USDT" && currency_2="RUB"', 'rate')
    if request[0][0] == 1:
        status = '✅ Активная торговля'
    else:
        status = '❌ Торговля деактивирована'
    await callback.answer(text='Торговля деактивирована')
    await callback.message.edit_text(f'Здесь Вы совершаете сделки с людьми, а бот выступает как гарант.'
                                     f'\nБудтье вежливы друг с другом.\nБиржевой курс: {request_2[0][0]} RUB за 1 USDT\nТекущий ваш статус:\n{' '*20}{status}',
                                     reply_markup=nav.inline_p2p_main_menu_activate)


@dp.callback_query(F.data == 'p2p_activate')
async def p2p_trade_activeate(callback: CallbackQuery, state: FSMContext):
    await write_db(f"UPDATE users SET active_user=1 WHERE login='{callback.from_user.username}'")
    await write_db(f"UPDATE p2p_advertisements SET status=1 WHERE login='{callback.from_user.username}'")
    request = await read_db(f'users WHERE login="{callback.from_user.username}"', 'active_user')
    request_2 = await read_db(f'exchange_rates WHERE currency_1="USDT" && currency_2="RUB"', 'rate')
    if request[0][0] == 1:
        status = '✅ Активная торговля'
    else:
        status = '❌ Торговля деактивирована'
    await callback.answer(text='Торговля активирована')
    await callback.message.edit_text(
                           f'Здесь Вы совершаете сделки с людьми, а бот выступает как гарант.'
                           f'\nБудтье вежливы друг с другом.\nБиржевой курс: {request_2[0][0]} RUB за 1 USDT\nТекущий ваш статус:\n{' '*20}{status}',
                           reply_markup=nav.inline_p2p_main_menu_deactivate)


@dp.callback_query(F.data == 'back_p2p_menu')
async def back_p2p_menu(callback: CallbackQuery, state: FSMContext):
    request = await read_db(f'users WHERE login="{callback.from_user.username}"', 'active_user')
    request_2 = await read_db(f'exchange_rates WHERE currency_1="USDT" && currency_2="RUB"', 'rate')
    if request[0][0] == 1:
        status = '✅ Активная торговля'
    else:
        status = '❌ Торговля деактивирована'
    mark = nav.inline_p2p_main_menu_deactivate
    if int(request[0][0]) == 0:
        mark = nav.inline_p2p_main_menu_activate
    await callback.message.edit_text(f'Здесь Вы совершаете сделки с людьми, а бот выступает как гарант.'
                                            f'\nБудтье вежливы друг с другом.\nБиржевой курс: {request_2[0][0]} RUB за 1 USDT'
                                            f'\nТекущий ваш статус:\n{' ' * 20}{status}', reply_markup=mark)


@dp.callback_query(F.data == 'my_advertisements')
async def p2p_active_trades(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    request = await read_db(
        f'p2p_advertisements WHERE login="{callback.from_user.username}"', '*')
    await state.set_state(cl.Announcement_pag.mass)
    if not request:
        await callback.message.edit_text(f'У вас пока нет объявлений', reply_markup=nav.inline_p2p_create_main_menu)
    else:
        count = 0
        count2 = 0
        mass = []
        mass2 = []
        for i in request:
            word = 'продаже'
            if count >= 10:
                if int(request[count2][15]) == 1:
                    word = 'покупке'
                mass.append(mass2.copy())
                mass2.clear()
                count = 0
                mass2.append(InlineKeyboardButton(text=f'Объявление о {word} #{request[count2][1]}', callback_data=cl_m.Advertisements(action='select_adv2', number=f'{request[count2][1]}').pack())),
            else:
                if int(request[count2][15]) == 1:
                    word = 'покупке'
                mass2.append(InlineKeyboardButton(text=f'Объявление о {word} #{request[count2][1]}', callback_data=cl_m.Advertisements(action='select_adv2', number=f'{request[count2][1]}').pack()))
            count += 1
            count2 += 1
        mass.append(mass2.copy())
        await state.update_data(mass=mass)
        with suppress(TelegramBadRequest):
            await callback.message.edit_text(f'У вас {len(request)} объявлений.', reply_markup=paginator_avde(mass))


@dp.callback_query(cl_m.Advertisements.filter())
async def p2p_create_buy_fiat(callback: CallbackQuery, callback_data: cl_m.Advertisements, state: FSMContext):
    number = callback_data.number
    await state.set_state(cl.Buyp2p.crypto)
    await state.update_data(number=number)
    if callback_data.action == 'select_adv':
        request = await read_db(f'p2p_advertisements WHERE number="{number}"', f'*')
        request_2 = await read_db(f'freezing_of_funds WHERE number_adv="{number}",{cfg.coins_index[int(request[0][6])]}')
        request_3 = await read_db(f'users_vendor WHERE id="{request[0][0]}"', 'sum, count, rep_plus, rep_minus')
        await state.update_data(bank=request[0][5], crypto=request[0][6], fiat=request[0][3], sum=request[0][14], conditions=request[0][11], time=request[0][10], type=request[0][15])
        data = await state.get_data()
        volume = 0
        count = 0
        if request_2:
            for i in request_2:
                volume += float(request_2[count][0])
                count += 1
            volume = float(request[0][7]) - volume
        else:
            volume = float(request[0][7])
        await state.update_data(volume=volume)
        time = f'{data['time']} минут'
        if int(data['time']) == 60:
            time = '1 час'
        banks = request[0][5].replace(',', '').split()
        count, bank, conditions = 1, '', 'не указаны.'
        conditions = str(request[0][11])
        for i in banks:
            bank += str(count) + '. ' + str(cfg.banks[int(i)]) + '\n'
            count += 1
        word = 'продает'
        mark = nav.inline_p2p_buy_create_menu
        if int(data['type']) == 0:
            mark = nav.inline_p2p_sell_create_menu
            word = 'покупает'
        if int(request_3[0][2]) == 0:
            likes = 0
        else:
            likes = (request_3[0][2] / (request_3[0][2] + request_3[0][3])) * 100
        if int(request_3[0][3]) == 0:
            dislikes = 0
        else:
            dislikes = (request_3[0][3] / (request_3[0][2] + request_3[0][3])) * 100
        id = str(request[0][0])
        if int(request_3[0][1]) >= 3:
            id = str(request[0][0]) + '✅'
        await callback.message.edit_text(f'📉 Объявление #{number}\n\n👤 id{id} {word} '
                                         f'{cfg.coins_index[data['crypto']]} за {cfg.bot_currency_2[data['fiat']]}'
                                         f'\n🏆 {request_3[0][1]} сделок · ${request_3[0][0]}\n👍: {likes}% 👎: {dislikes}%\n\n Цена за 1 {cfg.coins_index[data['crypto']]}: '
                                         f'{data['sum']} {cfg.bot_currency_2[data['fiat']]}\n\nДоступный объем: '
                                         f'{volume} {cfg.coins_index[data['crypto']]}\nЛимиты: '
                                         f'{request[0][8]} - {request[0][9]} {cfg.bot_currency_2[data['fiat']]} или '
                                         f'{float(request[0][8]) / float(request[0][14])} ~ '
                                         f'{float(request[0][9]) / float(request[0][14])} '
                                         f'{cfg.coins_index[data['crypto']]}\n\nСпособы оплаты:\n{bank}\n\nСрок оплаты: '
                                         f'{time}\n\nУсловия сделки: {conditions}', reply_markup=mark)
    elif callback_data.action == 'select_adv3':
        request_4 = await read_db(f'freezing_of_funds WHERE number="{number}"', f'number_adv')
        request = await read_db(f'p2p_advertisements WHERE number="{request_4[0][0]}"', f'*')
        request_2 = await read_db(f'freezing_of_funds WHERE number_adv="{number}"','{cfg.coins_index[int(request[0][6])]}')
        request_3 = await read_db(f'users_vendor WHERE id="{request[0][0]}"', 'sum, count, rep_plus, rep_minus')
        await state.update_data(bank=request[0][5], crypto=request[0][6], fiat=request[0][3], sum=request[0][14], conditions=request[0][11], time=request[0][10], type=request[0][15])
        data = await state.get_data()
        volume = 0
        count = 0
        if request_2:
            for i in request_2:
                volume += float(request_2[count][0])
                count += 1
            volume = float(request[0][7]) - volume
        else:
            volume = float(request[0][7])
        await state.update_data(volume=volume)
        time = f'{data['time']} минут'
        if int(data['time']) == 60:
            time = '1 час'
        banks = request[0][5].replace(',', '').split()
        count, bank, conditions = 1, '', 'не указаны.'
        conditions = str(request[0][11])
        for i in banks:
            bank += str(count) + '. ' + str(cfg.banks[int(i)]) + '\n'
            count += 1
        word = 'продает'
        if int(data['type']) == 0:
                   word = 'покупает'
        if int(request_3[0][2]) == 0:
            likes = 0
        else:
            likes = (request_3[0][2] / (request_3[0][2] + request_3[0][3])) * 100
        if int(request_3[0][3]) == 0:
            dislikes = 0
        else:
            dislikes = (request_3[0][3] / (request_3[0][2] + request_3[0][3])) * 100
        id = str(request[0][0])
        if int(request_3[0][1]) >= 3:
            id = str(request[0][0]) + '✅'
        await callback.message.edit_text(f'📉 Объявление #{number}\n\n👤 id{id} {word} '
                                         f'{cfg.coins_index[data['crypto']]} за {cfg.bot_currency_2[data['fiat']]}'
                                         f'\n🏆 {request_3[0][1]} сделок · ${request_3[0][0]}\n👍: {likes}% 👎: {dislikes}%\n\n Цена за 1 {cfg.coins_index[data['crypto']]}: '
                                         f'{data['sum']} {cfg.bot_currency_2[data['fiat']]}\n\nДоступный объем: '
                                         f'{volume} {cfg.coins_index[data['crypto']]}\nЛимиты: '
                                         f'{request[0][8]} - {request[0][9]} {cfg.bot_currency_2[data['fiat']]} или '
                                         f'{float(request[0][8]) / float(request[0][14])} ~ '
                                         f'{float(request[0][9]) / float(request[0][14])} '
                                         f'{cfg.coins_index[data['crypto']]}\n\nСпособы оплаты:\n{bank}\n\nСрок оплаты: '
                                         f'{time}\n\nУсловия сделки: {conditions}', reply_markup=nav.inline_p2p_active_menu)
    elif callback_data.action == 'select_adv2':
        request = await read_db(f'p2p_advertisements WHERE number="{number}"', f'*')
        request_2 = await read_db(f'freezing_of_funds WHERE number_adv="{number}"', '{cfg.coins_index[int(request[0][6])]}')
        request_3 = await read_db(f'users_vendor WHERE id="{request[0][0]}"', 'sum, count, rep_plus, rep_minus')
        number = callback_data.number
        await state.set_state(cl.Buyp2p.number)
        await state.update_data(number=number)
        type = request[0][15]
        await state.update_data(type=type)
        data = await state.get_data()
        request = await read_db(f'p2p_advertisements WHERE number="{number}"', '*')
        request_rate = await read_db(f'exchange_rates WHERE currency_2="{cfg.bot_currency_2[int(request[0][3])]}" && currency_1="{cfg.coins_index[request[0][6]]}"','rate')
        sum = request[0][13]
        if request[0][12] != 0:
            sum = float(request_rate[0][0]) + (float(request[0][12]) * float(request_rate[0][0]) / 100)
        word = 'Продажа'
        time = f'{request[0][10]} минут'
        if int(request[0][10]) == 60:
            time = '1 час'
        if int(request[0][15]) == 1:
            word = 'Покупка'
        banks = request[0][5].replace(',', '').split()
        count, bank = 1, ''
        for i in banks:
            bank += str(count) + '. ' + str(cfg.banks[int(i)]) + '\n'
            count += 1
        await callback.message.edit_text(
            f'🧾 Объявление #{request[0][1]}\n\n{word} {cfg.coins_index[int(request[0][6])]} за '
            f'{cfg.bot_currency_2[int(request[0][3])]}.\n\nЦена: {sum} '
            f'{cfg.bot_currency_2[int(request[0][3])]}\n\nОбщий объем: '
            f'{int(float(request[0][7]))} {cfg.coins_index[int(request[0][6])]}\nЛимиты: '
            f'{int(request[0][8])} {cfg.bot_currency_2[int(request[0][3])]} ~'
            f' {int(request[0][9])} {cfg.bot_currency_2[int(request[0][3])]}\n\n Способы '
            f'оплаты:\n{bank}\n\nСрок оплаты: {time}\n\nУсловия сделки: не указаны.\n\n👌 '
            f'Активно. Объявление показывается в общем списке.',
            reply_markup=nav.inline_p2p_buy_curr_menu_3)
    elif callback_data.action == 'select_ticket':
        id = callback_data.number
        await state.set_state(cl.Adm.id)
        await state.update_data(id=id)
        request = await read_db(f'support_tickets WHERE number_tik="{id}" ', '*')
        request_4 = await read_db(f'p2p_advertisements WHERE number={request[0][1]} ', '*')
        request_5 = await read_db(f'freezing_of_funds WHERE number="{request[0][0]}" ', f'login, login_vendor, {cfg.coins_index[int(request_4[0][6])]}, data')  #запрос по сделке
        word = 'Продает'
        if int(request_4[0][15]) == 1:
            word = 'Покупает'
        await callback.message.edit_text(f'Информация по запросу\nНомер запроса: #{request[0][6]} '
                                         f'Номер объявления #{request[0][1]}\nСредства заморожены по сделке #D{request[0][0]}'
                                         f'\nДата поступления обращения: {request[0][5]}\nТекст обращения: {request[0][4]}'
                                         f'\n\nИнформация по объявлению:\nОбъявление номер #{request[0][1]}\n'
                                         f'Продавец: {request_4[0][2]}\n{word} {cfg.coins_index[int(request_4[0][6])]} в количестве {request_4[0][7]} по цене {request_4[0][15]} {cfg.bot_currency_2[int(request_4[0][6])]}'
                                         f'\n Дата создания объявления {request_4[0][16]}\n\nИнформация по сделке:\nНомер сделки #D{request[0][0]}'
                                         f'\nЛогин покупателя: {request_5[0][0]}\nЛогин продавца: {request_5[0][1]}\nКоличество замороженных средств: {request_5[0][2]} {cfg.coins_index[int(request_4[0][6])]}\nДата создания сделки: {request_5[0][3]}'
                                         , reply_markup=nav.inline_p2p_tickets_delete_menu)


@dp.callback_query(F.data == 'p2p_buy_create')
async def p2p_buy_create(callback: CallbackQuery, state: FSMContext):
    request = await read_db(f'users WHERE id="{callback.from_user.id}" ', 'name')
    if str(request[0][0]) == '0':
        await callback.message.edit_text(f'Для совершения покупок необходимо пройти верификацию.'
                                         f'\nПройти ее можно нажав на кнопку "✅ Верификация" ниже.')
    else:
        data = await state.get_data()
        word = 'купить'
        mark = nav.inline_p2p_buy_create_fiat_menu
        if int(data['type']) == 0:
            mark = ''
            word = 'продать'
        request = await read_db(f'p2p_advertisements WHERE number="{int(data['number'])}"', '*')
        await callback.message.edit_text(f'Отправьте сумму {cfg.coins_index[int(data['crypto'])]}, которую вы хотите {word}.'
                                         f'\n\nМинимум: {float(request[0][8]) / float(request[0][14])} {cfg.coins_index[int(data['crypto'])]}\n'
                                         f'Максимум: {float(request[0][9]) / float(request[0][14])} {cfg.coins_index[int(data['crypto'])]}\n\n'
                                         f'Цена за 1 {cfg.coins_index[int(data['crypto'])]}: {data['sum']}{cfg.bot_currency_2[int(data['fiat'])]}',
                                         reply_markup=nav.inline_p2p_buy_create_fiat_menu)
        await state.set_state(cl.Buyp2p.sum_crypt)


@dp.callback_query(F.data == 'p2p_buy_create_fiat')
async def p2p_buy_create(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    word = 'купить'
    mark = nav.inline_p2p_buy_create_2_menu
    if int(data['type']) == 0:
        mark = ''
        word = 'продать'
    request = await read_db(f'p2p_advertisements WHERE number="{int(data['number'])}"', '*')
    await callback.message.edit_text(f'Отправьте сумму {cfg.bot_currency_2[int(data['fiat'])]}, за которую вы хотите {word}.'
                                     f'\n\nМинимум: {request[0][8]} {cfg.bot_currency_2[int(data['fiat'])]}\n'
                                     f'Максимум: {request[0][9]} {cfg.bot_currency_2[int(data['fiat'])]}\n\n'
                                     f'Цена за 1 {cfg.coins_index[int(data['crypto'])]}: {data['sum']}{cfg.bot_currency_2[int(data['fiat'])]}',
                                     reply_markup=nav.inline_p2p_buy_create_2_menu)
    await state.set_state(cl.Buyp2p.sum_fiat)


@dp.message(cl.Buyp2p.sum_crypt)
async def percentage_edit(message: types.Message, state: FSMContext):
    try:
        sum = message.text.replace(',', '.')
        data = await state.get_data()
        word = 'купить'
        mark = nav.inline_p2p_buy_create_fin_menu
        if int(data['type']) == 0:
            mark = nav.inline_p2p_sell_create_fin_menu
            word = 'продать'
        request = await read_db(f'p2p_advertisements WHERE number="{int(data['number'])}"', '*')
        await state.update_data(sum_crypt=sum)
        await state.update_data(sum_fiat=float(sum)*float(data['sum']))
        data = await state.get_data()
        if float(sum) > float(data['volume']):
            await state.set_state(cl.Buyp2p.sum_crypt)
            await bot.send_message(message.chat.id,f'Отправьте сумму {cfg.coins_index[int(data['crypto'])]}, которую вы хотите {word}.'
                f'\n\nМинимум: {float(request[0][8]) / float(request[0][14])} {cfg.coins_index[int(data['crypto'])]}\n'
                f'Максимум: {float(request[0][9]) / float(request[0][14])} {cfg.coins_index[int(data['crypto'])]}\n\n'
                f'Цена за 1 {cfg.coins_index[int(data['crypto'])]}: {data['sum']}{cfg.bot_currency_2[int(data['fiat'])]}'
                                                   f'\n\nСумма покупки не может быть больше объема продажи из объявления!',
                reply_markup=nav.inline_p2p_buy_create_fiat_menu)
        elif float(sum) < (float(request[0][8]) / float(request[0][14])) or float(sum) > (float(request[0][9]) / float(request[0][14])):
            await bot.send_message(message.chat.id,
                                   f'Отправьте сумму {cfg.coins_index[int(data['crypto'])]}, которую вы хотите {word}.'
                                   f'\n\nМинимум: {float(request[0][8]) / float(request[0][14])} {cfg.coins_index[int(data['crypto'])]}\n'
                                   f'Максимум: {float(request[0][9]) / float(request[0][14])} {cfg.coins_index[int(data['crypto'])]}\n\n'
                                   f'Цена за 1 {cfg.coins_index[int(data['crypto'])]}: {data['sum']}{cfg.bot_currency_2[int(data['fiat'])]}'
                                   f'\n\nСумма покупки не должна превышать пороги покупки!',
                                   reply_markup=nav.inline_p2p_buy_create_fiat_menu)
            await state.set_state(cl.Buyp2p.sum_crypt)
        else:
            await bot.send_message(message.chat.id, f'Вы уверены, что хотите {word} {sum} '
                                                    f'{cfg.coins_index[int(data['crypto'])]} за {float(sum) * float(data['sum'])} '
                                                    f'{cfg.bot_currency_2[int(data['fiat'])]}?', reply_markup=nav.inline_p2p_buy_create_fin_menu)
            await state.set_state(cl.Buyp2p.sum_crypt)
    except:
        data = await state.get_data()
        word = 'купить'
        if int(data['type']) == 0:
            word = 'продать'
        request = await read_db(f'p2p_advertisements WHERE number="{int(data['number'])}"', '*')
        await bot.send_message(message.chat.id,
            f'Отправьте сумму {cfg.coins_index[int(data['crypto'])]}, которую вы хотите {word}.'
            f'\n\nМинимум: {float(request[0][8]) / float(request[0][14])} {cfg.coins_index[int(data['crypto'])]}\n'
            f'Максимум: {float(request[0][9]) / float(request[0][14])} {cfg.coins_index[int(data['crypto'])]}\n\n'
            f'Цена за 1 {cfg.coins_index[int(data['crypto'])]}: {data['sum']}{cfg.bot_currency_2[int(data['fiat'])]}',
            reply_markup=nav.inline_p2p_buy_create_fiat_menu)
        await state.set_state(cl.Buyp2p.sum_crypt)

@dp.message(cl.Buyp2p.sum_fiat)
async def percentage_edit(message: types.Message, state: FSMContext):
    try:
        sum = message.text.replace(',', '.')
        data = await state.get_data()
        word = 'купить'
        mark = nav.inline_p2p_buy_create_fin_menu
        if int(data['type']) == 0:
            mark = nav.inline_p2p_sell_create_fin_menu
            word = 'продать'
        request = await read_db(f'p2p_advertisements WHERE number="{int(data['number'])}"', '*')
        await state.update_data(sum_fiat=sum)
        await state.update_data(sum_crypt=float(sum)/float(data['sum']))
        data = await state.get_data()
        if float(data['volume']) < (float(sum) / float(data['sum'])):
            await bot.send_message(message.chat.id,f'Отправьте сумму {cfg.bot_currency_2[int(data['fiat'])]}, '
                                                   f'за которую вы хотите {word}.\n\n'
                                                   f'Минимум: {request[0][8]} {cfg.bot_currency_2[int(data['fiat'])]}\n'
                                                   f'Максимум: {request[0][9]} {cfg.bot_currency_2[int(data['fiat'])]}'
                                                   f'\n\nЦена за 1 {cfg.coins_index[int(data['crypto'])]}: '
                                                   f'{data['sum']}{cfg.bot_currency_2[int(data['fiat'])]}'
                                                   f'\n\nСумма покупки не должна превышать пороги покупки!',
                                   reply_markup=nav.inline_p2p_buy_create_2_menu)
            await state.set_state(cl.Buyp2p.sum_fiat)
        elif float(sum) < float(request[0][8]) or float(sum) > float(request[0][9]):
            await bot.send_message(message.chat.id,
                                   f'Отправьте сумму {cfg.bot_currency_2[int(data['fiat'])]}, за которую вы хотите купить.'
                                   f'\n\nМинимум: {request[0][8]} {cfg.bot_currency_2[int(data['fiat'])]}\n'
                                   f'Максимум: {request[0][9]} {cfg.bot_currency_2[int(data['fiat'])]}\n\n'
                                   f'Цена за 1 {cfg.coins_index[int(data['crypto'])]}: {data['sum']}'
                                   f'{cfg.bot_currency_2[int(data['fiat'])]}\n\n'
                                   f'Сумма покупки не может быть выходить за максимальный и минимальный пороги объявления!',
                                   reply_markup=nav.inline_p2p_buy_create_2_menu)
            await state.set_state(cl.Buyp2p.sum_fiat)
        else:
            await bot.send_message(message.chat.id, f'Вы уверены, что хотите {word} {float(sum) / float(data['sum'])} '
                                                    f'{cfg.coins_index[int(data['crypto'])]} за {sum} {cfg.bot_currency_2[int(data['fiat'])]}?'
                                   , reply_markup=nav.inline_p2p_buy_create_fin_menu)
            await state.set_state(cl.Buyp2p.sum_fiat)
    except:
        data = await state.get_data()
        word = 'купить'
        if int(data['type']) == 0:
            word = 'продать'
        request = await read_db(f'p2p_advertisements WHERE number="{int(data['number'])}"', '*')
        await bot.send_message(message.chat.id,
            f'Отправьте сумму {cfg.bot_currency_2[int(data['fiat'])]}, за которую вы хотите {word}.'
            f'\n\nМинимум: {request[0][8]} {cfg.bot_currency_2[int(data['fiat'])]}\n'
            f'Максимум: {request[0][9]} {cfg.bot_currency_2[int(data['fiat'])]}\n\n'
            f'Цена за 1 {cfg.coins_index[int(data['crypto'])]}: {data['sum']}{cfg.bot_currency_2[int(data['fiat'])]}',
            reply_markup=nav.inline_p2p_buy_create_2_menu)
        await state.set_state(cl.Buyp2p.sum_fiat)


@dp.callback_query(F.data == 'p2p_sell_create_fin')
async def p2p_buy_create(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    request = await read_db(f'p2p_advertisements WHERE number="{int(data['number'])}"', '*')
    request_2 = await read_db(f'users WHERE login="{str(request[0][2])}"', 'login, id')
    request_3 = await read_db(f'users_vendor WHERE id="{request[0][0]}"', 'sum, count, rep_plus, rep_minus')
    number = random.randint(10000, 9999999)
    word = 'Покупаете'
    type = 1
    if int(data['type']) == 0:
        word = 'Продаете'
        type = 0
    if int(request_3[0][2]) == 0:
        likes = 0
    else:
        likes = (request_3[0][2] / (request_3[0][2] + request_3[0][3])) * 100
    if int(request_3[0][3]) == 0:
        dislikes = 0
    else:
        dislikes = (request_3[0][3] / (request_3[0][2] + request_3[0][3])) * 100
    builder_trade_active_2 = InlineKeyboardBuilder()
    builder_trade_active_2.button(
        text='Отменить сделку',
        callback_data=cl_m.Advertisements_p2p(action='p2p_buy_cancel', value=f'{number}')
    )
    builder_trade_active_2.button(
        text='К списку активных сделок',
        callback_data='p2p_active_trades'
    )
    builder_trade_active_2.adjust(1)
    builder_trade_active_2.as_markup()
    id = str(request[0][0])
    if int(request_3[0][1]) >= 3:
        id = str(request[0][0]) + '✅'
    min = 60
    if int(request[0][10]) == 30 or int(request[0][10]) == 15:
        min = int(request[0][10])
    current_time = datetime.now() + timedelta(minutes=min)
    current_time = current_time.strftime('%Y-%m-%d %H:%M:%S')
    current_time2 = datetime.now() + timedelta(minutes=10)
    current_time2 = current_time2.strftime('%Y-%m-%d %H:%M:%S')
    await write_db(f"INSERT INTO active_transactions (number, sum, type_fiat, type_crypt, count, bank, login_customer, login_vendor, type, delete_at) VALUES ({number}, '{str(data['sum'])}', {int(data['fiat'])}, {int(data['crypto'])}, '{str(data['sum_crypt'])}', '{str(data['bank'])}', '{str(callback.from_user.username)}', '{str(request_2[0][0])}', {type}, '{current_time2}')")
    await write_db(f"INSERT INTO freezing_of_funds (number, number_adv, login, login_vendor, {cfg.coins_index[int(data['crypto'])]}, time, delete_at) VALUES ({number}, {int(data['number'])}, '{str(callback.from_user.username)}', '{str(request_2[0][0])}' ,'{data['sum_crypt']}', {int(request[0][10])}, '{current_time}')")
    await callback.message.edit_text(f'Сделка #D{number}\n\n👤 id{id}\n🏆 {request_3[0][1]} сделок · ${request_3[0][0]}\n👍: {likes}% 👎: {dislikes}%\n\n{word}: '
                                     f'{data['sum_crypt']} {cfg.coins_index[data['crypto']]}\nПлатите: {data['sum_fiat']} {cfg.bot_currency_2[data['fiat']]}'
                                     f'\n\n🕘 Ожидайте подтверждения сделки.\n\n⚠️ Продавец должен принять сделку в течение 10 минут, иначе она будет отменена.',
                                     reply_markup=builder_trade_active_2.as_markup())
    builder_trade_active = InlineKeyboardBuilder()
    builder_trade_active.button(
        text='Подтвердить сделку',
        callback_data=cl_m.Advertisements_p2p(action='p2p_active_trade_acc', value=f'{number}')
    )
    builder_trade_active.button(
        text='Отменить сделку',
        callback_data=cl_m.Advertisements_p2p(action='p2p_buy_cancel', value=f'{number}')
    )
    builder_trade_active.adjust(1)
    builder_trade_active.as_markup()
    await state.set_state(cl.Trade.id)
    await state.update_data(id=callback.from_user.id, id_vendor=request_2[0][1], number=number, number_adv=request[0][1])
    await bot.send_message(int(request_2[0][1]),f'У вас новый запрос по объявлению #{int(data['number'])} от пользователя {callback.from_user.id}\n\nПодтвердите или отмените сделку в течении 10 минут.', reply_markup=builder_trade_active.as_markup())
    await state.set_state(cl.Trade.chat_id)


@dp.callback_query(F.data == 'p2p_buy_create_fin')
async def p2p_buy_create(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    request = await read_db(f'p2p_advertisements WHERE number="{int(data['number'])}"', '*')
    request_2 = await read_db(f'users WHERE login="{str(request[0][2])}"', 'login, id')
    request_3 = await read_db(f'users_vendor WHERE id="{request[0][0]}"', 'sum, count, rep_plus, rep_minus')
    number = random.randint(10000, 9999999)
    if int(request_3[0][2]) == 0:
        likes = 0
    else:
        likes = (request_3[0][2] / (request_3[0][2] + request_3[0][3])) * 100
    if int(request_3[0][3]) == 0:
        dislikes = 0
    else:
        dislikes = (request_3[0][3] / (request_3[0][2] + request_3[0][3])) * 100
    builder_trade_active_2 = InlineKeyboardBuilder()
    builder_trade_active_2.button(
        text='Отменить сделку',
        callback_data=cl_m.Advertisements_p2p(action='p2p_buy_cancel', value=f'{number}')
    )
    builder_trade_active_2.button(
        text='К списку активных сделок',
        callback_data='p2p_active_trades'
    )
    builder_trade_active_2.adjust(1)
    builder_trade_active_2.as_markup()
    min = 60
    if int(request[0][10]) == 30 or int(request[0][10]) == 15:
        min = int(request[0][10])
    current_time = datetime.now() + timedelta(minutes=min)
    current_time = current_time.strftime('%Y-%m-%d %H:%M:%S')
    current_time2 = datetime.now() + timedelta(minutes=10)
    current_time2 = current_time2.strftime('%Y-%m-%d %H:%M:%S')
    await write_db(f"INSERT INTO active_transactions (number, sum, type_fiat, type_crypt, count, bank, login_customer, login_vendor, type, delete_at) VALUES ({number}, '{str(data['sum'])}', {int(data['fiat'])}, {int(data['crypto'])}, '{str(data['sum_crypt'])}', '{str(data['bank'])}', '{str(callback.from_user.username)}', '{str(request_2[0][0])}', 1, '{current_time2}')")
    await write_db(f"INSERT INTO freezing_of_funds (number, number_adv, login, login_vendor, {cfg.coins_index[int(data['crypto'])]}, time, delete_at) VALUES ({number}, {int(data['number'])}, '{str(callback.from_user.username)}', '{str(request_2[0][0])}' ,'{data['sum_crypt']}', {int(request[0][10])}, '{current_time}')")
    id = str(request[0][0])
    if int(request_3[0][1]) >= 3:
        id = str(request[0][0]) + '✅'
    await callback.message.edit_text(f'Сделка #D{number}\n\n👤 id{id}\n🏆 {request_3[0][1]} сделок · ${request_3[0][0]}\n👍: {likes}% 👎: {dislikes}%\n\nПокупаете: '
                                     f'{data['sum_crypt']} {cfg.coins_index[data['crypto']]}\nПлатите: {data['sum_fiat']} {cfg.bot_currency_2[data['fiat']]}'
                                     f'\n\n🕘 Ожидайте подтверждения сделки.\n\n⚠️ Продавец должен принять сделку в течение 10 минут, иначе она будет отменена.',
                                     reply_markup=builder_trade_active_2.as_markup())
    builder_trade_active = InlineKeyboardBuilder()
    builder_trade_active.button(
        text='Подтвердить сделку',
        callback_data=cl_m.Advertisements_p2p(action='p2p_active_trade_acc', value=f'{number}')
    )
    builder_trade_active.button(
        text='Отменить сделку',
        callback_data=cl_m.Advertisements_p2p(action='p2p_buy_cancel', value=f'{number}')
    )
    builder_trade_active.adjust(1)
    builder_trade_active.as_markup()
    await state.set_state(cl.Trade.id)
    await state.update_data(id=callback.from_user.id, id_vendor=request_2[0][1], number=number, number_adv=request[0][1])
    await bot.send_message(int(request_2[0][1]),f'У вас новый запрос по объявлению #{int(data['number'])} от пользователя {callback.from_user.id}\n\nПодтвердите или отмените сделку в течении 10 минут.', reply_markup=builder_trade_active.as_markup())
    await state.set_state(cl.Trade.chat_id)


@dp.callback_query(cl_m.Banks.filter(F.action.in_(['prev_avde', 'next_avde'])))
async def callback_query(callback: CallbackQuery, callback_data: cl_m.Banks, state: FSMContext):
    data = await state.update_data()
    page_num = int(callback_data.page)
    page = page_num - 1 if page_num > 0 else 0
    if callback_data.action == 'next_avde':
        page = page_num + 1 if page_num < (len(data['mass'])) else page_num
    mark = paginator_avde(data['mass'], 0, page)
    try:
        if data['edit']:
            mark = paginator_avde(data['mass'], 1, page)
    except:
        pass
    with suppress(TelegramBadRequest):
        await callback.message.edit_text(f'Объявления:', reply_markup=mark)
    await callback.answer()


@dp.callback_query(F.data == 'p2p_active_trades')
async def p2p_active_trades(callback: CallbackQuery, state: FSMContext):
    login = callback.from_user.username
    request = await read_db(f'freezing_of_funds WHERE "{login}" IN (login, login_vendor)', '*')
    count, count2, mass, mass2, mass3 = 0, 0, [], [], []
    word = 'Покупка'
    if request:
        for i in request:
            if str(request[count2][3]) == str(login):
                word = 'Продажа'
            if count >= 10:
                mass.append(mass2.copy())
                mass2.clear()
                count = 0
                mass2.append(InlineKeyboardButton(text=f'{word} #{request[count2][0]}',
                                                  callback_data=cl_m.Advertisements(action='select_adv3',
                                                                                   number=f'{request[count2][0]}').pack())),
            else:
                mass2.append(InlineKeyboardButton(text=f'{word} #{request[count2][0]}',
                                                  callback_data=cl_m.Advertisements(action='select_adv3',
                                                                                   number=f'{request[count2][0]}').pack()))
            word = 'Покупка'
            count += 1
            count2 += 1
        mass.append(mass2.copy())
        await state.set_state(cl.Announcement_pag.mass)
        await state.update_data(mass=mass)
        with suppress(TelegramBadRequest):
            await callback.message.edit_text(f'Ваши активные сделки:', reply_markup=paginator_avde(mass))
    else:
        await callback.message.edit_text(f'У вас нет активных сделок.', reply_markup=nav.inline_p2p_active_none_menu)


@dp.callback_query(F.data == 'p2p_withdrawn_adv_1')
async def p2p_active_trades(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await write_db(f"UPDATE p2p_advertisements SET status=1 WHERE number='{data['number']}'")
    await callback.answer(text=f'Объявление #{data['number']} находится на публикации')
    request = await read_db(f'p2p_advertisements WHERE number="{data['number']}"', '*')
    count = 1
    word = 'Продажа'
    if int(request[0][15]) == 1:
        word = 'Покупка'
    bank = ''
    banks = request[0][5].replace(',', '').split()
    status = '👌 Активно. Объявление показывается в общем списке.'
    status_mark = nav.inline_p2p_buy_curr_menu_3
    if int(request[0][17]) == 0:
        status = '😔 Неактивно. Объявление не показывается в общем списке.'
        status_mark = nav.inline_p2p_buy_curr_menu_3_1

    for i in banks:
        bank += str(count) + '.' + ' ' + str(cfg.banks[int(i)]) + '\n'
        count += 1
    if int(request[0][10]) == 60:
        time = '1 час'
    elif int(request[0][10]) == 30:
        time = '30 минут'
    else:
        time = '15 минут'
    conditions = 'не указаны.'
    if request[0][11] != '0':
        conditions = str(request[0][11])
    await callback.message.edit_text(
        f'🧾 Объявление #{request[0][1]}\n\n{word} {cfg.coins_index[int(request[0][6])]} за '
        f'{cfg.bot_currency_2[int(request[0][3])]}.\n\nЦена: {request[0][13]} '
        f'{cfg.bot_currency_2[int(request[0][3])]}\n\nОбщий объем: '
        f'{int(float(request[0][7]))} {cfg.coins_index[int(request[0][6])]}\nЛимиты: '
        f'{int(request[0][8])} {cfg.bot_currency_2[int(request[0][3])]} ~'
        f' {int(request[0][9])} {cfg.bot_currency_2[int(request[0][3])]}\n\n Способы '
        f'оплаты:\n{bank}\n\nСрок оплаты: {time}\n\nУсловия сделки: {conditions}\n\n{status}',
        reply_markup=status_mark)
    await callback.answer()


@dp.callback_query(F.data == 'back_adv_edit_2')
async def back_adv_edit_2(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    request = await read_db(f'p2p_advertisements WHERE number="{data['number']}"', '*')
    count = 1
    word = 'Продажа'
    if int(request[0][15]) == 1:
        word = 'Покупка'
    bank = ''
    banks = request[0][5].replace(',', '').split()
    status = '👌 Активно. Объявление показывается в общем списке.'
    status_mark = nav.inline_p2p_buy_curr_menu_3
    if int(request[0][17]) == 0:
        status = '😔 Неактивно. Объявление не показывается в общем списке.'
        status_mark = nav.inline_p2p_buy_curr_menu_3_1
    for i in banks:
        bank += str(count) + '.' + ' ' + str(cfg.banks[int(i)]) + '\n'
        count += 1
    if int(request[0][10]) == 60:
        time = '1 час'
    elif int(request[0][10]) == 30:
        time = '30 минут'
    else:
        time = '15 минут'
    conditions = 'не указаны.'
    if request[0][11] != '0':
        conditions = str(request[0][11])
    await callback.message.edit_text(
        f'🧾 Объявление #{request[0][1]}\n\n{word} {cfg.coins_index[int(request[0][6])]} за '
        f'{cfg.bot_currency_2[int(request[0][3])]}.\n\nЦена: {request[0][13]} '
        f'{cfg.bot_currency_2[int(request[0][3])]}\n\nОбщий объем: '
        f'{int(float(request[0][7]))} {cfg.coins_index[int(request[0][6])]}\nЛимиты: '
        f'{int(request[0][8])} {cfg.bot_currency_2[int(request[0][3])]} ~'
        f' {int(request[0][9])} {cfg.bot_currency_2[int(request[0][3])]}\n\n Способы '
        f'оплаты:\n{bank}\n\nСрок оплаты: {time}\n\nУсловия сделки: {conditions}\n\n{status}',
        reply_markup=status_mark)
    await callback.answer()


@dp.callback_query(cl_m.Advertisements.filter())
async def edit_adv(callback: CallbackQuery, callback_data: cl_m.Banks, state: FSMContext):
    text = callback_data.number
    await state.update_data(number=text)
    data = await state.get_data()
    request = await read_db(f'p2p_advertisements WHERE number="{data['number']}"', '*')
    count = 1
    word = 'Продажа'
    if int(request[0][15]) == 1:
        word = 'Покупка'
    bank = ''
    banks = request[0][5].replace(',', '').split()
    status = '👌 Активно. Объявление показывается в общем списке.'
    status_mark = nav.inline_p2p_buy_curr_menu_3
    if int(request[0][17]) == 0:
        status = '😔 Неактивно. Объявление не показывается в общем списке.'
        status_mark = nav.inline_p2p_buy_curr_menu_3_1
    for i in banks:
        bank += str(count) + '.' + ' ' + str(cfg.banks[int(i)]) + '\n'
        count += 1
    if int(request[0][10]) == 60:
        time = '1 час'
    elif int(request[0][10]) == 30:
        time = '30 минут'
    else:
        time = '15 минут'
    conditions = 'не указаны.'
    if request[0][11] != '0':
        conditions = str(request[0][11])
    await callback.message.edit_text(
        f'🧾 Объявление #{request[0][1]}\n\n{word} {cfg.coins_index[int(request[0][6])]} за '
        f'{cfg.bot_currency_2[int(request[0][3])]}.\n\nЦена: {request[0][13]} '
        f'{cfg.bot_currency_2[int(request[0][3])]}\n\nОбщий объем: '
        f'{int(float(request[0][7]))} {cfg.coins_index[int(request[0][6])]}\nЛимиты: '
        f'{int(request[0][8])} {cfg.bot_currency_2[int(request[0][3])]} ~'
        f' {int(request[0][9])} {cfg.bot_currency_2[int(request[0][3])]}\n\n Способы '
        f'оплаты:\n{bank}\n\nСрок оплаты: {time}\n\nУсловия сделки: {conditions}\n\n{status}',
        reply_markup=status_mark)
    await callback.answer()


@dp.callback_query(F.data == 'p2p_create')
async def p2p_create(callback: CallbackQuery, state: FSMContext):
    request = await read_db(f'users WHERE id={callback.from_user.id}', 'name')
    if str(request[0][0]) == '0':
        await callback.message.edit_text(f'Для создания объявлений необходимо пройти верификацию.'
                                         f'\nПройти ее можно нажав на кнопку "✅ Верификация" ниже.')
    else:
        await callback.message.edit_text(
            f'Новое объявление', reply_markup=nav.inline_p2p_create_advertisements_menu)

@dp.callback_query(F.data == 'p2p_create_buy')
async def p2p_cteate_buy(callback: CallbackQuery, state: FSMContext):
    await state.set_state(cl.Buy_p2p.type)
    await state.update_data(type='buy')
    await callback.message.edit_text(
        f'Какую криптовалюту?', reply_markup=nav.builder_advertisements_p2p.as_markup())
    await state.set_state(cl.Buy_p2p.crypt)


@dp.callback_query(F.data == 'p2p_create_sell')
async def p2p_cteate_buy(callback: CallbackQuery, state: FSMContext):
    await state.set_state(cl.Buy_p2p.type)
    await state.update_data(type='sell')
    await callback.message.edit_text(
        f'Какую криптовалюту?', reply_markup=nav.builder_advertisements_p2p.as_markup())
    await state.set_state(cl.Buy_p2p.crypt)


@dp.callback_query(F.data == 'p2p_rep_plus')
async def p2p_rep_plus(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await write_db(f"UPDATE users_vendor SET rep_plus=rep_plus+1 WHERE id={data['id_vendor']}")
    await callback.message.edit_text(f'Спасибо!')


@dp.callback_query(F.data == 'p2p_rep_minus')
async def p2p_rep_minus(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await write_db(f"UPDATE users_vendor SET rep_minus=rep_minus+1 WHERE id={data['id_vendor']}")
    await callback.message.edit_text(f'Спасибо!')


@dp.callback_query(F.data == 'p2p_time_edit')
async def p2p_time_edit(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    request_rate = await read_db(f'p2p_advertisements WHERE number="{data['number']}" ','time')
    time = request_rate[0][0]
    match time:
        case 15:
            time = '15 минут'
        case 30:
            time = '30 минут'
        case 60:
            time = '1 час'
    with suppress(TelegramBadRequest):
        await callback.message.edit_text(f'Выберите количество времени, в течение которого должна быть отправлена '
                                         f'оплата.\nСейчас установлено время: {time}', reply_markup=nav.builder_time_edit.as_markup())


@dp.callback_query(F.data == 'p2p_create_sum')
async def p2p_banks_edit(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await state.set_state(cl.Buyp2p.filter)
    await callback.message.edit_text(f'Вы можете указать сумму в RUB, чтобы отфильтровать список доступных объявлений.'
                                     , reply_markup=nav.inline_p2p_filter_back_menu)


@dp.message(cl.Buyp2p.filter)
async def trade_crypt(message: types.Message, state: FSMContext):
    data = await state.update_data()
    try:
        text = float((message.text).replace(',', '.'))
        await state.update_data(filter=text)
        filter = InlineKeyboardButton(
            text=f'{text} {cfg.bot_currency_2[int(data['fiat'])]} или более',
            callback_data='bank_filter'
        )
        res_filter = InlineKeyboardButton(
            text='Сбросить фильтр',
            callback_data='p2p_bank_2'
        )
        inline_filter_main = [[filter], [res_filter]]
        inline_filter_main_menu = InlineKeyboardMarkup(inline_keyboard=inline_filter_main)
        await bot.send_message(message.chat.id,
                               f'Здесь вы можете купить {cfg.coins_index[int(data['crypto'])]} за {cfg.bot_currency_2[int(data['fiat'])]} через {cfg.banks[int(data['bank'])]}.'
                               , reply_markup=inline_filter_main_menu)
    except:
        await state.set_state(cl.Buyp2p.filter)
        await bot.send_message(message.chat.id,
            f'Вы можете указать сумму в RUB, чтобы отфильтровать список доступных объявлений.'
            , reply_markup=nav.inline_p2p_filter_back_menu)


@dp.callback_query(F.data == 'bank_filter')
async def bank_filter(callback: CallbackQuery, state: FSMContext):
    data = await state.update_data()
    type = '1'
    if int(data['type']) == 1:
        type = '0'
    request = await read_db(
        f"p2p_advertisements WHERE currency='{data['fiat']}' && crypt='{data['crypto']}' && type='{type}' && banks LIKE '%{data['bank']}%' && sum>={float(data['filter'])}",
        '*')
    count, count2, mass, mass2 = 0, 0, [], []
    for i in request:
        word = 'продаже'
        if count >= 10:
            if int(request[count2][15]) == 1:
                word = 'покупке'
            mass.append(mass2.copy())
            mass2.clear()
            count = 0
            mass2.append(InlineKeyboardButton(
                text=f'{request[count2][14]}  · {request[count2][8]} - {request[count2][9]}   id{request[count2][0]}',
                callback_data=cl_m.Advertisements(action='select_adv',
                                                  number=f'{request[count2][1]}').pack())),
        else:
            if int(request[count2][15]) == 1:
                word = 'покупке'
            mass2.append(InlineKeyboardButton(
                text=f'{request[count2][14]}  · {request[count2][8]} - {request[count2][9]}   id{request[count2][0]}',
                callback_data=cl_m.Advertisements(action='select_adv',
                                                  number=f'{request[count2][1]}').pack()))
        count += 1
        count2 += 1
    mass.append(mass2.copy())
    await state.update_data(mass=mass)
    word = 'купить'
    await state.update_data(edit=1)
    if data['type'] == 0:
        word = 'продать'
    await callback.message.edit_text(f'Здесь вы можете {word} {cfg.coins_index[int(data['crypto'])]} за '
                                     f'{cfg.bot_currency_2[int(data['fiat'])]} через {cfg.banks[int(data['bank'])]}.',
                                     reply_markup=paginator_avde(mass, 1))


@dp.callback_query(F.data == 'p2p_bank_2')
async def bank_2(callback: CallbackQuery, state: FSMContext):
    data = await state.update_data()
    type = '1'
    if int(data['type']) == 1:
        type = '0'
    request = await read_db(
        f"p2p_advertisements WHERE currency='{data['fiat']}' && crypt='{data['crypto']}' && type='{type}' && banks LIKE '%{data['bank']}%'",
        '*')
    count, count2, mass, mass2 = 0, 0, [], []
    for i in request:
        word = 'продаже'
        if count >= 10:
            if int(request[count2][15]) == 1:
                word = 'покупке'
            mass.append(mass2.copy())
            mass2.clear()
            count = 0
            mass2.append(InlineKeyboardButton(
                text=f'{request[count2][14]}  · {request[count2][8]} - {request[count2][9]}   id{request[count2][0]}',
                callback_data=cl_m.Advertisements(action='select_adv',
                                                  number=f'{request[count2][1]}').pack())),
        else:
            if int(request[count2][15]) == 1:
                word = 'покупке'
            mass2.append(InlineKeyboardButton(
                text=f'{request[count2][14]}  · {request[count2][8]} - {request[count2][9]}   id{request[count2][0]}',
                callback_data=cl_m.Advertisements(action='select_adv',
                                                  number=f'{request[count2][1]}').pack()))
        count += 1
        count2 += 1
    mass.append(mass2.copy())
    await state.update_data(mass=mass)
    word = 'купить'
    await state.update_data(edit=1)
    if data['type'] == 0:
        word = 'продать'
    await callback.message.edit_text(f'Здесь вы можете {word} {cfg.coins_index[int(data['crypto'])]} за '
                                     f'{cfg.bot_currency_2[int(data['fiat'])]} через {cfg.banks[int(data['bank'])]}.',
                                     reply_markup=paginator_avde(mass, 1))


@dp.callback_query(F.data == 'p2p_banks_edit')
async def p2p_banks_edit(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    request = await read_db(f'p2p_advertisements WHERE number="{data['number']}"', 'banks')
    banks = request[0][0].replace(',', '').split()
    bank = ''
    count = 1
    for i in banks:
        bank += str(count) + '.' + ' ' + str(cfg.banks[int(i)]) + '\n'
        count += 1
    with suppress(TelegramBadRequest):
        await callback.message.edit_text(f'Выберите от 1 до 10 способов оплаты, которые вы хотите использовать в объявлении.\n{bank}', reply_markup=paginator(nav.banks_2, 1))


@dp.callback_query(cl_m.Buy_time_edit.filter())
async def p2p_time_edit_f(callback: CallbackQuery, callback_data: cl_m.Buy_time_edit, state: FSMContext):
    text = callback_data.time
    data = await state.get_data()
    await write_db(f"UPDATE p2p_advertisements SET time={text} WHERE number='{data['number']}'")
    time = ''
    match text:
        case 15:
            time = '15 минут'
        case 30:
            time = '30 минут'
        case 60:
            time = '1 час'
    await callback.message.edit_text(f'Выберите количество времени, в течение которого должна быть отправлена '
                                     f'оплата.\nСейчас установлено время: {time}', reply_markup=nav.builder_time_edit.as_markup())


@dp.callback_query(cl_m.Advertisements_p2p.filter())
async def p2p_create_buy_crypt(callback: CallbackQuery, callback_data: cl_m.Advertisements_p2p, state: FSMContext):
    type = callback_data.value
    if callback_data.action == 'select_balance_currency':
        await state.update_data(crypt=type)
        await state.update_data(banks=[])
        with suppress(TelegramBadRequest):
            await callback.message.edit_text(
                f'Выберите валюту?', reply_markup=nav.builder_adv_p2p_fiat.as_markup())
        await state.set_state(cl.Buy_p2p.count)
    elif callback_data.action == 'select_balance_currency_2':
        text = callback_data.value
        await state.update_data(crypto=int(text))
        await callback.message.edit_text(f'Выберите валюту.', reply_markup=nav.builder_buy_p2p_fiat.as_markup())
    elif callback_data.action == 'select_balance_currency_3':
        text = callback_data.value
        await state.update_data(fiat=int(text))
        data = await state.get_data()
        word = 'покупки'
        if data['type'] == 0:
            word = 'продажи'
        await callback.message.edit_text(f'Выберите способ оплаты для {word} криптовалюты за {cfg.bot_currency_2[int(data['fiat'])]}.', reply_markup=paginator_2(nav.banks_3))
    elif callback_data.action == 'p2p_buy_cancel':
        data = callback_data.value
        request = await read_db(f'freezing_of_funds WHERE number="{int(data)}"', 'login')
        request_2 = await read_db(f'users WHERE login="{request[0][0]}"', 'id')
        await bot.send_message(int(request_2[0][0]), f'Сделка #D{data} была отменена.')
        await write_db(f"DELETE FROM freezing_of_funds WHERE number={data}")
        await write_db(f"DELETE FROM p2p_advertisements WHERE number={data}")
        await callback.message.edit_text(f'Сделка #D{data} успешно отменена')
        await state.clear()
    elif callback_data.action == 'p2p_active_trade_acc':
        await state.set_state(cl.Trade.id)
        data = callback_data.value
        request = await read_db(f'freezing_of_funds WHERE number="{int(data)}"', 'login, number_adv')
        request_2 = await read_db(f'p2p_advertisements WHERE number="{int(data)}"', 'conditions, currency, crypt, sum, type')
        request_3 = await read_db(f'users WHERE login="{request[0][0]}"', f'id, name')
        request_4 = await read_db(f'freezing_of_funds WHERE number="{int(data)}"', f'{cfg.coins_index[int(request_2[0][2])]}')
        await state.update_data(id = request_3[0][0], id_vendor=callback.from_user.id, number = data, number_adv = request[0][1] )
        if request_2[0][4] == 0:
            await bot.send_message(int(request_3[0][0]), f'Сделка #D{data} была подтверждена id{callback.from_user.id}.'
                                                         f'\n\nОтправьте {float(request_2[0][3]) * float(request_4[0][0])} '
                                                         f'{cfg.bot_currency_2[int(request_2[0][1])]} по реквизитам из условий объявления и отправьте чек в этот чат.\n\nУсловия объявления: {request_2[0][0]}')
            await callback.message.edit_text(f'Сделка #D{data} принята, ожидайте чек.\n\nВнимание! Данные в чеке должны совпадать с данными покупателя!\n\nДанные покупателя: {request_3[0][1]}')
        elif request_2[0][4] == 1:
            await bot.send_message(int(request_3[0][0]), f'Сделка #D{data} была подтверждена id{callback.from_user.id}.\n\nОтправьте ваши реквизиты в этот чат, продавец переведет по ним деньги.\n\nУсловия объявления: {request_2[0][0]}\n\nВнимание! Данные в чеке должны совпадать с данными продавца!\n\nДанные продавца: {request_3[0][1]}')
            await callback.message.edit_text(f'Сделка #D{data} принята. Сейчас в этом чате вам придут реквизиты покупателя, отправьте по ним {float(request_2[0][3]) * float(request_4[0][0])} {cfg.bot_currency_2[int(request_2[0][1])]} и прикрепите чек в этот чат.')
    elif callback_data.action == 'p2p_trade_fin':
        data = await state.get_data()
        number = callback_data.value
        request = await read_db(f'p2p_advertisements WHERE number={data['number_adv']}', 'login, currency, crypt, type, sum')
        request_2 = await read_db(f'freezing_of_funds WHERE number={int(data['number'])}', f'login, {cfg.coins_index[int(request[0][2])]}, login_vendor')
        if int(request[0][3]) == 1:
            await write_db(f"UPDATE p2p_advertisements SET crypt_count=crypt_count - {request_2[0][1]} WHERE number={int(data['number_adv'])}")
            await write_db(f"UPDATE users_purses SET {cfg.coins_index[int(request[0][2])]}={cfg.coins_index[int(request[0][2])]} + {request_2[0][1]} WHERE login='{request[0][0]}'")
            await write_db(f"UPDATE users_purses SET {cfg.coins_index[int(request[0][2])]}={cfg.coins_index[int(request[0][2])]} - {request_2[0][1]} WHERE login='{request_2[0][0]}'")
            request_3 = await read_db(f'exchange_rates WHERE currency_2="{cfg.bot_currency_2[int(request[0][1])]}" && currency_1 = "USDT"', 'rate')
            await write_db(f"UPDATE users_vendor SET count=count+1, sum=sum+{float(request[0][4]) * float(request_2[0][1]) / float(request_3[0][0])} WHERE login='{request_2[0][2]}'")
            request_4 = await read_db(f'p2p_advertisements WHERE number={data['number_adv']}', 'sum')
            if int(request_4[0][0]) == 0:
                await write_db(f"DELETE FROM p2p_advertisements WHERE number={data['number_adv']}")
            await write_db(f"DELETE FROM freezing_of_funds WHERE number={number}")
            with suppress(TelegramBadRequest):
                await bot.send_message(int(data['id_vendor']),f'Оплата подтверждена !\n\nСредства автоматически начисленны вам на баланс.\n\nСпасибо, что пользуетесь нашей P2P платформой ! ❤️')
                await bot.send_message(int(data['id']),f'Оплата подтверждена !\n\nСредства автоматически начисленны на баланс покупателя.\n\nСпасибо, что пользуетесь нашей P2P платформой ! ❤️')
                await bot.send_message(int(data['id']), f'Пожалуйста, оцените продавца.',reply_markup=nav.inline_p2p_rep_menu)
        elif int(request[0][3]) == 0:
                await write_db(f"UPDATE p2p_advertisements SET crypt_count=crypt_count - {request_2[0][1]} WHERE number={int(data['number_adv'])}")
                await write_db(f"UPDATE users_purses SET {cfg.coins_index[int(request[0][2])]}={cfg.coins_index[int(request[0][2])]} - {request_2[0][1]} WHERE login='{request[0][0]}'")
                await write_db(f"UPDATE users_purses SET {cfg.coins_index[int(request[0][2])]}={cfg.coins_index[int(request[0][2])]} + {request_2[0][1]} WHERE login='{request_2[0][0]}'")
                request_3 = await read_db(f'exchange_rates WHERE currency_2="{cfg.bot_currency_2[int(request[0][1])]}" && currency_1 = "USDT"','rate')
                await write_db(f"UPDATE users_vendor SET count=count+1, sum=sum+{float(request[0][4]) * float(request_2[0][1]) / float(request_3[0][0])} WHERE login='{request_2[0][2]}'")
                request_4 = await read_db(f'p2p_advertisements WHERE number={data['number_adv']}','sum')
                if int(request_4[0][0]) == 0:
                    await write_db(f"DELETE FROM p2p_advertisements WHERE number={data['number_adv']}")
                await write_db(f"DELETE FROM freezing_of_funds WHERE number={number}")
                with suppress(TelegramBadRequest):
                    await bot.send_message(int(data['id_vendor']),f'Оплата подтверждена !\n\nСредства автоматически начисленны на баланс покупателя.\n\nСпасибо, что пользуетесь нашей P2P платформой ! ❤️')
                    await bot.send_message(int(data['id']),f'Оплата подтверждена продавцом!\n\nСредства автоматически начисленны вам на баланс.\n\nСпасибо, что пользуетесь нашей P2P платформой ! ❤️')
                    await bot.send_message(int(data['id']),f'Пожалуйста, оцените продавца.', reply_markup=nav.inline_p2p_rep_menu)
    elif callback_data.action == 'p2p_support':
        data = await state.get_data()
        number_tik = random.randint(10000, 9999999)
        number, number_adv, id, id_vendor = data['number'], data['number_adv'], data['id'], data['id_vendor']
        await state.set_state(cl.Ticket.number)
        await state.update_data(number=number, number_adv=number_adv, id=id, id_vendor=id_vendor, number_tik=number)
        await bot.send_message(callback.from_user.id,
                               f'Номер вашего обращения #{number_tik}\n\nОпишите вашу проблему в одном сообщении.')
        await state.set_state(cl.Ticket.text)

@dp.callback_query(cl_m.Banks.filter(F.action.in_(['prev_adv', 'next_adv'])))
async def callback_query(callback: CallbackQuery, callback_data: cl_m.Banks, state: FSMContext):
    data = await state.update_data()
    request = await read_db(f'p2p_advertisements WHERE number={data['number']}', 'banks')
    banks = request[0][0].replace(',','').split()
    bank = ''
    count = 1
    for i in banks:
        bank += str(count) + '.' + ' ' + str(cfg.banks[int(i)]) + '\n'
        count += 1
    page_num = int(callback_data.page)
    page = page_num - 1 if page_num > 0 else 0
    if callback_data.action == 'next_adv':
        page = page_num + 1 if page_num < len(nav.banks_2) else page_num
    with suppress(TelegramBadRequest):
        await callback.message.edit_text(
            f'Выберите от 1 до 10 способов оплаты, которые вы хотите использовать в объявлении.\n{bank}',
            reply_markup=paginator(nav.banks_2, 1, page))
    await callback.answer()


@dp.callback_query(cl_m.Banks.filter(F.action.in_(['prev_2', 'next_2'])))
async def callback_query(callback: CallbackQuery, callback_data: cl_m.Banks, state: FSMContext):
    data = await state.update_data()
    word = 'покупки'
    if data['type'] == 0:
        word = 'продажи'
    count = 1
    page_num = int(callback_data.page)
    page = page_num - 1 if page_num > 0 else 0
    if callback_data.action == 'next_2':
        page = page_num + 1 if page_num < len(nav.banks_3) else page_num
    with suppress(TelegramBadRequest):
        await callback.message.edit_text(f'Выберите способ оплаты для {word} криптовалюты за {cfg.bot_currency_2[int(data['fiat'])]}.', reply_markup=paginator_2(nav.banks_3, page))
    await callback.answer()


@dp.callback_query(cl_m.Banks.filter(F.action.in_(['prev', 'next'])))
async def callback_query(callback: CallbackQuery, callback_data: cl_m.Banks, state: FSMContext):
    data = await state.update_data()
    bank = ''
    count = 1
    for i in data['banks']:
        bank += str(count) + '.' + ' ' + str(cfg.banks[i]) + '\n'
        count += 1
    page_num = int(callback_data.page)
    page = page_num - 1 if page_num > 0 else 0
    if callback_data.action == 'next':
        page = page_num + 1 if page_num < len(nav.banks) else page_num
    with suppress(TelegramBadRequest):
        await callback.message.edit_text(f'Выберите от 1 до 10 способов оплаты, которые вы хотите использовать в объявлении.\n{bank}', reply_markup=paginator(nav.banks, 0, page))
    await callback.answer()


@dp.callback_query(cl_m.Advertisements_p2p_fiat.filter())
async def p2p_create_buy_fiat(callback: CallbackQuery, callback_data: cl_m.Coins, state: FSMContext):
    type = callback_data.value
    await state.update_data(currency=type)
    await callback.message.edit_text(f'Выберите от 1 до 10 способов оплаты, которые вы хотите использовать в объявлении.', reply_markup=paginator(nav.banks, 0))


@dp.callback_query(cl_m.Banks.filter())
async def p2p_cteate_buy_p2p_bank(callback: CallbackQuery, callback_data: cl_m.Banks, state: FSMContext):
    data = await state.update_data()
    if callback_data.action == 'select_bank_1':
        item = int(callback_data.value)
        banks = data['banks']
        if item in banks:
            await callback.answer(text='Данный банк уже есть в списке')
        else:
            banks.append(item)
            await state.update_data(banks=banks)
            data = await state.update_data()
        bank = ''
        count = 1
        for i in data['banks']:
            bank += str(count) + '.' + ' ' + str(cfg.banks[i]) + '\n'
            count += 1
        if len(data['banks']) == 10:
            builder_2 = InlineKeyboardBuilder()
            builder_2.row(
                InlineKeyboardButton(text='◀️ Назад',callback_data='p2p_create_buy_crypt'),
                InlineKeyboardButton(text='Продолжить',callback_data='p2p_create_buy_course'),
                width=2
            )
            await callback.message.edit_text(f'Вы выбрали максимальное количество банков. Нажмите "Продолжить" или "Назад"\n{bank}',reply_markup=builder_2.as_markup())
        elif len(data['banks']) <= 9:
            with suppress(TelegramBadRequest):
                await callback.message.edit_text(
                    f'Выберите от 1 до 10 способов оплаты, которые вы хотите использовать в объявлении.\n{bank}',
                    reply_markup=paginator(nav.banks, 0))
    elif callback_data.action == 'select_bank_2':
        item = str(callback_data.value)
        data = await state.get_data()
        request = await read_db(f'p2p_advertisements WHERE number="{data['number']}"','banks')
        banks = []
        banks = request[0][0].replace(',', '').split()
        bank_list = ''
        if item in banks:
            if len(banks) <= 1:
                await callback.answer(text='Вы не можете убрать из списка единственный банк')
            else:
                await callback.answer(text='Банк удален из списка')
                banks.remove(item)
                for i in banks:
                    bank_list += str(i) + ', '
                await write_db(f"UPDATE p2p_advertisements SET banks='{bank_list}' WHERE number={data['number']}")
        else:
            banks.append(item)
            for i in banks:
                bank_list += str(i) + ', '
            await write_db(f"UPDATE p2p_advertisements SET banks='{bank_list}' WHERE number={data['number']}")
        bank = ''
        count = 1
        if len(banks) >= 1:
            for i in banks:
                bank += str(count) + '. '+ str(cfg.banks[int(i)]) + '\n'
                count += 1
        if len(banks) == 10:
            builder_2 = InlineKeyboardBuilder()
            builder_2.row(
        InlineKeyboardButton(text='◀️ Назад', callback_data='p2p_create_buy_crypt'),
                InlineKeyboardButton(text='Продолжить', callback_data='p2p_create_buy_course'),
                width=2
                )
            await callback.message.edit_text(f'Вы выбрали максимальное количество банков. Нажмите "Продолжить", "Назад" или удалите один из банков.\n{bank}', reply_markup=paginator(nav.banks_2, 1))
        elif len(banks) <= 9:
            with suppress(TelegramBadRequest):
                await callback.message.edit_text(f'Выберите от 1 до 10 способов оплаты, которые вы хотите использовать в объявлении.\n{bank}', reply_markup=paginator(nav.banks_2, 1))
    elif callback_data.action == 'select_bank_3':
        item = str(callback_data.value)
        await state.update_data(bank=item)
        data = await state.update_data()
        type = '1'
        if int(data['type']) == 1:
            type = '0'
        request = await read_db(
            f"p2p_advertisements WHERE currency='{data['fiat']}' && crypt='{data['crypto']}' && type='{type}' && banks LIKE '%{data['bank']}%'", '*')
        count, count2, mass, mass2 = 0, 0, [], []
        for i in request:
            word = 'продаже'
            if count >= 10:
                if int(request[count2][15]) == 1:
                    word = 'покупке'
                mass.append(mass2.copy())
                mass2.clear()
                count = 0
                mass2.append(InlineKeyboardButton(text=f'{request[count2][14]}  · {request[count2][8]} - {request[count2][9]}   id{request[count2][0]}',
                                                  callback_data=cl_m.Advertisements(action='select_adv',
                                                                                   number=f'{request[count2][1]}').pack())),
            else:
                if int(request[count2][15]) == 1:
                    word = 'покупке'
                mass2.append(InlineKeyboardButton(text=f'{request[count2][14]}  · {request[count2][8]} - {request[count2][9]}   id{request[count2][0]}',
                                                  callback_data=cl_m.Advertisements(action='select_adv',
                                                                                   number=f'{request[count2][1]}').pack()))
            count += 1
            count2 += 1
        mass.append(mass2.copy())
        await state.update_data(mass=mass)
        word = 'купить'
        await state.update_data(edit=1)
        if data['type'] == 0:
            word = 'продать'
        await callback.message.edit_text(f'Здесь вы можете {word} {cfg.coins_index[int(data['crypto'])]} за '
                                         f'{cfg.bot_currency_2[int(data['fiat'])]} через {cfg.banks[int(item)]}.',
                                         reply_markup=paginator_avde(mass, 1))
    elif callback_data.action == 'p2p_create_buy_course':
        data = await state.update_data()
        request_rate = await read_db(
            f'exchange_rates WHERE currency_1="{cfg.coins_index[int(data['crypt'])]}" && currency_2="{cfg.bot_currency_2[int(data['currency'])]}"',
            'rate, minimum_exchange_amount')
        await state.update_data(course=request_rate[0][0])
        if data['type'] == 'buy':
            await callback.message.edit_text(
                f'Пришлите фиксированную цену в {cfg.bot_currency_2[int(data['currency'])]} для покупки {cfg.coins_index[int(data['crypt'])]}.\n\nБиржевой курс: {request_rate[0][0]} {cfg.bot_currency_2[int(data['currency'])]}\n\nЦена за 1 {cfg.coins_index[int(data['crypt'])]} = {request_rate[0][0]} {cfg.bot_currency_2[int(data['currency'])]}\n\n{'-'*60}\n⚠️ В цене объявления должны быть учтены все возможные комиссии платёжных систем. Правилами сервиса запрещено взимать дополнительные комиссии с пользователей - покупатели должны переводить точную сумму сделки.\n{'-'*60}', reply_markup=nav.inline_p2p_bank_2_fix_menu)
        elif data['type'] == 'sell':
            await callback.message.edit_text(
                f'Пришлите фиксированную цену в {cfg.bot_currency_2[int(data['currency'])]} для продажи {cfg.coins_index[int(data['crypt'])]}.\n\nБиржевой курс: {request_rate[0][0]} {cfg.bot_currency_2[int(data['currency'])]}\n\nЦена за 1 {cfg.coins_index[int(data['crypt'])]} = {request_rate[0][0]} {cfg.bot_currency_2[int(data['currency'])]}\n\n{'-' * 60}\n⚠️ В цене объявления должны быть учтены все возможные комиссии платёжных систем. Правилами сервиса запрещено взимать дополнительные комиссии с пользователей - покупатели должны переводить точную сумму сделки.\n{'-' * 60}',
                reply_markup=nav.inline_p2p_bank_2_fix_menu)
        await state.set_state(cl.Buy_p2p.fix_count_sell)


@dp.callback_query(F.data == 'p2p_create_buy_course')
async def p2p_cteate_buy_p2p_bank_tinkoff(callback: CallbackQuery, state: FSMContext):
    data = await state.update_data()
    request_rate = await read_db(
        f'exchange_rates WHERE currency_1="{cfg.coins_index[int(data['crypt'])]}" && currency_2="{cfg.bot_currency_2[int(data['currency'])]}"',
        'rate, minimum_exchange_amount')
    await state.update_data(course=request_rate[0][0])
    if data['type'] == 'buy':
        await callback.message.edit_text(
            f'Пришлите фиксированную цену в {cfg.bot_currency_2[int(data['currency'])]} для покупки {cfg.coins_index[int(data['crypt'])]}.\n\nБиржевой курс: {request_rate[0][0]} {cfg.bot_currency_2[int(data['currency'])]}\n\nЦена за 1 {cfg.coins_index[int(data['crypt'])]} = {request_rate[0][0]} {cfg.bot_currency_2[int(data['currency'])]}\n\n{'-' * 60}\n⚠️ В цене объявления должны быть учтены все возможные комиссии платёжных систем. Правилами сервиса запрещено взимать дополнительные комиссии с пользователей - покупатели должны переводить точную сумму сделки.\n{'-' * 60}',
            reply_markup=nav.inline_p2p_bank_2_fix_menu)
    elif data['type'] == 'sell':
        await callback.message.edit_text(
            f'Пришлите фиксированную цену в {cfg.bot_currency_2[int(data['currency'])]} для продажи {cfg.coins_index[int(data['crypt'])]}.\n\nБиржевой курс: {request_rate[0][0]} {cfg.bot_currency_2[int(data['currency'])]}\n\nЦена за 1 {cfg.coins_index[int(data['crypt'])]} = {request_rate[0][0]} {cfg.bot_currency_2[int(data['currency'])]}\n\n{'-' * 60}\n⚠️ В цене объявления должны быть учтены все возможные комиссии платёжных систем. Правилами сервиса запрещено взимать дополнительные комиссии с пользователей - покупатели должны переводить точную сумму сделки.\n{'-' * 60}',
            reply_markup=nav.inline_p2p_bank_2_fix_menu)
    await state.set_state(cl.Buy_p2p.fix_count_sell)


@dp.callback_query(F.data == 'p2p_bank_fix')
async def p2p_cteate_buy_p2p_bank_tinkoff(callback: CallbackQuery, state: FSMContext):
    data = await state.update_data()
    if data['type'] == 'buy':
        with suppress(TelegramBadRequest):
            await callback.message.edit_text(
                f'Отправьте фиксированную цену в {cfg.bot_currency_2[int(data['currency'])]} для покупки {cfg.coins_index[int(data['crypt'])]}.\n\nБиржевой курс: {float(data['course'])} {cfg.bot_currency_2[int(data['currency'])]}\n\nЦена за 1 {cfg.coins_index[int(data['crypt'])]} = {float(data['course'])} {cfg.bot_currency_2[int(data['currency'])]}\n\n{'-'*60}\n⚠️ В цене объявления должны быть учтены все возможные комиссии платёжных систем. Правилами сервиса запрещено взимать дополнительные комиссии с пользователей - покупатели должны переводить точную сумму сделки.\n{'-'*60}', reply_markup=nav.inline_p2p_bank_2_fix_menu)
    elif data['type'] == 'sell':
        with suppress(TelegramBadRequest):
            await callback.message.edit_text(
                f'Отправьте фиксированную цену в {cfg.bot_currency_2[int(data['currency'])]} для продажи {cfg.coins_index[int(data['crypt'])]}.\n\nБиржевой курс: {float(data['course'])} {cfg.bot_currency_2[int(data['currency'])]}\n\nЦена за 1 {cfg.coins_index[int(data['crypt'])]} = {float(data['course'])} {cfg.bot_currency_2[int(data['currency'])]}\n\n{'-' * 60}\n⚠️ В цене объявления должны быть учтены все возможные комиссии платёжных систем. Правилами сервиса запрещено взимать дополнительные комиссии с пользователей - покупатели должны переводить точную сумму сделки.\n{'-' * 60}',
                reply_markup=nav.inline_p2p_bank_2_fix_menu)
    await state.set_state(cl.Buy_p2p.fix_count_sell)

@dp.callback_query(F.data == 'p2p_bank_floating')
async def p2p_cteate_buy_p2p_bank_tinkoff(callback: CallbackQuery, state: FSMContext):
    data = await state.update_data()
    if data['type'] == 'buy':
        with suppress(TelegramBadRequest):
            await callback.message.edit_text(
            f'Отправьте процент от биржевого курса для покупки {cfg.coins_index[int(data['crypt'])]}.\n(например, +4% или -2.5%)\n\nБиржевой курс: {float(data['course'])} {cfg.bot_currency_2[int(data['currency'])]}\n\nЦена за 1 {cfg.coins_index[int(data['crypt'])]} = {float(data['course'])} {cfg.bot_currency_2[int(data['currency'])]}\n\n{'-'*60}\n⚠️ В курсе объявления должны быть учтены все возможные комиссии платёжных систем. Правилами сервиса запрещено взимать дополнительные комиссии с пользователей - покупатели должны переводить точную сумму сделки.\n{'-'*60}',
                reply_markup=nav.inline_p2p_bank_2_floating_menu)
    elif data['type'] == 'sell':
        with suppress(TelegramBadRequest):
            await callback.message.edit_text(
                f'Отправьте процент от биржевого курса для продажи {cfg.coins_index[int(data['crypt'])]}.\n\nБиржевой курс: {float(data['course'])} {cfg.bot_currency_2[int(data['currency'])]}\n\nЦена за 1 {cfg.coins_index[int(data['crypt'])]} = {float(data['course'])} {cfg.bot_currency_2[int(data['currency'])]}\n\n{'-' * 60}\n⚠️ В цене объявления должны быть учтены все возможные комиссии платёжных систем. Правилами сервиса запрещено взимать дополнительные комиссии с пользователей - покупатели должны переводить точную сумму сделки.\n{'-' * 60}',
                reply_markup=nav.inline_p2p_bank_2_floating_menu)
    await state.set_state(cl.Buy_p2p.percentage)

@dp.callback_query(F.data == 'p2p_bank_next')
async def p2p_cteate_buy_p2p_bank_next(callback: CallbackQuery, state: FSMContext):
    data = await state.update_data()
    if data['type'] == 'buy':
        word = 'купить'
    else:
        word = 'продать'
    await callback.message.edit_text(
        f'Отправьте объем {cfg.coins_index[int(data['crypt'])]}, который хотите {word}.',
        reply_markup=nav.inline_p2p_bank_2_2_menu)
    await state.set_state(cl.Buy_p2p.crypt_count)


@dp.message(cl.Buy_p2p.crypt_count)
async def trade_crypt(message: types.Message, state: FSMContext):
    data = await state.update_data()
    request = await read_db(f'users_purses WHERE id="{message.from_user.id}"', f'{cfg.coins_index[int(data['crypt'])]}')
    try:
        type = float((message.text).replace(',', '.'))
    except:
        type = float(message.text)
    if data['type'] == 'buy':
        word = 'купить'
    else:
        word = 'продать'
    await state.update_data(crypt_count=type)
    data = await state.update_data()
    if data['fix_count_sell'] is None:
        count = type * (float(data['course']) + (float(data['course']) * float(data['percentage'] / 100)))
    else:
        count = type * float(data['fix_count_sell'])
    if int(type) > float(request[0][0]) and data['type'] == 'sell':
        await bot.send_message(message.chat.id,
            f'Отправьте объем {cfg.coins_index[int(data['crypt'])]}, который хотите {word}.\n\nСумма продажи должна быть меньше суммы на вашем кошельке.',
            reply_markup=nav.inline_p2p_bank_2_2_menu)
        await state.set_state(cl.Buy_p2p.crypt_count)
    else:
        await bot.send_message(message.chat.id, f'Отправьте лимиты сделки в {cfg.bot_currency_2[int(data['currency'])]} '
                                                f'через дефис, которые определяют минимальную и максимальную сумму одной '
                                                f'сделки (например, 600-9575.35 или 600-30000000).\n\nТекущий объем:'
                                                f' {data['crypt_count']} {cfg.coins_index[int(data['crypt'])]}   {count}'
                                                f' {cfg.bot_currency_2[int(data['currency'])]}')
        await state.set_state(cl.Buy_p2p.crypt_min)


@dp.message(cl.Buy_p2p.crypt_min)
async def buy_p2p_crypt_min_max(message: types.Message, state: FSMContext):
    type_curr = (message.text).split("-")
    await state.update_data(crypt_min=type_curr[0])
    await state.update_data(crypt_max=type_curr[1])
    data = await state.get_data()
    await bot.send_message(message.chat.id,f'Выберите количество времени, в течение которого должна быть отправлена '
                                           f'оплата.', reply_markup=nav.builder_buytime.as_markup())


@dp.callback_query(F.data == 'p2p_buy_time')
async def buy_p2p_crypt_time(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(f'Выберите количество времени, в течение которого должна быть отправлена '
                                     f'оплата.', reply_markup=nav.builder_buytime.as_markup())
    await callback.answer()


@dp.callback_query(F.data == 'p2p_create_buy_curr')
async def p2p_create_announcement_buy(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(f'🎉 Объявление успешно создано!\n\nТеперь вы можете опубликовать объявление, '
                                     f'чтобы начать принимать сделки.', reply_markup=nav.inline_p2p_buy_curr_menu_2)


@dp.callback_query(F.data == 'p2p_bank_edit')
async def p2p_conditions(callback: CallbackQuery, state: FSMContext):
    data = await state.update_data()
    request = await read_db(f'p2p_advertisements WHERE number="{data['number']}"','currency, crypt, min, max, type')
    if request[0][1] == 'buy':
        word = 'покупке'
    else:
        word = 'продаже'
    await callback.message.edit_text(f'Редактирование лимитов сделки по {word} #{data['number']}.\n\nОтправьте лимиты сделки в {cfg.bot_currency_2[int(request[0][0])]} через дефис, которые определяют минимальную и максимальную сумму одной сделки (например, 600-9575.35 или 600-30000000).\n\nТекущие лимиты: {request[0][2]} - {request[0][3]}', reply_markup=nav.inline_p2p_conditions_menu_)
    await state.set_state(cl.Buy_p2p.crypt_max)


@dp.callback_query(F.data == 'p2p_limits_edit')
async def p2p_conditions(callback: CallbackQuery, state: FSMContext):
    data = await state.update_data()
    request = await read_db(f'p2p_advertisements WHERE number="{data['number']}"','currency, crypt, min, max, type')
    if request[0][1] == 'buy':
        word = 'покупке'
    else:
        word = 'продаже'
    await callback.message.edit_text(f'Редактирование лимитов сделки по {word} #{data['number']}.\n\nОтправьте лимиты сделки в {cfg.bot_currency_2[int(request[0][0])]} через дефис, которые определяют минимальную и максимальную сумму одной сделки (например, 600-9575.35 или 600-30000000).\n\nТекущие лимиты: {request[0][2]} - {request[0][3]}', reply_markup=nav.inline_p2p_conditions_menu_)
    await state.set_state(cl.Buy_p2p.crypt_max)


@dp.message(cl.Buy_p2p.crypt_max)
async def p2p_conditions(message: types.Message, state: FSMContext):
    text = str(message.text)
    text = (message.text).split("-")
    data = await state.update_data()
    await state.update_data(crypt_min=text[0])
    await state.update_data(crypt_max=text[1])
    await write_db(f"UPDATE p2p_advertisements SET min='{text[0]}', max='{text[1]}' WHERE number='{data['number']}'")
    request = await read_db(f'p2p_advertisements WHERE number="{data['number']}"','currency, crypt, min, max, type')
    if request[0][1] == 'buy':
        word = 'покупке'
    else:
        word = 'продаже'
    if request is None:
        conditions = 'не указаны'
    else:
        conditions = str(request[0][0])
    await bot.send_message(message.chat.id,f'Редактирование лимитов сделки по {word} #{data['number']}.\n\nОтправьте лимиты сделки в {cfg.bot_currency_2[int(request[0][0])]} через дефис, которые определяют минимальную и максимальную сумму одной сделки (например, 600-9575.35 или 600-30000000).\n\nТекущие лимиты: {request[0][2]} - {request[0][3]}', reply_markup=nav.inline_p2p_conditions_menu_)


@dp.callback_query(F.data == 'p2p_withdrawn_adv')
async def p2p_withdrawn_adv(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await write_db(f"UPDATE p2p_advertisements SET status=0 WHERE number='{data['number']}'")
    await callback.answer(text=f'Объявление #{data['number']} снято с публикации')
    request = await read_db(f'p2p_advertisements WHERE number="{data['number']}"', '*')
    count = 1
    word = 'Продажа'
    if int(request[0][15]) == 1:
        word = 'Покупка'
    bank = ''
    banks = request[0][5].replace(',', '').split()
    status = '👌 Активно. Объявление показывается в общем списке.'
    status_mark = nav.inline_p2p_buy_curr_menu_3
    if int(request[0][17]) == 0:
        status = '😔 Неактивно. Объявление не показывается в общем списке.'
        status_mark = nav.inline_p2p_buy_curr_menu_3_1
    for i in banks:
        bank += str(count) + '.' + ' ' + str(cfg.banks[int(i)]) + '\n'
        count += 1
    if int(request[0][10]) == 60:
        time = '1 час'
    elif int(request[0][10]) == 30:
        time = '30 минут'
    else:
        time = '15 минут'
    conditions = 'не указаны.'
    if request[0][11] != '0':
        conditions = str(request[0][11])
    await callback.message.edit_text(
        f'🧾 Объявление #{request[0][1]}\n\n{word} {cfg.coins_index[int(request[0][6])]} за '
        f'{cfg.bot_currency_2[int(request[0][3])]}.\n\nЦена: {request[0][13]} '
        f'{cfg.bot_currency_2[int(request[0][3])]}\n\nОбщий объем: '
        f'{int(float(request[0][7]))} {cfg.coins_index[int(request[0][6])]}\nЛимиты: '
        f'{int(request[0][8])} {cfg.bot_currency_2[int(request[0][3])]} ~'
        f' {int(request[0][9])} {cfg.bot_currency_2[int(request[0][3])]}\n\n Способы '
        f'оплаты:\n{bank}\n\nСрок оплаты: {time}\n\nУсловия сделки: {conditions}\n\n{status}',
        reply_markup=status_mark)
    await callback.answer()


@dp.callback_query(F.data == 'delete_adv_edit')
async def delete_adv_edit(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await write_db(f"DELETE FROM p2p_advertisements WHERE number={data['number']}")
    await callback.message.edit_text(f'Вы успешно удалили объявление #{data['number']}', reply_markup=nav.inline_p2p_delete_adv_menu_2)



@dp.callback_query(F.data == 'delete_adv')
async def delete_adv(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await callback.message.edit_text(f'Вы уверены что хотите удалить объявление #{data['number']}', reply_markup=nav.inline_p2p_delete_adv_menu)

@dp.callback_query(F.data == 'p2p_conditions')
async def p2p_conditions(callback: CallbackQuery, state: FSMContext):
    data = await state.update_data()
    request = await read_db(f'p2p_advertisements WHERE number="{data['number']}"','conditions, type')
    if request[0][1] == 'buy':
        word = 'покупке'
    else:
        word = 'продаже'
    if request[0][0] == 0:
        conditions = 'не указаны'
    else:
        conditions = str(request[0][0])
    await callback.message.edit_text(f'Редактирование условий сделки по {word} #{data['number']}.\n\nПришлите дополнительные условия сделки по объявлению (до 500 символов).\nПользователи увидят эти условия перед созданием сделки.\nОбязательно укажите реквизиты для оплаты!\n\nТекущие условия сделки: {conditions}', reply_markup=nav.inline_p2p_conditions_menu_)
    await state.set_state(cl.Buy_p2p.conditions)


@dp.message(cl.Buy_p2p.conditions)
async def p2p_conditions(message: types.Message, state: FSMContext):
    text = str(message.text)
    data = await state.update_data()
    await state.update_data(conditions=text)
    request = await read_db(f'p2p_advertisements WHERE number="{data['number']}"', 'conditions, type')
    if request[0][1] == 'buy':
        word = 'покупке'
    else:
        word = 'продаже'
    if request is None:
        conditions = 'не указаны'
    else:
        conditions = str(request[0][0])
    await write_db(f"UPDATE p2p_advertisements SET conditions='{text}' WHERE number='{data['number']}'")
    await bot.send_message(message.chat.id,f'Редактирование условий сделки #{data['number']} по {word}.\n\nПришлите дополнительные условия сделки по объявлению (до 500 символов).\nПользователи увидят эти условия перед созданием сделки.\nОбязательно укажите реквизиты для оплаты!\n\nТекущие условия сделки: {text}', reply_markup=nav.inline_p2p_conditions_menu_)
    await state.set_state(cl.Buy_p2p.conditions)


@dp.message(cl.Ticket.text)
async def p2p_support_text(message: types.Message, state: FSMContext):
    text2 = message.text
    data = await state.update_data()
    await bot.send_message(message.chat.id,f'Спасибо! Ваше обращиние #{data['number_tik']} c текстом:\n{text2}\n\nУпешно отправлено.\n\nВ ближайщее время с вами на связь выйдет администрация нашей платформы.')
    await write_db(f"INSERT INTO support_tickets (number_freezing, number_adv, id, id_vendor, message, number_tik) VALUES ({data['number']}, {data['number_adv']}, {data['id']}, {data['id_vendor']}, '{text2}', {data['number_tik']})")
    request = await read_db(f'users WHERE access=1', 'id')
    builder = InlineKeyboardBuilder()
    builder.button(
        text=f'Посмотреть обращение #{data['number_tik']}',
        callback_data=cl_m.Advertisements(action='select_ticket', number=f'{data['number_tik']}'))
    builder.adjust(1)
    builder.as_markup()
    for i in request[0]:
        await bot.send_message(int(i),f'Поступило новое обращние в поддержку.\nНомер: #{data['number_tik']}', reply_markup=builder.as_markup())


@dp.callback_query(F.data == 'p2p_create_announcement_buy')
async def p2p_create_announcement_buy_finish(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    number = random.randint(10000, 9999999)
    await state.update_data(number=number)
    request_2 = await read_db(
        f'users WHERE login="{callback.from_user.username}"', 'id')
    bank = ''
    count = 1
    for i in data['banks']:
        bank += str(count) + '.' + ' ' + str(cfg.banks[i]) + '\n'
        count += 1
    if data['percentage'] is None:
        sum = float(data['fix_count_sell']) * float(data['crypt_count'])
    else:
        sum = float(data['crypt_count']) * (
                    float(data['course']) + (float(data['course'])) * float(data['percentage']) / 100)
    if int(data['time']) < 60:
        time = f'{data['time']} минут'
    else:
        time = f'1 час'
    if data['type'] == 'buy':
        word = 'Покупка'
        type = 1
    else:
        word = 'Продажа'
        type = 0
    bank_list = ''
    for i in data['banks']:
        bank_list += str(i) + ', '
    if data['fix_count_sell'] is None:
        await write_db(f"INSERT INTO p2p_advertisements (id, number, login, currency, banks, crypt, crypt_count, min, max, time, percentage, sum, type) VALUES ({request_2[0][0]}, {number}, '{callback.from_user.username}',{int(data['currency'])}, '{bank_list}', {int(data['crypt'])}, '{data['crypt_count']}', '{data['crypt_min']}', '{data['crypt_max']}', {int(data['time'])}, '{data['percentage']}', '{sum / float(data['crypt_count'])}', {type})")
    elif data['percentage'] is None:
        await write_db(f"INSERT INTO p2p_advertisements (id, number, login, currency, banks, crypt, crypt_count, min, max, time, fix_count_sell, sum, type) VALUES ({request_2[0][0]}, {number}, '{callback.from_user.username}',{int(data['currency'])}, '{bank_list}', {int(data['crypt'])}, '{data['crypt_count']}', '{data['crypt_min']}', '{data['crypt_max']}', {int(data['time'])}, '{data['fix_count_sell']}', '{sum}', {type})")
    data = await state.get_data()
    request = await read_db(f'p2p_advertisements WHERE number="{data['number']}"', '*')
    count = 1
    bank = ''
    banks = request[0][5].replace(',', '').split()
    for i in banks:
        bank += str(count) + '.' + ' ' + str(cfg.banks[int(i)]) + '\n'
        count += 1
    if int(request[0][10]) < 60:
        time = f'{data['time']} минут'
    else:
        time = f'1 час'
    await callback.message.edit_text(f'🧾 Объявление #{request[0][1]}\n\n{word} {cfg.coins_index[int(request[0][6])]} за '
                                     f'{cfg.bot_currency_2[int(request[0][3])]}.\n\nЦена: {request[0][14]} '
                                     f'{cfg.bot_currency_2[int(request[0][3])]}\n\nОбщий объем: '
                                     f'{int(float(request[0][7]))} {cfg.coins_index[int(request[0][6])]}\nЛимиты: '
                                     f'{int(request[0][8])} {cfg.bot_currency_2[int(request[0][3])]} ~'
                                     f' {int(request[0][9])} {cfg.bot_currency_2[int(request[0][3])]}\n\n Способы '
                                     f'оплаты:\n{bank}\n\nСрок оплаты: {time}\n\nУсловия сделки: не указаны.\n\n👌 '
                                     f'Активно. Объявление показывается в общем списке.',
                                     reply_markup=nav.inline_p2p_buy_curr_menu_3)
    await state.clear()
    await callback.answer()


@dp.callback_query(cl_m.Buy_time.filter())
async def p2p_cteate_buy_p2p_bank(callback: CallbackQuery, callback_data: cl_m.Banks, state: FSMContext):
    if callback_data.action == 'select_time_buy':
        time = callback_data.time
        await state.update_data(time=time)
        data = await state.get_data()
        bank = ''
        count = 1
        for i in data['banks']:
            bank += str(count) + '.' + ' ' + str(cfg.banks[i]) + '\n'
            count += 1
        if data['percentage'] is None:
            sum = float(data['fix_count_sell']) * float(data['crypt_count'])
        else:
            sum = float(data['crypt_count']) * (float(data['course']) + (float(data['course']))*float(data['percentage'])/100)
        if int(data['time']) < 60:
            time = f'{data['time']} минут'
        else:
            time = f'1 час'
        if data['type'] == 'buy':
            word = 'Покупка'
        else:
            word = 'Продажа'
        await callback.message.edit_text(f'{word} {cfg.coins_index[int(data['crypt'])]} за '
                                         f'{cfg.bot_currency_2[int(data['currency'])]}.\n\n'
                                         f'Цена: {sum} {cfg.bot_currency_2[int(data['currency'])]}'
                                         f'\n\nОбщий объем: {data['crypt_count']} {cfg.coins_index[int(data['crypt'])]}\n'
                                         f'Лимиты: {data['crypt_min']} {cfg.bot_currency_2[int(data['currency'])]} ~ '
                                         f'{data['crypt_max']} {cfg.bot_currency_2[int(data['currency'])]}\n\n'
                                         f'Способы оплаты:\n{bank}\nСрок оплаты: {time}',
                                         reply_markup=nav.inline_p2p_buy_curr_menu)


@dp.message(cl.Buy_p2p.percentage)
async def trade_crypt(message: types.Message, state: FSMContext):
    type = float((message.text).replace(',', '.'))
    await state.update_data(percentage=type)
    await state.update_data(fix_count_sell=None)
    data = await state.update_data()
    await bot.send_message(message.chat.id,
        f'Пришлите процент от биржевого курса для покупки {cfg.coins_index[int(data['crypt'])]}.\n(например,+4% или -2.5%)\n\nБиржевой курс: {float(data['course'])} {cfg.bot_currency_2[int(data['currency'])]}\n\nЦена за 1 {cfg.coins_index[int(data['crypt'])]} = {float(data['course']) + (float(data['course']) * float(data['percentage']) / 100)} {cfg.bot_currency_2[int(data['currency'])]}\nПроцент биржевого курса: {data['percentage']}%\n\n{'-'*60}\n⚠️ В курсе объявления должны быть учтены все возможные комиссии платёжных систем. Правилами сервиса запрещено взимать дополнительные комиссии с пользователей - покупатели должны переводить точную сумму сделки.\n{'-'*60}',
        reply_markup=nav.inline_p2p_bank_2_floating_menu)
    await state.set_state(cl.Buy_p2p.percentage)

@dp.message(cl.Buy_p2p.fix_count_sell)
async def trade_crypt(message: types.Message, state: FSMContext):
    type = float((message.text).replace(',', '.'))
    await state.update_data(percentage=None)
    await state.update_data(fix_count_sell=type)
    data = await state.update_data()
    if data['type'] == 'buy':
        await bot.send_message(message.chat.id,
            f'Пришлите фиксированную цену в {cfg.bot_currency_2[int(data['currency'])]} для покупки {cfg.coins_index[int(data['crypt'])]}.\n\nБиржевой курс: {float(data['course'])} {cfg.bot_currency_2[int(data['currency'])]}\n\nЦена за 1 {cfg.coins_index[int(data['crypt'])]} = {data['fix_count_sell']} {cfg.bot_currency_2[int(data['currency'])]}\n\n{'-'*60}\n⚠️ В цене объявления должны быть учтены все возможные комиссии платёжных систем. Правилами сервиса запрещено взимать дополнительные комиссии с пользователей - покупатели должны переводить точную сумму сделки.\n{'-'*60}',
            reply_markup=nav.inline_p2p_bank_2_fix_menu)
    elif data['type'] == 'sell':
        await bot.send_message(message.chat.id,
                               f'Пришлите фиксированную цену в {cfg.bot_currency_2[int(data['currency'])]} для продажи {cfg.coins_index[int(data['crypt'])]}.\n\nБиржевой курс: {float(data['course'])} {cfg.bot_currency_2[int(data['currency'])]}\n\nЦена за 1 {cfg.coins_index[int(data['crypt'])]} = {data['fix_count_sell']} {cfg.bot_currency_2[int(data['currency'])]}\n\n{'-' * 60}\n⚠️ В цене объявления должны быть учтены все возможные комиссии платёжных систем. Правилами сервиса запрещено взимать дополнительные комиссии с пользователей - покупатели должны переводить точную сумму сделки.\n{'-' * 60}',
                               reply_markup=nav.inline_p2p_bank_2_fix_menu)
    await state.set_state(cl.Buy_p2p.fix_count_sell)


@dp.message()
async def bot_message(message: types.Message, state: FSMContext):
    if message.document or message.photo:
        data = await state.get_data()
        request = await read_db(f'p2p_advertisements WHERE number="{data['number_adv']}"','type')
        if int(request[0][0]) == 0:
            chat_id = data['id_vendor']
            builder_trade_active = InlineKeyboardBuilder()
            builder_trade_active.button(
                text='Подтвердить сделку',
                callback_data=cl_m.Advertisements_p2p(action='p2p_trade_fin', value=f'{data['number']}')
            )
            builder_trade_active.button(
                text='Написать в поддержку',
                callback_data=cl_m.Advertisements_p2p(action='p2p_support', value=f'{data['number']}')
            )
            builder_trade_active.adjust(1)
            builder_trade_active.as_markup()
            if chat_id:
                if message.forward_from:
                    forward_text = message.caption if message.caption else None
                    await message.copy_to(chat_id, disable_notification=True,
                                          caption=forward_text, reply_markup=builder_trade_active.as_markup())
                else:
                    await message.copy_to(chat_id,
                                          disable_notification=True, reply_markup=builder_trade_active.as_markup())
        elif int(request[0][0]) == 1:
            chat_id = data['id']
            builder_trade_active = InlineKeyboardBuilder()
            builder_trade_active.button(
                text='Подтвердить сделку',
                callback_data=cl_m.Advertisements_p2p(action='p2p_trade_fin', value=f'{data['number']}')
            )
            builder_trade_active.button(
                text='Написать в поддержку',
                callback_data=cl_m.Advertisements_p2p(action='p2p_support', value=f'{data['number']}')
            )
            builder_trade_active.adjust(1)
            builder_trade_active.as_markup()
            if chat_id:
                if message.forward_from:
                    forward_text = message.caption if message.caption else None
                    await message.copy_to(chat_id, disable_notification=True,
                                          caption=forward_text, reply_markup=builder_trade_active.as_markup())
                else:
                    await message.copy_to(chat_id,
                                          disable_notification=True, reply_markup=builder_trade_active.as_markup())
    if message.text == cfg.lang_ru['home']:
        await bot.send_message(message.chat.id, f'{cfg.lang_ru['home']}',reply_markup=nav.main_menu)
    elif message.text == cfg.lang_ru['P2P']:
        request = await read_db(f'users WHERE login="{message.from_user.username}"', 'active_user')
        request_2 = await read_db(f'exchange_rates WHERE currency_1="USDT" && currency_2="RUB"', 'rate')
        if request[0][0] == 1:
            status = '✅ Активная торговля'
        else:
            status = '❌ Торговля деактивирована'
        mark = nav.inline_p2p_main_menu_deactivate
        if int(request[0][0]) == 0:
            mark = nav.inline_p2p_main_menu_activate
        await bot.send_message(message.chat.id, f'Здесь Вы совершаете сделки с людьми, а бот выступает как гарант.'
                                                f'\nБудтье вежливы друг с другом.\nБиржевой курс: {request_2[0][0]} RUB за 1 USDT'
                                                f'\nТекущий ваш статус:\n{' '*20}{status}',reply_markup=mark)
    elif message.text == cfg.lang_ru['settings']:
        await bot.send_message(message.chat.id, f'{cfg.lang_ru['settings']}',reply_markup=nav.settings_menu)
        await bot.send_message(message.chat.id, 'Остались вопросы? Напишите нам!',reply_markup=nav.inlnine_contct_menu)
    elif message.text == cfg.lang_ru['support']:
        link = InlineKeyboardBuilder()
        link.add(types.InlineKeyboardButton(
            text="Наша поддержка",
            url="https://t.me/")
        )
        await bot.send_message(message.chat.id, f'{cfg.lang_ru['support']}',reply_markup=link.as_markup())
    elif message.text == cfg.lang_ru['opportunities']:
        link = InlineKeyboardBuilder()
        link.add(types.InlineKeyboardButton(
            text="Имнформация о возможностях",
            url="https://t.me/")
        )
        await bot.send_message(message.chat.id, f'Узнать о возможностях данного бота можно узнать по кнопке ниже', reply_markup=link.as_markup())
    elif message.text == cfg.lang_ru['commissions']:
        await bot.send_message(message.chat.id, f'Тут информация о комиссиях')
    elif message.text == cfg.lang_ru['verification']:
        request = await read_db(f'users WHERE login="{message.from_user.username}"', 'name')
        if int(request[0][0]) == 0:
            await message.answer(f'Внимание!\n'
                                 f'Отправляя данные вы подтверждаете ваши личные данные и при оплате в чеке будут указанны ваши указанные данные, '
                                 f'в случае несоответсвия продавец имеет право откланить выплату.\n Введите ваше имя, фамилию и отчество', reply_markup=nav.main_menu)
            await state.set_state(cl.Verifi.name)
        else:
            await bot.send_message(message.chat.id, f'Вы уже проходили верификацию, ваше ФИО - {request[0][0]}\nЕсли вы хотите изменить '
                                                    f'данные верификации, то введите команду /reset_verifi')
    elif message.text == cfg.lang_ru['wallet']:
        request = await read_db(f'users_purses WHERE login="{message.from_user.username}"', '*')
        await message.answer(f'Ваш баланс:\n {cfg.coins_2[0]}: {request[0][2]} {cfg.coins_index[0]} \n{cfg.coins_2[1]}: {request[0][3]} {cfg.coins_index[1]} \n{cfg.coins_2[2]}: {request[0][4]} {cfg.coins_index[2]} '
                             f'\n{cfg.coins_2[3]}: {request[0][5]} {cfg.coins_index[3]} \n{cfg.coins_2[4]}: {request[0][6]} {cfg.coins_index[4]} \n{cfg.coins_2[5]}: {request[0][7]} {cfg.coins_index[5]} \n{cfg.coins_2[6]}: {request[0][8]} {cfg.coins_index[5]} \n{cfg.coins_2[7]}: {request[0][9]} {cfg.coins_index[7]} \n{cfg.coins_2[8]}: {request[0][10]} {cfg.coins_index[8]} \n{cfg.coins_2[9]}: {request[0][11]} {cfg.coins_index[9]}',
                             reply_markup=nav.wallet_menu)
    elif message.text == cfg.lang_ru['bot currency']:
        currency = await read_db(f'users WHERE login="{message.from_user.username}"', 'currency')

        await message.answer(f'Выберите локальную валюту:\n Сейчас установлена {cfg.bot_currency[currency[0][0]]}',
                             reply_markup=nav.bot_currency_menu)
    elif message.text == message.text in cfg.coins:
        currency = await read_db(f'users WHERE login="{message.from_user.username}"', 'currency')
        index_curr = cfg.coins.index(message.text)
        await write_db(f"UPDATE users SET currency={index_curr} WHERE login='{message.from_user.username}'")
        currency = await read_db(f'users WHERE login="{message.from_user.username}"', 'currency')
        await message.answer(f'Валюта {cfg.coins[currency[0][0]]} установлена!', reply_markup=nav.settings_menu)
    elif message.text == cfg.lang_ru['refill']:
        await message.answer(f'Выберите валюту для пополнения', reply_markup=nav.bot_refill_menu)
    elif message.text in cfg.coins:
        await message.answer(f'Вы выбрали {message.text}\nДля пополнения кошелька выполните действия по ссылке ниже\n(тут ссылка)', reply_markup=nav.bot_refill_menu)
    elif message.text == cfg.lang_ru['address_book']:
        await message.answer(f'{message.text}', reply_markup=nav.bot_address_book_menu)
    elif message.text == cfg.lang_ru['add']:
        await message.answer(f'Введите номер кошелька, который хотите добавить')
        await state.set_state(cl.Addwallets.number)
    elif message.text == cfg.lang_ru['save']:
        request = await read_db(f'users_purses WHERE login="{message.from_user.username}"','saved_wallets_1, saved_wallets_2, saved_wallets_3')
        await message.answer(f'Сохраненные счета в адресной книге: \n 1.{request[0][0]}\n 2.{request[0][1]}\n 3.{request[0][2]}', reply_markup=nav.bot_address_book_menu)
    elif message.text == cfg.lang_ru['delete']:
        request = await read_db(f'users_purses WHERE login="{message.from_user.username}"','saved_wallets_1, saved_wallets_2, saved_wallets_3')
        await message.answer(f'Выберите кошелек который хотите удалить:\n(Введите цифру от 1 до 3)'
                             f'\n 1.{request[0][0]}\n 2.{request[0][1]}\n 3.{request[0][2]}', reply_markup=nav.bot_address_book_menu)
        await state.set_state(cl.Deletewallets.number)
    elif message.text == cfg.lang_ru['withdraw']:
        request = await read_db(f'users_purses WHERE login="{message.from_user.username}"','saved_wallets_1, saved_wallets_2, saved_wallets_3')
        await message.answer(f'Введите номер кошелька, или выберите кошелек из списка, на который хотите вывести средства:'
                             f'\n(Для выбора кошелька из адресной книги введите цифру от 1 до 3)\n 1.{request[0][0]}'
                             f'\n 2.{request[0][1]}\n 3.{request[0][2]}',reply_markup=nav.wallet_menu)
        await state.set_state(cl.Withdraw.number)
    elif message.text == cfg.lang_ru['exchange']:
        request = await read_db(f'users_purses WHERE login="{message.from_user.username}"', '*')
        request_2 = await read_db(f'users WHERE login="{message.from_user.username}"', 'currency')
        await message.answer(f' 🐬 Здесь вы можете торговать криптовалютой как на обычной бирже.\n⚡️ Все заявки на обмен выполняются автоматически.\n{'-'*40}\nID пользователя: {message.from_user.username}\nОбщий баланс {cfg.coins_2[request_2[0][0]]}: {request[0][request_2[0][0]+2]} {cfg.coins_index[request_2[0][0]]} \n{'-'*40}\n🔹Tether {request[0][2]} USDT \n🔹Toncoin: {request[0][3]} TON \n🔹Gram: {request[0][4]} GRAM \n🔹Bitcoin: {request[0][5]} BTC \n🔹Litecoin: {request[0][6]} LTC \n🔹Ethereum: {request[0][7]} ETH \n🔹Binance Coin: {request[0][8]} BNB \n🔹TRON: {request[0][9]} TRX \n🔹USD Coin: {request[0][10]} USDC\n🔹Notcoin: {request[0][11]} NOT',reply_markup=nav.inlnine_exchange_menu_hide_zero)
    elif message.text:
        data = await state.get_data()
        if message.from_user.id == data['id']:
            chat_id = data['id_vendor']
            if chat_id:
                if message.forward_from:
                    forward_text = message.caption if message.caption else None
                    await message.copy_to(chat_id, disable_notification=True,
                                          caption=forward_text)
                else:
                    await message.copy_to(chat_id,
                                          disable_notification=True)

async def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
        host=config['SQL']['host'],
        user=config['SQL']['user'],
        passwd=config['SQL']['password'],
        database=config['SQL']['database']
        )
        print("Подключение к базе данных MySQL прошло успешно ;)")
    except Error as e:
        print(f"Произошла ошибка '{e}' :(")
    return connection

async def users_write_db(table, column, columns2, count, count2):
    connection = await create_connection()
    cursorObject = connection.cursor()
    try:
        insert_movies_query = f"INSERT INTO {table} ({column}, {columns2}) VALUES ('{count}', {count2})"
        with connection.cursor() as cursor:
            cursor.execute(insert_movies_query)
            connection.commit()
            print(f'Пользователь {count} был добавлен в таблицу {table} в столбец {column}!')
    except Error as e:
        print(f"Произошла ошибка '{e}' :(")
    connection.close()


def timer_delete(number, time2):
    sleep = time2 * 60
    time.sleep(sleep)
    request = read_db(f'freezing_of_funds WHERE number="{number}"', '*')
    if request:
        write_db(f"DELETE FROM freezing_of_funds WHERE number={number}")
        print(f'{number} удален')
    return


async def write_db(request):
    connection = await create_connection()
    cursorObject = connection.cursor()
    try:
        insert_movies_query = f"{request}"
        with connection.cursor() as cursor:
            cursor.execute(insert_movies_query)
            connection.commit()
            print(f'{request} успешно выполнено')
    except Error as e:
        print(f"Произошла ошибка '{e}' :(")
    connection.close()


def run_background_func(number, time2):
    threading.Thread(target=timer_delete(number, time2)).start()


async def read_db(tables, column='*'):
    connection = await create_connection()
    select_movies_query = f'SELECT {column} FROM {tables}'
    try:
        with connection.cursor() as cursor:
            cursor.execute(select_movies_query)
            result = cursor.fetchall()
            return result
    except Error as e:
        print(f"Произошла ошибка '{e}' :(")
    connection.close()

async def check_user_login(user_login, user_id):
    user_id2 = '{user_login}, {user_id}'
    table = 'users'
    column = 'login'
    column2 = 'id'
    table2 = 'users_purses'
    table3 = 'users_vendor'
    temp = await read_db(table)
    users = []
    for i in temp:
        users.append(i[1])
    try:
        users.index(user_id)
    except:
        try:
            await users_write_db(table, column, column2, user_login, user_id)
            await users_write_db(table2,column, column2, user_login, user_id)
            await users_write_db(table3, column, column2, user_login, user_id)
        except Exception as e:
            print(f'{e}')


def paginator_avde(mass, edit: int=0, page: int=0):
    builder = InlineKeyboardBuilder()
    count = 10
    if page == len(mass)-1:
        count = len(mass[-1])
    for i in range(0, count):
        builder.row(mass[page][i])
    if edit == 0:
        builder.row(
            InlineKeyboardButton(text='◀️', callback_data=cl_m.Banks(action='prev_avde', value='prev', page=page).pack()),
            InlineKeyboardButton(text=f'{page+1} из {len(mass)}', callback_data=cl_m.Banks(action='page', value='page', page=page).pack()),
            InlineKeyboardButton(text='▶️', callback_data=cl_m.Banks(action='next_avde', value='next', page=page).pack()),
            InlineKeyboardButton(text='Создать объявление', callback_data='p2p_create'),
            width=3
        )
    elif edit == 1:
        builder.row(
            InlineKeyboardButton(text='◀️',
                                 callback_data=cl_m.Banks(action='prev_avde', value='prev', page=page).pack()),
            InlineKeyboardButton(text=f'{page + 1} из {len(mass)}',
                                 callback_data=cl_m.Banks(action='page', value='page', page=page).pack()),
            InlineKeyboardButton(text='▶️',
                                 callback_data=cl_m.Banks(action='next_avde', value='next', page=page).pack()),
            InlineKeyboardButton(text='Указать сумму', callback_data='p2p_create_sum'),
            width=3
        )
    builder.row(
        InlineKeyboardButton(text='Назад', callback_data='back_p2p_menu'),
    )
    return builder.as_markup()


def paginator_2(mass, page: int=0):
    builder = InlineKeyboardBuilder()
    count = 10
    if page == 2:
        count = 8
    for i in range(0, count):
        builder.row(mass[page][i])
    builder.row(
        InlineKeyboardButton(text='◀️', callback_data=cl_m.Banks(action='prev_2', value='prev_2', page=page).pack()),
        InlineKeyboardButton(text=f'{page+1} из 3', callback_data=cl_m.Banks(action='page', value='page', page=page).pack()),
        InlineKeyboardButton(text='▶️', callback_data=cl_m.Banks(action='next_2', value='next_2', page=page).pack()),
        InlineKeyboardButton(text='Назад', callback_data='back_p2p_menu'),
        InlineKeyboardButton(text='Продолжить',callback_data=cl_m.Banks(action='p2p_create_buy_course', value='next', page=page).pack()),
        width=3
    )
    return builder.as_markup()


def paginator(mass, edit: int=0, page: int=0):
    builder = InlineKeyboardBuilder()
    count = 10
    if page == 2:
        count = 8
    for i in range(0, count):
        builder.row(mass[page][i])
    if edit == 0:
        builder.row(
            InlineKeyboardButton(text='◀️', callback_data=cl_m.Banks(action='prev', value='prev', page=page).pack()),
            InlineKeyboardButton(text=f'{page+1} из 3', callback_data=cl_m.Banks(action='page', value='page', page=page).pack()),
            InlineKeyboardButton(text='▶️', callback_data=cl_m.Banks(action='next', value='next', page=page).pack()),
            InlineKeyboardButton(text='Назад', callback_data='p2p_create'),
            InlineKeyboardButton(text='Продолжить',callback_data=cl_m.Banks(action='p2p_create_buy_course', value='next', page=page).pack()),
            width=3
        )
    elif edit == 1:
        builder.row(
            InlineKeyboardButton(text='◀️', callback_data=cl_m.Banks(action='prev_adv', value='prev', page=page).pack()),
            InlineKeyboardButton(text=f'{page + 1} из 3', callback_data=cl_m.Banks(action='page', value='page', page=page).pack()),
            InlineKeyboardButton(text='▶️', callback_data=cl_m.Banks(action='next_adv', value='next', page=page).pack()),
            InlineKeyboardButton(text='Назад', callback_data='back_adv_edit_2'),
            width=3
        )
    return builder.as_markup()


async def main():
    await dp.start_polling(bot, relax=3, skip_updates=False)


if __name__ == "__main__":
    asyncio.run(main())