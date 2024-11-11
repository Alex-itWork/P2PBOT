import config as cfg
import classes_mark as cl_m
from imports import *


btn_home = KeyboardButton(text=cfg.lang_ru['home'])

# --- Main ---
btns_main_menu = [
    [
        KeyboardButton(text=cfg.lang_ru['wallet']),
        KeyboardButton(text=cfg.lang_ru['settings'])
    ],
    [
        KeyboardButton(text=cfg.lang_ru['exchange']),
        KeyboardButton(text=cfg.lang_ru['P2P'])
    ],
    [
        KeyboardButton(text=cfg.lang_ru['verification'])
    ]
]
main_menu = ReplyKeyboardMarkup(keyboard=btns_main_menu, resize_keyboard=True)

# --- Wallet ---
btns_menu_wallet = [
    [
        KeyboardButton(text=cfg.lang_ru['refill']),
        KeyboardButton(text=cfg.lang_ru['withdraw'])
    ],
    [
        KeyboardButton(text=cfg.lang_ru['address_book']),
        KeyboardButton(text=cfg.lang_ru['commissions'])
    ],
    [
        btn_home
    ]
]
wallet_menu = ReplyKeyboardMarkup(keyboard=btns_menu_wallet, resize_keyboard=True)

# --- P2P ---
btns_menu_p2p = [
    [
        KeyboardButton(text=cfg.lang_ru['buy']),
        KeyboardButton(text=cfg.lang_ru['sell'])
    ],
    [
      KeyboardButton(text=cfg.lang_ru['My_trades']),
      btn_home
    ]
]
p2p_menu = ReplyKeyboardMarkup(keyboard=btns_menu_p2p, resize_keyboard=True)

#--- Settings ---
btns_menu_settings = [
    [
        KeyboardButton(text=cfg.lang_ru['bot currency']),
        KeyboardButton(text=cfg.lang_ru['commissions'])
    ],
    [
        KeyboardButton(text=cfg.lang_ru['opportunities'])
    ],
    [
        btn_home
    ]
]
settings_menu = ReplyKeyboardMarkup(keyboard=btns_menu_settings, resize_keyboard=True)

#--- Verification ---
btns_menu_verification = [
    [
        KeyboardButton(text=cfg.lang_ru['confirm']),
        KeyboardButton(text=cfg.lang_ru['cancel'])
    ],
    [
        btn_home
    ]
]
verification_menu = ReplyKeyboardMarkup(keyboard=btns_menu_verification, resize_keyboard=True)

#--- bot_currency_menu ---
btns_bot_currency_menu = [
    [
        KeyboardButton(text=cfg.coins[0]),
        KeyboardButton(text=cfg.coins[1]),
        KeyboardButton(text=cfg.coins[2])
    ],
[
        KeyboardButton(text=cfg.coins[3]),
        KeyboardButton(text=cfg.coins[4]),
        KeyboardButton(text=cfg.coins[5])
    ],
[
        KeyboardButton(text=cfg.coins[6]),
        KeyboardButton(text=cfg.coins[7]),
        KeyboardButton(text=cfg.coins[8])
    ],
    [
        KeyboardButton(text=cfg.coins[9]),
        btn_home
    ]
]
bot_currency_menu = ReplyKeyboardMarkup(keyboard=btns_bot_currency_menu, resize_keyboard=True)

#--- Refill_menu --
btns_bot_refill_menu = [
    [
        KeyboardButton(text=cfg.coins[0]),
        KeyboardButton(text=cfg.coins[1]),
        KeyboardButton(text=cfg.coins[2])
    ],
[
        KeyboardButton(text=cfg.coins[3]),
        KeyboardButton(text=cfg.coins[4]),
        KeyboardButton(text=cfg.coins[5])
    ],
[
        KeyboardButton(text=cfg.coins[6]),
        KeyboardButton(text=cfg.coins[7]),
        KeyboardButton(text=cfg.coins[8])
    ],
    [
        KeyboardButton(text=cfg.coins[9]),
        btn_home
    ]
]
bot_refill_menu = ReplyKeyboardMarkup(keyboard=btns_bot_refill_menu, resize_keyboard=True)

#--- Withdraw_menu ---
btns_bot_withdraw_menu = [
    [
        KeyboardButton(text=cfg.lang_ru['address_book']),
        btn_home
    ]
]
bot_withdraw_menu = ReplyKeyboardMarkup(keyboard=btns_bot_withdraw_menu, resize_keyboard=True)

#--- address_book_menu ---
btns_bot_address_book_menu = [
    [
        KeyboardButton(text=cfg.lang_ru['add']),
        KeyboardButton(text=cfg.lang_ru['save']),
        KeyboardButton(text=cfg.lang_ru['delete'])
    ],
    [
        btn_home
    ]
]
bot_address_book_menu = ReplyKeyboardMarkup(keyboard=btns_bot_address_book_menu, resize_keyboard=True)

#--- inlnine_contct_menu---
btn_channel = InlineKeyboardButton(
            text=cfg.lang_ru['channel'],
            url="https://t.me/"
        )
btn_chat = InlineKeyboardButton(
    text=cfg.lang_ru['chat'],
    url="https://t.me/"
    )
btn_support = InlineKeyboardButton(
    text=cfg.lang_ru['support'],
    url="https://t.me/"
    )
inlnine_contct = [[btn_channel, btn_chat], [btn_support]]
inlnine_contct_menu = InlineKeyboardMarkup(inline_keyboard=inlnine_contct)

#--- inline_exchange_menu ---
btn_buy = InlineKeyboardButton(
    text=cfg.lang_ru['buy'],
    callback_data='buy_crypt'
    )
btn_sell = InlineKeyboardButton(
    text=cfg.lang_ru['sell'],
    callback_data="sell_crypt"
    )
btn_trade = InlineKeyboardButton(
    text="Обменять",
    callback_data='trade_cpypt'
    )
btn_story_exchange = InlineKeyboardButton(
    text="История",
    callback_data='story_exchange'
    )
btn_story_exchange_buy = InlineKeyboardButton(
    text="История покупок",
    callback_data='story_exchange_buy'
    )
btn_story_exchange_sell = InlineKeyboardButton(
    text="История продаж",
    callback_data='story_exchange_sell'
    )
btn_story_exchange_trade = InlineKeyboardButton(
    text="История обменов",
    callback_data='story_exchange_trade'
    )
btn_show_zero_balance = InlineKeyboardButton(
    text=cfg.lang_ru['show_zero_balance'],
    callback_data='show_zero_balance'
)
btn_hide_zero_balance = InlineKeyboardButton(
    text=cfg.lang_ru['hide_zero_balance'],
    callback_data='hide_zero_balance'
)
btn_total_balance_currency = InlineKeyboardButton(
    text=cfg.lang_ru['total_balance_currency'],
    callback_data='total_balance_currency'
)
inlnine_exchange_hide_zero = [[btn_buy, btn_sell], [btn_trade, btn_story_exchange], [btn_hide_zero_balance, btn_total_balance_currency]]
inlnine_exchange_menu_hide_zero = InlineKeyboardMarkup(inline_keyboard=inlnine_exchange_hide_zero)
inlnine_exchange_show_zero = [[btn_buy, btn_sell], [btn_trade, btn_story_exchange], [btn_show_zero_balance, btn_total_balance_currency]]
inlnine_exchange_menu_show_zero = InlineKeyboardMarkup(inline_keyboard=inlnine_exchange_show_zero)

back_exchange_buy_crypt = InlineKeyboardButton(
    text='◀️ Назад',
    callback_data='back_exchange_buy_crypt'
)

back_exchange_sell_crypt = InlineKeyboardButton(
    text='◀️ Назад',
    callback_data='back_exchange_sell_crypt'
)

btn_back_exchange_trade_crypt = InlineKeyboardButton(
    text='◀️ Назад',
    callback_data='back_exchange'
)

