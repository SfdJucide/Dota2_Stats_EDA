import logging
from aiogram import Dispatcher, types, Router, Bot
from aiogram.types import Message
from aiogram.filters import Text
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.command import Command
from aiogram.filters.callback_data import CallbackData

from config_reader import config
import utils


logging.basicConfig(level=logging.INFO)

router = Router()
bot = Bot(token=config.bot_token.get_secret_value())
dp = Dispatcher()


class HeroesCallbackFactory(CallbackData, prefix="hero"):
    hero_id: int

@dp.message(Command("start"))
async def command_start_handler(message: Message) -> None:

    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(
            text='Parse data',
            callback_data='parser'),
        types.InlineKeyboardButton(
            text='Time Statistic',
            callback_data='time_stats'),
        types.InlineKeyboardButton(
            text='Heroes Statistic',
            callback_data='heroes_stats'),
        types.InlineKeyboardButton(
            text='Dire and Radiant info',
            callback_data='teams_stats'),
        width=2
        )

    await message.answer(f"Hello, {message.from_user.full_name}! 🙂\nI'm DOTA 2 Stattistic Bot, Let's look at some stats!!!", reply_markup=builder.as_markup())

@dp.callback_query(Text("heroes_stats"))
async def show_heroes(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(
            text='Strength',
            callback_data='heroes_str'),
        types.InlineKeyboardButton(
            text='Agility',
            callback_data='heroes_agi'),
        types.InlineKeyboardButton(
            text='Intelligence',
            callback_data='heroes_int'),
        types.InlineKeyboardButton(
            text='Universal',
            callback_data='heroes_all'),
        width=2
        )
    
    await callback.message.answer("Choose attribute", reply_markup=builder.as_markup())

@dp.callback_query(Text("heroes_str"))
async def show_heroes(callback: types.CallbackQuery):
    heroes = utils.get_heroes_names('str')
    
    await callback.message.edit_text("Choose hero", reply_markup=heroes_mk(heroes))

@dp.callback_query(Text("heroes_int"))
async def show_heroes(callback: types.CallbackQuery):
    heroes = utils.get_heroes_names('int')
    
    await callback.message.edit_text("Choose hero", reply_markup=heroes_mk(heroes))

@dp.callback_query(Text("heroes_agi"))
async def show_heroes(callback: types.CallbackQuery):
    heroes = utils.get_heroes_names('agi')
    
    await callback.message.edit_text("Choose hero", reply_markup=heroes_mk(heroes))

@dp.callback_query(Text("heroes_all"))
async def show_heroes(callback: types.CallbackQuery):
    heroes = utils.get_heroes_names('all')
    
    await callback.message.edit_text("Choose hero", reply_markup=heroes_mk(heroes))

@dp.callback_query(Text("teams_stats"))
async def text_teams_stats_handler(callback: types.CallbackQuery):
    avg_scores = utils.get_avg_scores()
    winrates = utils.get_teams_winrates()
    await callback.message.answer(f"{avg_scores}\n{winrates}")

@dp.callback_query(Text("time_stats"))
async def text_time_stats_handler(callback: types.CallbackQuery):
    duration = utils.get_avg_duration()
    fb_time = utils.get_avg_first_blood()
    await callback.message.answer(f"Average Match Duration: {duration}\nAverage First Blood Timing: {fb_time}")

@dp.callback_query(Text("parser"))
async def text_parser_handler(callback: types.CallbackQuery):

    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(
            text='Parse data',
            callback_data='parse_games'),
        types.InlineKeyboardButton(
            text='Create tables',
            callback_data='create_tables'),
        types.InlineKeyboardButton(
            text='Insert static data',
            callback_data='insert_data'),
        width=1
        )

    await callback.message.answer(f"Select what to do", reply_markup=builder.as_markup())

@dp.callback_query(Text("parse_games"))
async def text_parse_games_handler(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(
            text='30 Min',
            callback_data='parse_games_30'),
        types.InlineKeyboardButton(
            text='1 Hour',
            callback_data='parse_games_60'),
        types.InlineKeyboardButton(
            text='3 Hours',
            callback_data='parse_games_180'),
        width=2
        )

    await callback.message.answer(f"Choose parsing time", reply_markup=builder.as_markup())

@dp.callback_query(Text("parse_games_30"))
async def text_parse_games_30_handler(callback: types.CallbackQuery):
    rows_num = utils.db.get_matches_number()
    await callback.message.answer(f"Start parsing...\nNRows = {rows_num}")
    try:
        utils.parse_matches(30)
    except:
        pass
    finally:
        rows_num = utils.db.get_matches_number()
        await callback.message.answer(f"Parsing done\nNRows = {rows_num}")

@dp.callback_query(Text("parse_games_60"))
async def text_parse_games_60_handler(callback: types.CallbackQuery):
    rows_num = utils.db.get_matches_number()
    await callback.message.answer(f"Start parsing...\nNRows = {rows_num}")
    try:
        utils.parse_matches(60)
    except:
        pass
    finally:
        rows_num = utils.db.get_matches_number()
        await callback.message.answer(f"Parsing done\nNRows = {rows_num}")

@dp.callback_query(Text("parse_games_180"))
async def text_parse_games_180_handler(callback: types.CallbackQuery):
    rows_num = utils.db.get_matches_number()
    await callback.message.answer(f"Start parsing...\nNRows = {rows_num}")
    try:
        utils.parse_matches(180)
    except:
        pass
    finally:
        rows_num = utils.db.get_matches_number()
        await callback.message.answer(f"Parsing done\nNRows = {rows_num}")

@dp.callback_query(Text("create_tables"))
async def text_create_tables_handler(callback: types.CallbackQuery):
    utils.create_tables()
    await callback.message.answer(f"Tables Created!")

@dp.callback_query(Text("insert_data"))
async def text_insert_data_handler(callback: types.CallbackQuery):
    utils.insert_static_data()
    await callback.message.answer(f"Data inserted!")

def heroes_mk(heroes):
    builder = InlineKeyboardBuilder()
    for hero in heroes:
        builder.button(
            text=f'{hero[1]}',
            callback_data=HeroesCallbackFactory(hero_id=hero[0]),
        )
    builder.adjust(3)

    return builder.as_markup()

@dp.callback_query(HeroesCallbackFactory.filter())
async def callbacks_heroes_fab(callback: types.CallbackQuery, callback_data: HeroesCallbackFactory):
    hero = utils.get_hero_stats(callback_data.hero_id)
    await callback.message.edit_text(f"{hero}")

async def run_bot():
    await dp.start_polling(bot)