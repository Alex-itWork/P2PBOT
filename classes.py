from imports import *

class Verifi(StatesGroup):
    name = State()


class Addwallets(StatesGroup):
    number = State()


class Deletewallets(StatesGroup):
    number = State()


class Withdraw(StatesGroup):
    number = State()
    check = State()


class Buycrypt(StatesGroup):
    type = State()
    type_user = State()
    count = State()
    amount = State()
    course = State()
    min = State()
    balance = State()
    type_user_hard = State
    balance_crypt = State()


class Sellcrypt(StatesGroup):
    type = State()
    type_user = State()
    count = State()
    amount = State()
    course = State()
    min = State()
    balance = State()
    type_user_hard = State
    balance_crypt = State()


class Tradecrypt(StatesGroup):
    type = State()
    type_user = State()
    count = State()
    amount = State()
    course = State()
    min = State()
    balance = State()
    type_user_hard = State
    balance_crypt = State()


class Buy_p2p(StatesGroup):
    type = State()
    currency = State()
    count = State()
    banks = State()
    crypt = State()
    crypt_min = State()
    crypt_max = State()
    crypt_count = State()
    time = State()
    conditions = State()
    percentage = State()
    fix_count_sell = State()
    course = State()
    number = State()
    edit = State()

class Announcement(StatesGroup):
    number = State()
    fix_count_sell = State()
    percentage = State()

class Announcement_pag(StatesGroup):
    mass = State()
    number = State()


class Buyp2p(StatesGroup):
    type = State()
    number = State()
    bank = State()
    crypto = State()
    fiat = State()
    sum = State()
    conditions = State()
    time = State()
    count = State()
    sum_crypt = State()
    sum_fiat = State()
    volume = State()
    filter = State()

class Trade(StatesGroup):
    number = State()
    number_adv = State()
    id = State()
    chat_id = State()
    id_vendor = State()

class Ticket(StatesGroup):
    number_tik = State()
    id = State()
    id_vendor = State()
    number = State()
    number_avd = State()
    text = State()

class Adm(StatesGroup):
    status = State()
    mass= State()
    number = State()
    course1 = State()
    course2 = State()
    count_course = State()
    id = State()

class Filter(StatesGroup):
    sum = State()