btn_back_exchange = InlineKeyboardButton(
    text='◀️ Назад',
    callback_data='back_exchange'
)

builder = InlineKeyboardBuilder()
builder.button(
    text=cfg.coins_index[1],
    callback_data=cl_m.Coins(action='select_coin', value='TON')
)
builder.button(
    text=cfg.coins_index[2],
    callback_data=cl_m.Coins(action='select_coin', value='GRAM')
)
builder.button(
    text=cfg.coins_index[3],
    callback_data=cl_m.Coins(action='select_coin', value='BTC')
)
builder.button(
    text=cfg.coins_index[4],
    callback_data=cl_m.Coins(action='select_coin', value='LTC')
)
builder.button(
    text=cfg.coins_index[5],
    callback_data=cl_m.Coins(action='select_coin', value='ETH')
)
builder.button(
    text=cfg.coins_index[6],
    callback_data=cl_m.Coins(action='select_coin', value='BNB')
)
builder.button(
    text=cfg.coins_index[7],
    callback_data=cl_m.Coins(action='select_coin', value='TRX')
)
builder.button(
    text=cfg.coins_index[8],
    callback_data=cl_m.Coins(action='select_coin', value='USDC')
)
builder.button(
    text=cfg.coins_index[9],
    callback_data=cl_m.Coins(action='select_coin', value='NOT')
)
builder.button(
    text='◀️ Назад',
    callback_data=cl_m.Coins(action='back_exchange', value='back_exchange')
)
builder.adjust(3)
builder.as_markup()



btn_create_application = InlineKeyboardButton(
    text=cfg.lang_ru['create_application'],
    callback_data='create_application_buy'
)

btn_create_application_sell = InlineKeyboardButton(
    text=cfg.lang_ru['create_application'],
    callback_data='create_application_sell'
)

btn_create_application_trade = InlineKeyboardButton(
    text=cfg.lang_ru['create_application'],
    callback_data='create_application_trade'
)

inlnine_create_application_trade = [[btn_create_application_trade],[btn_back_exchange_trade_crypt]]
inlnine_exchange_menu_create_application_trade = InlineKeyboardMarkup(inline_keyboard=inlnine_create_application_trade)

inline_create_exchange_menu_story = [[btn_story_exchange_buy, btn_story_exchange_sell], [btn_story_exchange_trade, btn_back_exchange]]
inline_exchange_menu_story = InlineKeyboardMarkup(inline_keyboard=inline_create_exchange_menu_story)

inlnine_create_application_sell = [[btn_create_application_sell, back_exchange_sell_crypt]]
inlnine_exchange_menu_create_application_sell = InlineKeyboardMarkup(inline_keyboard=inlnine_create_application_sell)

inlnine_create_application = [[btn_create_application, back_exchange_buy_crypt]]
inlnine_exchange_menu_create_application = InlineKeyboardMarkup(inline_keyboard=inlnine_create_application)

inlnine_exchange_back_3 = [[back_exchange_sell_crypt]]
inlnine_exchange_menu_back_3 = InlineKeyboardMarkup(inline_keyboard=inlnine_exchange_back_3)

inlnine_exchange_back_2 = [[btn_back_exchange]]
inlnine_exchange_menu_back_2 = InlineKeyboardMarkup(inline_keyboard=inlnine_exchange_back_2)


inlnine_exchange_back = [[back_exchange_buy_crypt]]
inlnine_exchange_menu_back = InlineKeyboardMarkup(inline_keyboard=inlnine_exchange_back)

inline_back_exchange_trade_crypt = [[btn_back_exchange_trade_crypt]]
inline_back_exchange_menu_trade_crypt =InlineKeyboardMarkup(inline_keyboard=inline_back_exchange_trade_crypt)


builder_sell = InlineKeyboardBuilder()
builder_sell.button(
    text=cfg.coins_index[1],
    callback_data=cl_m.Coins(action='select_coin_sell', value='TON')
)
builder_sell.button(
    text=cfg.coins_index[2],
    callback_data=cl_m.Coins(action='select_coin_sell', value='GRAM')
)
builder_sell.button(
    text=cfg.coins_index[3],
    callback_data=cl_m.Coins(action='select_coin_sell', value='BTC')
)
builder_sell.button(
    text=cfg.coins_index[4],
    callback_data=cl_m.Coins(action='select_coin_sell', value='LTC')
)
builder_sell.button(
    text=cfg.coins_index[5],
    callback_data=cl_m.Coins(action='select_coin_sell', value='ETH')
)
builder_sell.button(
    text=cfg.coins_index[6],
    callback_data=cl_m.Coins(action='select_coin_sell', value='BNB')
)
builder_sell.button(
    text=cfg.coins_index[7],
    callback_data=cl_m.Coins(action='select_coin_sell', value='TRX')
)
builder_sell.button(
    text=cfg.coins_index[8],
    callback_data=cl_m.Coins(action='select_coin_sell', value='USDC')
)
builder_sell.button(
    text=cfg.coins_index[9],
    callback_data=cl_m.Coins(action='select_coin_sell', value='NOT')
)
builder_sell.button(
    text='◀️ Назад',
    callback_data=cl_m.Coins(action='back_exchange', value='back_exchange')
)
builder_sell.adjust(3)
builder_sell.as_markup()


builder_trade = InlineKeyboardBuilder()
builder_trade.button(
    text=cfg.coins_index[0],
    callback_data=cl_m.Coins(action='select_coin_trade', value='USDT')
)
builder_trade.button(
    text=cfg.coins_index[1],
    callback_data=cl_m.Coins(action='select_coin_trade', value='TON')
)
builder_trade.button(
    text=cfg.coins_index[2],
    callback_data=cl_m.Coins(action='select_coin_trade', value='GRAM')
)
builder_trade.button(
    text=cfg.coins_index[3],
    callback_data=cl_m.Coins(action='select_coin_trade', value='BTC')
)
builder_trade.button(
    text=cfg.coins_index[4],
    callback_data=cl_m.Coins(action='select_coin_trade', value='LTC')
)
builder_trade.button(
    text=cfg.coins_index[5],
    callback_data=cl_m.Coins(action='select_coin_trade', value='ETH')
)
builder_trade.button(
    text=cfg.coins_index[6],
    callback_data=cl_m.Coins(action='select_coin_trade', value='BNB')
)
builder_trade.button(
    text=cfg.coins_index[7],
    callback_data=cl_m.Coins(action='select_coin_trade', value='TRX')
)
builder_trade.button(
    text=cfg.coins_index[8],
    callback_data=cl_m.Coins(action='select_coin_trade', value='USDC')
)
builder_trade.button(
    text=cfg.coins_index[9],
    callback_data=cl_m.Coins(action='select_coin_trade', value='NOT')
)
builder_trade.button(
    text='◀️ Назад',
    callback_data=cl_m.Coins(action='back_exchange', value='back_exchange')
)
builder_trade.adjust(3)
builder_trade.as_markup()

builder_trade = InlineKeyboardBuilder()
builder_trade.button(
    text=cfg.coins_index[0],
    callback_data=cl_m.Coins(action='select_coin_trade', value='USDT')
)
builder_trade.button(
    text=cfg.coins_index[1],
    callback_data=cl_m.Coins(action='select_coin_trade', value='TON')
)
builder_trade.button(
    text=cfg.coins_index[2],
    callback_data=cl_m.Coins(action='select_coin_trade', value='GRAM')
)
builder_trade.button(
    text=cfg.coins_index[3],
    callback_data=cl_m.Coins(action='select_coin_trade', value='BTC')
)
builder_trade.button(
    text=cfg.coins_index[4],
    callback_data=cl_m.Coins(action='select_coin_trade', value='LTC')
)
builder_trade.button(
    text=cfg.coins_index[5],
    callback_data=cl_m.Coins(action='select_coin_trade', value='ETH')
)
builder_trade.button(
    text=cfg.coins_index[6],
    callback_data=cl_m.Coins(action='select_coin_trade', value='BNB')
)
builder_trade.button(
    text=cfg.coins_index[7],
    callback_data=cl_m.Coins(action='select_coin_trade', value='TRX')
)
builder_trade.button(
    text=cfg.coins_index[8],
    callback_data=cl_m.Coins(action='select_coin_trade', value='USDC')
)
builder_trade.button(
    text=cfg.coins_index[9],
    callback_data=cl_m.Coins(action='select_coin_trade', value='NOT')
)
builder_trade.button(
    text='◀️ Назад',
    callback_data=cl_m.Coins(action='back_exchange', value='back_exchange')
)
builder_trade.adjust(3)
builder_trade.as_markup()

