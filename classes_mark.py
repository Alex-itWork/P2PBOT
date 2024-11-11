from imports import *

class Coins (CallbackData, prefix='coin'):
    action: str
    value: str


class Balance_currency (CallbackData, prefix='balance'):
    action: str
    value: str


class Advertisements_p2p (CallbackData, prefix='advertisements'):
    action: str
    value: str


class Advertisements_p2p_fiat (CallbackData, prefix='advertisements_fiat'):
    action: str
    value: str

class Banks_1(CallbackData, prefix='banks_1'):
    action: str
    value: str

class Banks(CallbackData, prefix= 'banks'):
    action: str
    value: str
    page: int


class Buy_time(CallbackData, prefix='time'):
    action: str
    time: int


class Buy_time_edit(CallbackData, prefix='time_edit'):
    action: str
    time: int


class Advertisements(CallbackData, prefix='adv'):
    action: str
    number: int