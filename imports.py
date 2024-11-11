import asyncio, logging, mysql.connector
import re
import string
import random
import numpy as np
import configparser, os
import math
import time
import asyncio
import threading
from aiogram.filters import callback_data
from aiogram.handlers import CallbackQueryHandler
from aiogram import Bot, Dispatcher, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters.command import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from mysql.connector import Error
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, CallbackQuery
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.strategy import FSMStrategy
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters.callback_data import CallbackData
from datetime import datetime, timedelta
from contextlib import suppress
from array import *
from aiogram.exceptions import TelegramBadRequest