builder_trade_2 = InlineKeyboardBuilder()
builder_trade_2.button(
    text=cfg.coins_index[0],
    callback_data=cl_m.Coins(action='select_coin_trade', value='USDT')
)
builder_trade_2.button(
    text=cfg.coins_index[1],
    callback_data=cl_m.Coins(action='select_coin_trade_2', value='TON')
)
builder_trade_2.button(
    text=cfg.coins_index[2],
    callback_data=cl_m.Coins(action='select_coin_trade_2', value='GRAM')
)
builder_trade_2.button(
    text=cfg.coins_index[3],
    callback_data=cl_m.Coins(action='select_coin_trade_2', value='BTC')
)
builder_trade_2.button(
    text=cfg.coins_index[4],
    callback_data=cl_m.Coins(action='select_coin_trade_2', value='LTC')
)
builder_trade_2.button(
    text=cfg.coins_index[5],
    callback_data=cl_m.Coins(action='select_coin_trade_2', value='ETH')
)
builder_trade_2.button(
    text=cfg.coins_index[6],
    callback_data=cl_m.Coins(action='select_coin_trade_2', value='BNB')
)
builder_trade_2.button(
    text=cfg.coins_index[7],
    callback_data=cl_m.Coins(action='select_coin_trade_2', value='TRX')
)
builder_trade_2.button(
    text=cfg.coins_index[8],
    callback_data=cl_m.Coins(action='select_coin_trade_2', value='USDC')
)
builder_trade_2.button(
    text=cfg.coins_index[8],
    callback_data=cl_m.Coins(action='select_coin_trade_2', value='NOT')
)
builder_trade_2.button(
    text='◀️ Назад',
    callback_data=cl_m.Coins(action='back_exchange', value='back_exchange')
)
builder_trade_2.adjust(3)
builder_trade_2.as_markup()

builder_balance_currency = InlineKeyboardBuilder()
builder_balance_currency.button(
    text=cfg.coins_index[0],
    callback_data=cl_m.Balance_currency(action='select_balance_currency', value='0')
)
builder_balance_currency.button(
    text=cfg.coins_index[1],
    callback_data=cl_m.Balance_currency(action='select_balance_currency', value='1')
)
builder_balance_currency.button(
    text=cfg.coins_index[2],
    callback_data=cl_m.Balance_currency(action='select_balance_currency', value='2')
)
builder_balance_currency.button(
    text=cfg.coins_index[3],
    callback_data=cl_m.Balance_currency(action='select_balance_currency', value='3')
)
builder_balance_currency.button(
    text=cfg.coins_index[4],
    callback_data=cl_m.Balance_currency(action='select_balance_currency', value='4')
)
builder_balance_currency.button(
    text=cfg.coins_index[5],
    callback_data=cl_m.Balance_currency(action='select_balance_currency', value='5')
)
builder_balance_currency.button(
    text=cfg.coins_index[6],
    callback_data=cl_m.Balance_currency(action='select_balance_currency', value='6')
)
builder_balance_currency.button(
    text=cfg.coins_index[7],
    callback_data=cl_m.Balance_currency(action='select_balance_currency', value='7')
)
builder_balance_currency.button(
    text=cfg.coins_index[8],
    callback_data=cl_m.Balance_currency(action='select_balance_currency', value='8')
)
builder_balance_currency.button(
    text=cfg.coins_index[9],
    callback_data=cl_m.Balance_currency(action='select_balance_currency', value='9')
)
builder_balance_currency.button(
    text=cfg.lang_ru['back'],
    callback_data=cl_m.Balance_currency(action='back_exchange', value='back_exchange')
)
builder_balance_currency.adjust(3)
builder_balance_currency.as_markup()

back_exchange_sell_crypt = InlineKeyboardButton(
    text='◀️ Назад',
    callback_data='back_exchange_sell_crypt'
)
btn_p2p_buy = InlineKeyboardButton(
    text=cfg.lang_ru['buy'],
    callback_data='p2p_buy'
)
btn_p2p_sell = InlineKeyboardButton(
    text=cfg.lang_ru['sell'],
    callback_data='p2p_sell'
)
btn_p2p_my_advertisements = InlineKeyboardButton(
    text=cfg.lang_ru['my_advertisements'],
    callback_data='my_advertisements'
)
btn_p2p_active_trades = InlineKeyboardButton(
    text=cfg.lang_ru['active_trades'],
    callback_data='p2p_active_trades'
)
btn_p2p_deactivate = InlineKeyboardButton(
    text=cfg.lang_ru['deactivate'],
    callback_data='p2p_deactivate'
)

btn_p2p_activate = InlineKeyboardButton(
    text=cfg.lang_ru['active'],
    callback_data='p2p_activate'
)

inline_p2p_main_deactivate = [[btn_p2p_buy, btn_p2p_sell], [btn_p2p_my_advertisements],[btn_p2p_active_trades], [btn_p2p_deactivate]]
inline_p2p_main_menu_deactivate =InlineKeyboardMarkup(inline_keyboard=inline_p2p_main_deactivate)

inline_p2p_main_activate = [[btn_p2p_buy, btn_p2p_sell], [btn_p2p_active_trades], [btn_p2p_activate]]
inline_p2p_main_menu_activate =InlineKeyboardMarkup(inline_keyboard=inline_p2p_main_activate)

btn_p2p_create = InlineKeyboardButton(
    text=cfg.lang_ru['create_p2p'],
    callback_data='p2p_create'
)

btn_p2p_back = InlineKeyboardButton(
    text='◀️ Назад',
    callback_data='back_p2p_menu'
)

inline_p2p_create_main = [[btn_p2p_create], [btn_p2p_back]]
inline_p2p_create_main_menu =InlineKeyboardMarkup(inline_keyboard=inline_p2p_create_main)

btn_p2p_advertisements_buy = InlineKeyboardButton(
    text=cfg.lang_ru['buy'],
    callback_data='p2p_create_buy'
)
btn_p2p_advertisements_sell = InlineKeyboardButton(
    text=cfg.lang_ru['sell'],
    callback_data='p2p_create_sell'
)
btn_p2p_back_advertisements = InlineKeyboardButton(
    text='◀️ Назад',
    callback_data='my_advertisements'
)

inline_p2p_create_main_advertisements = [[btn_p2p_advertisements_buy, btn_p2p_advertisements_sell], [btn_p2p_back_advertisements]]
inline_p2p_create_advertisements_menu =InlineKeyboardMarkup(inline_keyboard=inline_p2p_create_main_advertisements)

builder_advertisements_p2p = InlineKeyboardBuilder()
builder_advertisements_p2p.button(
    text=cfg.coins_index[0],
    callback_data=cl_m.Advertisements_p2p(action='select_balance_currency', value='0')
)
builder_advertisements_p2p.button(
    text=cfg.coins_index[1],
    callback_data=cl_m.Advertisements_p2p(action='select_balance_currency', value='1')
)
builder_advertisements_p2p.button(
    text=cfg.coins_index[2],
    callback_data=cl_m.Advertisements_p2p(action='select_balance_currency', value='2')
)
builder_advertisements_p2p.button(
    text=cfg.coins_index[3],
    callback_data=cl_m.Advertisements_p2p(action='select_balance_currency', value='3')
)
builder_advertisements_p2p.button(
    text=cfg.coins_index[4],
    callback_data=cl_m.Advertisements_p2p(action='select_balance_currency', value='4')
)
builder_advertisements_p2p.button(
    text=cfg.coins_index[5],
    callback_data=cl_m.Advertisements_p2p(action='select_balance_currency', value='5')
)
builder_advertisements_p2p.button(
    text=cfg.coins_index[6],
    callback_data=cl_m.Advertisements_p2p(action='select_balance_currency', value='6')
)
builder_advertisements_p2p.button(
    text=cfg.coins_index[7],
    callback_data=cl_m.Balance_currency(action='select_balance_currency', value='7')
)
builder_advertisements_p2p.button(
    text=cfg.coins_index[8],
    callback_data=cl_m.Balance_currency(action='select_balance_currency', value='8')
)
builder_advertisements_p2p.button(
    text=cfg.coins_index[9],
    callback_data=cl_m.Balance_currency(action='select_balance_currency', value='9')
)
builder_advertisements_p2p.button(
    text=cfg.lang_ru['back'],
    callback_data='p2p_create'
)
builder_advertisements_p2p.adjust(3)
builder_advertisements_p2p.as_markup()

builder_adv_p2p_fiat = InlineKeyboardBuilder()
builder_adv_p2p_fiat.button(
    text=cfg.bot_currency[0],
    callback_data=cl_m.Advertisements_p2p_fiat(action='select_balance_currency', value='0')
)
builder_adv_p2p_fiat.button(
    text=cfg.bot_currency[1],
    callback_data=cl_m.Advertisements_p2p_fiat(action='select_balance_currency', value='1')
)
builder_adv_p2p_fiat.button(
    text=cfg.bot_currency[2],
    callback_data=cl_m.Advertisements_p2p_fiat(action='select_balance_currency', value='2')
)
builder_adv_p2p_fiat.button(
    text=cfg.bot_currency[3],
    callback_data=cl_m.Advertisements_p2p_fiat(action='select_balance_currency', value='3')
)
builder_adv_p2p_fiat.button(
    text=cfg.bot_currency[4],
    callback_data=cl_m.Advertisements_p2p_fiat(action='select_balance_currency', value='4')
)
builder_adv_p2p_fiat.button(
    text=cfg.bot_currency[5],
    callback_data=cl_m.Advertisements_p2p_fiat(action='select_balance_currency', value='5')
)
builder_adv_p2p_fiat.button(
    text=cfg.bot_currency[6],
    callback_data=cl_m.Advertisements_p2p_fiat(action='select_balance_currency', value='6')
)
builder_adv_p2p_fiat.button(
    text=cfg.bot_currency[7],
    callback_data=cl_m.Advertisements_p2p_fiat(action='select_balance_currency', value='7')
)
builder_adv_p2p_fiat.button(
    text=cfg.bot_currency[8],
    callback_data=cl_m.Advertisements_p2p_fiat(action='select_balance_currency', value='8')
)
builder_adv_p2p_fiat.button(
    text=cfg.bot_currency[9],
    callback_data=cl_m.Advertisements_p2p_fiat(action='select_balance_currency', value='9')
)
builder_adv_p2p_fiat.button(
    text=cfg.bot_currency[10],
    callback_data=cl_m.Advertisements_p2p_fiat(action='select_balance_currency', value='10')
)
builder_adv_p2p_fiat.button(
    text=cfg.bot_currency[11],
    callback_data=cl_m.Advertisements_p2p_fiat(action='select_balance_currency', value='11')
)
builder_adv_p2p_fiat.button(
    text=cfg.bot_currency[12],
    callback_data=cl_m.Advertisements_p2p_fiat(action='select_balance_currency', value='12')
)
builder_adv_p2p_fiat.button(
    text=cfg.bot_currency[13],
    callback_data=cl_m.Advertisements_p2p_fiat(action='select_balance_currency', value='13')
)
builder_adv_p2p_fiat.button(
    text=cfg.bot_currency[14],
    callback_data=cl_m.Advertisements_p2p_fiat(action='select_balance_currency', value='14')
)
builder_adv_p2p_fiat.button(
    text=cfg.bot_currency[15],
    callback_data=cl_m.Advertisements_p2p_fiat(action='select_balance_currency', value='15')
)
builder_adv_p2p_fiat.button(
    text=cfg.bot_currency[16],
    callback_data=cl_m.Advertisements_p2p_fiat(action='select_balance_currency', value='16')
)
builder_adv_p2p_fiat.button(
    text=cfg.bot_currency[17],
    callback_data=cl_m.Advertisements_p2p_fiat(action='select_balance_currency', value='17')
)
builder_adv_p2p_fiat.button(
    text=cfg.lang_ru['back'],
    callback_data='p2p_create_buy'
)
builder_adv_p2p_fiat.adjust(3)
builder_adv_p2p_fiat.as_markup()

p2p_bank_fix_curr = InlineKeyboardButton(
    text=f'• {cfg.lang_ru['fix']} •',
    callback_data='p2p_bank_fix'
)
p2p_bank_fix = InlineKeyboardButton(
    text=cfg.lang_ru['fix'],
    callback_data='p2p_bank_fix'
)
p2p_bank_floating_curr = InlineKeyboardButton(
    text=f'• {cfg.lang_ru['floating']} •',
    callback_data='p2p_bank_floating'
)
p2p_bank_floating = InlineKeyboardButton(
    text=cfg.lang_ru['floating'],
    callback_data='p2p_bank_floating'
)
p2p_bank_back = InlineKeyboardButton(
    text=cfg.lang_ru['back'],
    callback_data='p2p_create_buy'
)
p2p_bank_next = InlineKeyboardButton(
    text='Продолжить',
    callback_data='p2p_bank_next'
)
inline_p2p_bank_2_fix = [[p2p_bank_fix_curr, p2p_bank_floating], [p2p_bank_next], [p2p_bank_back]]
inline_p2p_bank_2_fix_menu = InlineKeyboardMarkup(inline_keyboard=inline_p2p_bank_2_fix)
inline_p2p_bank_2_floating = [[p2p_bank_fix, p2p_bank_floating_curr], [p2p_bank_next], [p2p_bank_back]]
inline_p2p_bank_2_floating_menu = InlineKeyboardMarkup(inline_keyboard=inline_p2p_bank_2_floating)

p2p_bank_back = InlineKeyboardButton(
    text=cfg.lang_ru['back'],
    callback_data='p2p_create'
)
inline_p2p_bank_2_2 = [[p2p_bank_back]]
inline_p2p_bank_2_2_menu = InlineKeyboardMarkup(inline_keyboard=inline_p2p_bank_2_2)

banks = [
    [
        InlineKeyboardButton(text=cfg.banks[0], callback_data=cl_m.Banks(action=f'select_bank_1', value='0', page=0).pack()),
        InlineKeyboardButton(text=cfg.banks[1], callback_data=cl_m.Banks(action=f'select_bank_1', value='1', page=0).pack()),
        InlineKeyboardButton(text=cfg.banks[2], callback_data=cl_m.Banks(action=f'select_bank_1', value='2', page=0).pack()),
        InlineKeyboardButton(text=cfg.banks[3], callback_data=cl_m.Banks(action=f'select_bank_1', value='3', page=0).pack()),
        InlineKeyboardButton(text=cfg.banks[4], callback_data=cl_m.Banks(action=f'select_bank_1', value='4', page=0).pack()),
        InlineKeyboardButton(text=cfg.banks[5], callback_data=cl_m.Banks(action=f'select_bank_1', value='5', page=0).pack()),
        InlineKeyboardButton(text=cfg.banks[6], callback_data=cl_m.Banks(action=f'select_bank_1', value='6', page=0).pack()),
        InlineKeyboardButton(text=cfg.banks[7], callback_data=cl_m.Banks(action=f'select_bank_1', value='7', page=0).pack()),
        InlineKeyboardButton(text=cfg.banks[8], callback_data=cl_m.Banks(action=f'select_bank_1', value='8', page=0).pack()),
        InlineKeyboardButton(text=cfg.banks[9], callback_data=cl_m.Banks(action=f'select_bank_1', value='9', page=0).pack())
    ],
    [
        InlineKeyboardButton(text=cfg.banks[10], callback_data=cl_m.Banks(action=f'select_bank_1', value='10', page=1).pack()),
        InlineKeyboardButton(text=cfg.banks[11], callback_data=cl_m.Banks(action=f'select_bank_1', value='11', page=1).pack()),
        InlineKeyboardButton(text=cfg.banks[12], callback_data=cl_m.Banks(action=f'select_bank_1', value='12', page=1).pack()),
        InlineKeyboardButton(text=cfg.banks[13], callback_data=cl_m.Banks(action=f'select_bank_1', value='13', page=1).pack()),
        InlineKeyboardButton(text=cfg.banks[14], callback_data=cl_m.Banks(action=f'select_bank_1', value='14', page=1).pack()),
        InlineKeyboardButton(text=cfg.banks[15], callback_data=cl_m.Banks(action=f'select_bank_1', value='15', page=1).pack()),
        InlineKeyboardButton(text=cfg.banks[16], callback_data=cl_m.Banks(action=f'select_bank_1', value='16', page=1).pack()),
        InlineKeyboardButton(text=cfg.banks[17], callback_data=cl_m.Banks(action=f'select_bank_1', value='17', page=1).pack()),
        InlineKeyboardButton(text=cfg.banks[18], callback_data=cl_m.Banks(action=f'select_bank_1', value='18', page=1).pack()),
        InlineKeyboardButton(text=cfg.banks[19], callback_data=cl_m.Banks(action=f'select_bank_1', value='19', page=1).pack())
    ],
    [
        InlineKeyboardButton(text=cfg.banks[20], callback_data=cl_m.Banks(action=f'select_bank_1', value='20', page=2).pack()),
        InlineKeyboardButton(text=cfg.banks[21], callback_data=cl_m.Banks(action=f'select_bank_1', value='21', page=2).pack()),
        InlineKeyboardButton(text=cfg.banks[22], callback_data=cl_m.Banks(action=f'select_bank_1', value='22', page=2).pack()),
        InlineKeyboardButton(text=cfg.banks[23], callback_data=cl_m.Banks(action=f'select_bank_1', value='23', page=2).pack()),
        InlineKeyboardButton(text=cfg.banks[24], callback_data=cl_m.Banks(action=f'select_bank_1', value='24', page=2).pack()),
        InlineKeyboardButton(text=cfg.banks[25], callback_data=cl_m.Banks(action=f'select_bank_1', value='25', page=2).pack()),
        InlineKeyboardButton(text=cfg.banks[26], callback_data=cl_m.Banks(action=f'select_bank_1', value='26', page=2).pack()),
        InlineKeyboardButton(text=cfg.banks[27], callback_data=cl_m.Banks(action=f'select_bank_1', value='27', page=2).pack()),
        InlineKeyboardButton(text=cfg.banks[28], callback_data=cl_m.Banks(action=f'select_bank_1', value='28', page=2).pack())
    ]
]

banks_2 = [
    [
        InlineKeyboardButton(text=cfg.banks[0], callback_data=cl_m.Banks(action=f'select_bank_2', value='0', page=0).pack()),
        InlineKeyboardButton(text=cfg.banks[1], callback_data=cl_m.Banks(action=f'select_bank_2', value='1', page=0).pack()),
        InlineKeyboardButton(text=cfg.banks[2], callback_data=cl_m.Banks(action=f'select_bank_2', value='2', page=0).pack()),
        InlineKeyboardButton(text=cfg.banks[3], callback_data=cl_m.Banks(action=f'select_bank_2', value='3', page=0).pack()),
        InlineKeyboardButton(text=cfg.banks[4], callback_data=cl_m.Banks(action=f'select_bank_2', value='4', page=0).pack()),
        InlineKeyboardButton(text=cfg.banks[5], callback_data=cl_m.Banks(action=f'select_bank_2', value='5', page=0).pack()),
        InlineKeyboardButton(text=cfg.banks[6], callback_data=cl_m.Banks(action=f'select_bank_2', value='6', page=0).pack()),
        InlineKeyboardButton(text=cfg.banks[7], callback_data=cl_m.Banks(action=f'select_bank_2', value='7', page=0).pack()),
        InlineKeyboardButton(text=cfg.banks[8], callback_data=cl_m.Banks(action=f'select_bank_2', value='8', page=0).pack()),
        InlineKeyboardButton(text=cfg.banks[9], callback_data=cl_m.Banks(action=f'select_bank_2', value='9', page=0).pack())
    ],
    [
        InlineKeyboardButton(text=cfg.banks[10], callback_data=cl_m.Banks(action=f'select_bank_2', value='10', page=1).pack()),
        InlineKeyboardButton(text=cfg.banks[11], callback_data=cl_m.Banks(action=f'select_bank_2', value='11', page=1).pack()),
        InlineKeyboardButton(text=cfg.banks[12], callback_data=cl_m.Banks(action=f'select_bank_2', value='12', page=1).pack()),
        InlineKeyboardButton(text=cfg.banks[13], callback_data=cl_m.Banks(action=f'select_bank_2', value='13', page=1).pack()),
        InlineKeyboardButton(text=cfg.banks[14], callback_data=cl_m.Banks(action=f'select_bank_2', value='14', page=1).pack()),
        InlineKeyboardButton(text=cfg.banks[15], callback_data=cl_m.Banks(action=f'select_bank_2', value='15', page=1).pack()),
        InlineKeyboardButton(text=cfg.banks[16], callback_data=cl_m.Banks(action=f'select_bank_2', value='16', page=1).pack()),
        InlineKeyboardButton(text=cfg.banks[17], callback_data=cl_m.Banks(action=f'select_bank_2', value='17', page=1).pack()),
        InlineKeyboardButton(text=cfg.banks[18], callback_data=cl_m.Banks(action=f'select_bank_2', value='18', page=1).pack()),
        InlineKeyboardButton(text=cfg.banks[19], callback_data=cl_m.Banks(action=f'select_bank_2', value='19', page=1).pack())
    ],
    [
        InlineKeyboardButton(text=cfg.banks[20], callback_data=cl_m.Banks(action=f'select_bank_2', value='20', page=2).pack()),
        InlineKeyboardButton(text=cfg.banks[21], callback_data=cl_m.Banks(action=f'select_bank_2', value='21', page=2).pack()),
        InlineKeyboardButton(text=cfg.banks[22], callback_data=cl_m.Banks(action=f'select_bank_2', value='22', page=2).pack()),
        InlineKeyboardButton(text=cfg.banks[23], callback_data=cl_m.Banks(action=f'select_bank_2', value='23', page=2).pack()),
        InlineKeyboardButton(text=cfg.banks[24], callback_data=cl_m.Banks(action=f'select_bank_2', value='24', page=2).pack()),
        InlineKeyboardButton(text=cfg.banks[25], callback_data=cl_m.Banks(action=f'select_bank_2', value='25', page=2).pack()),
        InlineKeyboardButton(text=cfg.banks[26], callback_data=cl_m.Banks(action=f'select_bank_2', value='26', page=2).pack()),
        InlineKeyboardButton(text=cfg.banks[27], callback_data=cl_m.Banks(action=f'select_bank_2', value='27', page=2).pack()),
        InlineKeyboardButton(text=cfg.banks[28], callback_data=cl_m.Banks(action=f'select_bank_2', value='28', page=2).pack())
    ]
]

banks_3 = [
    [
        InlineKeyboardButton(text=cfg.banks[0], callback_data=cl_m.Banks(action=f'select_bank_3', value='0', page=0).pack()),
        InlineKeyboardButton(text=cfg.banks[1], callback_data=cl_m.Banks(action=f'select_bank_3', value='1', page=0).pack()),
        InlineKeyboardButton(text=cfg.banks[2], callback_data=cl_m.Banks(action=f'select_bank_3', value='2', page=0).pack()),
        InlineKeyboardButton(text=cfg.banks[3], callback_data=cl_m.Banks(action=f'select_bank_3', value='3', page=0).pack()),
        InlineKeyboardButton(text=cfg.banks[4], callback_data=cl_m.Banks(action=f'select_bank_3', value='4', page=0).pack()),
        InlineKeyboardButton(text=cfg.banks[5], callback_data=cl_m.Banks(action=f'select_bank_3', value='5', page=0).pack()),
        InlineKeyboardButton(text=cfg.banks[6], callback_data=cl_m.Banks(action=f'select_bank_3', value='6', page=0).pack()),
        InlineKeyboardButton(text=cfg.banks[7], callback_data=cl_m.Banks(action=f'select_bank_3', value='7', page=0).pack()),
        InlineKeyboardButton(text=cfg.banks[8], callback_data=cl_m.Banks(action=f'select_bank_3', value='8', page=0).pack()),
        InlineKeyboardButton(text=cfg.banks[9], callback_data=cl_m.Banks(action=f'select_bank_3', value='9', page=0).pack())
    ],
    [
        InlineKeyboardButton(text=cfg.banks[10], callback_data=cl_m.Banks(action=f'select_bank_3', value='10', page=1).pack()),
        InlineKeyboardButton(text=cfg.banks[11], callback_data=cl_m.Banks(action=f'select_bank_3', value='11', page=1).pack()),
        InlineKeyboardButton(text=cfg.banks[12], callback_data=cl_m.Banks(action=f'select_bank_3', value='12', page=1).pack()),
        InlineKeyboardButton(text=cfg.banks[13], callback_data=cl_m.Banks(action=f'select_bank_3', value='13', page=1).pack()),
        InlineKeyboardButton(text=cfg.banks[14], callback_data=cl_m.Banks(action=f'select_bank_3', value='14', page=1).pack()),
        InlineKeyboardButton(text=cfg.banks[15], callback_data=cl_m.Banks(action=f'select_bank_3', value='15', page=1).pack()),
        InlineKeyboardButton(text=cfg.banks[16], callback_data=cl_m.Banks(action=f'select_bank_3', value='16', page=1).pack()),
        InlineKeyboardButton(text=cfg.banks[17], callback_data=cl_m.Banks(action=f'select_bank_3', value='17', page=1).pack()),
        InlineKeyboardButton(text=cfg.banks[18], callback_data=cl_m.Banks(action=f'select_bank_3', value='18', page=1).pack()),
        InlineKeyboardButton(text=cfg.banks[19], callback_data=cl_m.Banks(action=f'select_bank_3', value='19', page=1).pack())
    ],
    [
        InlineKeyboardButton(text=cfg.banks[20], callback_data=cl_m.Banks(action=f'select_bank_3', value='20', page=2).pack()),
        InlineKeyboardButton(text=cfg.banks[21], callback_data=cl_m.Banks(action=f'select_bank_3', value='21', page=2).pack()),
        InlineKeyboardButton(text=cfg.banks[22], callback_data=cl_m.Banks(action=f'select_bank_3', value='22', page=2).pack()),
        InlineKeyboardButton(text=cfg.banks[23], callback_data=cl_m.Banks(action=f'select_bank_3', value='23', page=2).pack()),
        InlineKeyboardButton(text=cfg.banks[24], callback_data=cl_m.Banks(action=f'select_bank_3', value='24', page=2).pack()),
        InlineKeyboardButton(text=cfg.banks[25], callback_data=cl_m.Banks(action=f'select_bank_3', value='25', page=2).pack()),
        InlineKeyboardButton(text=cfg.banks[26], callback_data=cl_m.Banks(action=f'select_bank_3', value='26', page=2).pack()),
        InlineKeyboardButton(text=cfg.banks[27], callback_data=cl_m.Banks(action=f'select_bank_3', value='27', page=2).pack()),
        InlineKeyboardButton(text=cfg.banks[28], callback_data=cl_m.Banks(action=f'select_bank_3', value='28', page=2).pack())
    ]
]

builder_buytime = InlineKeyboardBuilder()
builder_buytime.button(
    text='15 минут',
    callback_data=cl_m.Buy_time(action='select_time_buy', time=15)
)
builder_buytime.button(
    text='30 минут',
    callback_data=cl_m.Buy_time(action='select_time_buy', time=30)
)
builder_buytime.button(
    text='1 час',
    callback_data=cl_m.Buy_time(action='select_time_buy', time=60)
)
builder_buytime.button(
    text=cfg.lang_ru['back'],
    callback_data='p2p_bank_next'
)
builder_buytime.adjust(3)
builder_buytime.as_markup()

p2p_buy_curr = InlineKeyboardButton(
    text='Создать объявление',
    callback_data='p2p_create_buy_curr'
)
p2p_buy_curr_back = InlineKeyboardButton(
    text='Назад',
    callback_data='p2p_buy_time'
)
inline_p2p_buy_curr = [[p2p_buy_curr], [p2p_buy_curr_back]]
inline_p2p_buy_curr_menu = InlineKeyboardMarkup(inline_keyboard=inline_p2p_buy_curr)

p2p_buy_curr_2 = InlineKeyboardButton(
    text='Опубликовать',
    callback_data='p2p_create_announcement_buy'
)
p2p_buy_curr_back_2 = InlineKeyboardButton(
    text=cfg.lang_ru['back'],
    callback_data='p2p_buy_time'
)
inline_p2p_buy_curr_2 = [[p2p_buy_curr_2], [p2p_buy_curr_back_2]]
inline_p2p_buy_curr_menu_2 = InlineKeyboardMarkup(inline_keyboard=inline_p2p_buy_curr_2)

p2p_withdrawn_adv = InlineKeyboardButton(
    text='Снять с публикации',
    callback_data='p2p_withdrawn_adv'
)
p2p_withdrawn_adv_1 = InlineKeyboardButton(
    text='Отправить на публикацию',
    callback_data='p2p_withdrawn_adv_1'
)
p2p_count = InlineKeyboardButton(
    text='Цена',
    callback_data='p2p_buy_fix_edit'
)
p2p_limits = InlineKeyboardButton(
    text='Лимиты',
    callback_data='p2p_limits_edit'
)
p2p_payment = InlineKeyboardButton(
    text='Способы оплаты',
    callback_data='p2p_banks_edit'
)
p2p_time = InlineKeyboardButton(
    text='Срок оплаты',
    callback_data='p2p_time_edit'
)
p2p_conditions = InlineKeyboardButton(
    text='Условия сделки',
    callback_data='p2p_conditions'
)
p2p_delete_adv = InlineKeyboardButton(
    text='Удалить объявление',
    callback_data='delete_adv'
)
p2p_back_adv = InlineKeyboardButton(
    text='Назад к объявлениям',
    callback_data='my_advertisements'
)

inline_p2p_buy_curr_3 = [[p2p_withdrawn_adv], [p2p_count], [p2p_limits], [p2p_payment], [p2p_time], [p2p_conditions],
                         [p2p_delete_adv], [p2p_back_adv]]
inline_p2p_buy_curr_menu_3 = InlineKeyboardMarkup(inline_keyboard=inline_p2p_buy_curr_3)

inline_p2p_buy_curr_3_1 = [[p2p_withdrawn_adv_1], [p2p_count], [p2p_limits], [p2p_payment], [p2p_time], [p2p_conditions],
                         [p2p_delete_adv], [p2p_back_adv]]
inline_p2p_buy_curr_menu_3_1 = InlineKeyboardMarkup(inline_keyboard=inline_p2p_buy_curr_3_1)

p2p_conditions_back = InlineKeyboardButton(
    text='Назад',
    callback_data='back_adv_edit_2'
)

inline_p2p_conditions = [[p2p_conditions_back]]
inline_p2p_conditions_menu_ = InlineKeyboardMarkup(inline_keyboard=inline_p2p_conditions)

builder_time_edit = InlineKeyboardBuilder()
builder_time_edit.button(
    text='15 минут',
    callback_data=cl_m.Buy_time_edit(action='select_time_buy', time=15)
)
builder_time_edit.button(
    text='30 минут',
    callback_data=cl_m.Buy_time_edit(action='select_time_buy', time=30)
)
builder_time_edit.button(
    text='1 час',
    callback_data=cl_m.Buy_time_edit(action='select_time_buy', time=60)
)
builder_time_edit.button(
    text=cfg.lang_ru['back'],
    callback_data='back_adv_edit_2'
)
builder_time_edit.adjust(3)
builder_time_edit.as_markup()


p2p_delete_adv_edit = InlineKeyboardButton(
    text='Удалить объявление',
    callback_data='delete_adv_edit'
)
p2p_back_adv_edit = InlineKeyboardButton(
    text='Назад к объявлениям',
    callback_data='my_advertisements'
)

inline_p2p_delete_adv = [[p2p_delete_adv_edit], [p2p_back_adv_edit]]
inline_p2p_delete_adv_menu = InlineKeyboardMarkup(inline_keyboard=inline_p2p_delete_adv)

p2p_back_adv_edit_2 = InlineKeyboardButton(
    text='Назад к объявлениям',
    callback_data='my_advertisements'
)

inline_p2p_delete_adv_2 = [[p2p_back_adv_edit]]
inline_p2p_delete_adv_menu_2 = InlineKeyboardMarkup(inline_keyboard=inline_p2p_delete_adv_2)



p2p_fix_curr_edit = InlineKeyboardButton(
    text=f'• {cfg.lang_ru['fix']} •',
    callback_data='p2p_buy_fix_edit'
)
p2p_fix_edit = InlineKeyboardButton(
    text=cfg.lang_ru['fix'],
    callback_data='p2p_buy_fix_edit'
)
p2p_floating_curr_edit = InlineKeyboardButton(
    text=f'• {cfg.lang_ru['floating']} •',
    callback_data='p2p_bank_floating_edit'
)
p2p_floating_edit = InlineKeyboardButton(
    text=cfg.lang_ru['floating'],
    callback_data='p2p_bank_floating_edit'
)
p2p_next_edit = InlineKeyboardButton(
    text='Продолжить',
    callback_data='back_adv_edit_2'
)
inline_p2p_fix_edit = [[p2p_fix_curr_edit, p2p_floating_edit], [p2p_next_edit]]
inline_p2p_fix_menu_edit = InlineKeyboardMarkup(inline_keyboard=inline_p2p_fix_edit)
inline_p2p_floating_edit = [[p2p_fix_edit, p2p_floating_curr_edit], [p2p_next_edit]]
inline_p2p_floating_menu_edit = InlineKeyboardMarkup(inline_keyboard=inline_p2p_floating_edit)


builder_crypt_p2p = InlineKeyboardBuilder()
builder_crypt_p2p.button(
    text=cfg.coins_index[0],
    callback_data=cl_m.Advertisements_p2p(action='select_balance_currency_2', value='0')
)
builder_crypt_p2p.button(
    text=cfg.coins_index[1],
    callback_data=cl_m.Advertisements_p2p(action='select_balance_currency_2', value='1')
)
builder_crypt_p2p.button(
    text=cfg.coins_index[2],
    callback_data=cl_m.Advertisements_p2p(action='select_balance_currency_2', value='2')
)
builder_crypt_p2p.button(
    text=cfg.coins_index[3],
    callback_data=cl_m.Advertisements_p2p(action='select_balance_currency_2', value='3')
)
builder_crypt_p2p.button(
    text=cfg.coins_index[4],
    callback_data=cl_m.Advertisements_p2p(action='select_balance_currency_2', value='4')
)
builder_crypt_p2p.button(
    text=cfg.coins_index[5],
    callback_data=cl_m.Advertisements_p2p(action='select_balance_currency_2', value='5')
)
builder_crypt_p2p.button(
    text=cfg.coins_index[6],
    callback_data=cl_m.Advertisements_p2p(action='select_balance_currency_2', value='6')
)
builder_crypt_p2p.button(
    text=cfg.coins_index[7],
    callback_data=cl_m.Advertisements_p2p(action='select_balance_currency_2', value='7')
)
builder_crypt_p2p.button(
    text=cfg.coins_index[8],
    callback_data=cl_m.Advertisements_p2p(action='select_balance_currency_2', value='8')
)
builder_crypt_p2p.button(
    text=cfg.coins_index[9],
    callback_data=cl_m.Advertisements_p2p(action='select_balance_currency_2', value='9')
)
builder_crypt_p2p.button(
    text=cfg.lang_ru['back'],
    callback_data='back_p2p_menu'
)
builder_crypt_p2p.adjust(3)
builder_crypt_p2p.as_markup()

builder_buy_p2p_fiat = InlineKeyboardBuilder()
builder_buy_p2p_fiat.button(
    text=cfg.bot_currency[0],
    callback_data=cl_m.Advertisements_p2p(action='select_balance_currency_3', value='0')
)
builder_buy_p2p_fiat.button(
    text=cfg.bot_currency[1],
    callback_data=cl_m.Advertisements_p2p(action='select_balance_currency_3', value='1')
)
builder_buy_p2p_fiat.button(
    text=cfg.bot_currency[2],
    callback_data=cl_m.Advertisements_p2p(action='select_balance_currency_3', value='2')
)
builder_buy_p2p_fiat.button(
    text=cfg.bot_currency[3],
    callback_data=cl_m.Advertisements_p2p(action='select_balance_currency_3', value='3')
)
builder_buy_p2p_fiat.button(
    text=cfg.bot_currency[4],
    callback_data=cl_m.Advertisements_p2p(action='select_balance_currency_3', value='4')
)
builder_buy_p2p_fiat.button(
    text=cfg.bot_currency[5],
    callback_data=cl_m.Advertisements_p2p(action='select_balance_currency_3', value='5')
)
builder_buy_p2p_fiat.button(
    text=cfg.bot_currency[6],
    callback_data=cl_m.Advertisements_p2p(action='select_balance_currency_3', value='6')
)
builder_buy_p2p_fiat.button(
    text=cfg.bot_currency[7],
    callback_data=cl_m.Advertisements_p2p(action='select_balance_currency_3', value='7')
)
builder_buy_p2p_fiat.button(
    text=cfg.bot_currency[8],
    callback_data=cl_m.Advertisements_p2p(action='select_balance_currency_3', value='8')
)
builder_buy_p2p_fiat.button(
    text=cfg.bot_currency[9],
    callback_data=cl_m.Advertisements_p2p(action='select_balance_currency_3', value='9')
)
builder_buy_p2p_fiat.button(
    text=cfg.bot_currency[10],
    callback_data=cl_m.Advertisements_p2p(action='select_balance_currency_3', value='10')
)
builder_buy_p2p_fiat.button(
    text=cfg.bot_currency[11],
    callback_data=cl_m.Advertisements_p2p(action='select_balance_currency_3', value='11')
)
builder_buy_p2p_fiat.button(
    text=cfg.bot_currency[12],
    callback_data=cl_m.Advertisements_p2p(action='select_balance_currency_3', value='12')
)
builder_buy_p2p_fiat.button(
    text=cfg.bot_currency[13],
    callback_data=cl_m.Advertisements_p2p(action='select_balance_currency_3', value='13')
)
builder_buy_p2p_fiat.button(
    text=cfg.bot_currency[14],
    callback_data=cl_m.Advertisements_p2p(action='select_balance_currency_3', value='14')
)
builder_buy_p2p_fiat.button(
    text=cfg.bot_currency[15],
    callback_data=cl_m.Advertisements_p2p(action='select_balance_currency_3', value='15')
)
builder_buy_p2p_fiat.button(
    text=cfg.bot_currency[16],
    callback_data=cl_m.Advertisements_p2p(action='select_balance_currency_3', value='16')
)
builder_buy_p2p_fiat.button(
    text=cfg.bot_currency[17],
    callback_data=cl_m.Advertisements_p2p(action='select_balance_currency_3', value='17')
)
builder_buy_p2p_fiat.button(
    text=cfg.lang_ru['back'],
    callback_data='back_p2p_menu'
)
builder_buy_p2p_fiat.adjust(3)
builder_buy_p2p_fiat.as_markup()


p2p_buy_create = InlineKeyboardButton(
    text='Купить',
    callback_data='p2p_buy_create'
)
p2p_back_adv_2 = InlineKeyboardButton(
    text=cfg.lang_ru['back'],
    callback_data='back_p2p_menu'
)
inline_p2p_buy_create = [[p2p_buy_create], [p2p_back_adv_2]]
inline_p2p_buy_create_menu = InlineKeyboardMarkup(inline_keyboard=inline_p2p_buy_create)

p2p_back_active = InlineKeyboardButton(
    text=cfg.lang_ru['back'],
    callback_data='p2p_active_trades'
)
inline_p2p_active = [[p2p_back_active]]
inline_p2p_active_menu = InlineKeyboardMarkup(inline_keyboard=inline_p2p_active)

p2p_buy_create_fiat = InlineKeyboardButton(
    text='Указать в валюте',
    callback_data='p2p_buy_create_fiat'
)
p2p_back_adv_2_fiat = InlineKeyboardButton(
    text='Назад к объявлениям',
    callback_data='my_advertisements'
)
inline_p2p_buy_create_fiat = [[p2p_buy_create_fiat], [p2p_back_adv_2]]
inline_p2p_buy_create_fiat_menu = InlineKeyboardMarkup(inline_keyboard=inline_p2p_buy_create_fiat)

p2p_buy_create_2 = InlineKeyboardButton(
    text='Указать в крипте',
    callback_data='p2p_buy_create'
)
inline_p2p_buy_create_2 = [[p2p_buy_create_2], [p2p_back_adv_2]]
inline_p2p_buy_create_2_menu = InlineKeyboardMarkup(inline_keyboard=inline_p2p_buy_create_2)

p2p_buy_create_fin = InlineKeyboardButton(
    text='Создать сделку',
    callback_data='p2p_buy_create_fin'
)
inline_p2p_buy_create_fin = [[p2p_buy_create_fin], [p2p_back_adv_2]]
inline_p2p_buy_create_fin_menu = InlineKeyboardMarkup(inline_keyboard=inline_p2p_buy_create_fin)

p2p_sell_create_fin = InlineKeyboardButton(
    text='Создать сделку',
    callback_data='p2p_sell_create_fin'
)

inline_p2p_sell_create_fin = [[p2p_sell_create_fin], [p2p_back_adv_2]]
inline_p2p_sell_create_fin_menu = InlineKeyboardMarkup(inline_keyboard=inline_p2p_sell_create_fin)

p2p_buy_cancel = InlineKeyboardButton(
    text='Отменить сделку',
    callback_data='p2p_buy_cancel'
)
p2p_active_trade = InlineKeyboardButton(
    text='К списку активных сделок',
    callback_data='p2p_active_trade'
)
p2p_active_trade_acc = InlineKeyboardButton(
    text='Подтвердить сделку',
    callback_data='p2p_active_trade_acc'
)
inline_p2p_buy_create_fin_2 = [[p2p_buy_cancel], [p2p_active_trade]]
inline_p2p_buy_create_fin_2_menu = InlineKeyboardMarkup(inline_keyboard=inline_p2p_buy_create_fin_2)

inline_p2p_arv_acc = [[p2p_active_trade_acc], [p2p_buy_cancel]]
inline_p2p_arv_acc_menu = InlineKeyboardMarkup(inline_keyboard=inline_p2p_arv_acc)


p2p_sell_create = InlineKeyboardButton(
    text='Продать',
    callback_data='p2p_buy_create'
)
p2p_back_adv_2 = InlineKeyboardButton(
    text=cfg.lang_ru['back'],
    callback_data='my_advertisements'
)
inline_p2p_sell_create = [[p2p_sell_create], [p2p_back_adv_2]]
inline_p2p_sell_create_menu = InlineKeyboardMarkup(inline_keyboard=inline_p2p_sell_create)

p2p_rep_plus = InlineKeyboardButton(
    text='👍',
    callback_data='p2p_rep_plus'
)
p2p_rep_minus = InlineKeyboardButton(
    text='👎',
    callback_data='p2p_rep_minus'
)
inline_p2p_rep = [[p2p_rep_plus, p2p_rep_minus]]
inline_p2p_rep_menu = InlineKeyboardMarkup(inline_keyboard=inline_p2p_rep)


btn_p2p_back_active = InlineKeyboardButton(
    text='◀️ Назад',
    callback_data='back_p2p_menu'
)
inline_p2p_active_none = [[btn_p2p_back_active]]
inline_p2p_active_none_menu = InlineKeyboardMarkup(inline_keyboard=inline_p2p_active_none)


change_couse_back = InlineKeyboardButton(
    text='Назад',
    callback_data='adm_back'
)
inline_change_couse = [[change_couse_back]]
inline_change_couse_menu = InlineKeyboardMarkup(inline_keyboard=inline_change_couse)

change_couse = InlineKeyboardButton(
    text='Изменить курс',
    callback_data='change_couse'
)
course = InlineKeyboardButton(
    text='Просмотр курсов',
    callback_data='course'
)
balance_bot = InlineKeyboardButton(
    text='Общий баланс площадки',
    callback_data='balance_bot'
)
sup_tickets = InlineKeyboardButton(
    text='Обращения в поддержку',
    callback_data='p2p_tickets'
)
inline_adm_main = [[change_couse], [course], [balance_bot], [sup_tickets]]
inline_adm_main_menu = InlineKeyboardMarkup(inline_keyboard=inline_adm_main)

inline_balance_main = [[change_couse_back]]
inline_adm_balance_menu = InlineKeyboardMarkup(inline_keyboard=inline_balance_main)

filter_back = InlineKeyboardButton(
    text='Назад',
    callback_data='p2p_bank_2'
)
inline_p2p_filter_back = [[filter_back]]
inline_p2p_filter_back_menu = InlineKeyboardMarkup(inline_keyboard=inline_p2p_filter_back)


change_couse2 = InlineKeyboardButton(
    text='Изменить еще один курс',
    callback_data='change_couse'
)
change_couse_back = InlineKeyboardButton(
    text='Назад',
    callback_data='adm_back'
)
inline_change_couse_2 = [[change_couse2], [change_couse_back]]
inline_change_couse_2_menu = InlineKeyboardMarkup(inline_keyboard=inline_change_couse_2)

tikets_back = InlineKeyboardButton(
    text='Назад',
    callback_data='p2p_tickets'
)
inline_p2p_tickets_back = [[tikets_back]]
inline_p2p_tickets_back_menu = InlineKeyboardMarkup(inline_keyboard=inline_p2p_tickets_back)

tikets_delete = InlineKeyboardButton(
    text='Удалить обращение',
    callback_data='p2p_tickets_delete'
)
inline_p2p_tickets_delete = [[tikets_delete],[tikets_back]]
inline_p2p_tickets_delete_menu = InlineKeyboardMarkup(inline_keyboard=inline_p2p_tickets_delete)

inline_p2p_course = [[change_couse], [change_couse_back]]
inline_p2p_course_menu = InlineKeyboardMarkup(inline_keyboard=inline_p2p_course)