from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import (
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton
)

from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from database import (
    add_user,
    get_users_count,
    sohranit_anketu,
    poluchit_anketu,
    poluchit_vse_ankety,
    kolichestvo_anket,
    udalit_anketu
)

import asyncio

TOKEN = "Сюда токен надо свой не дам:)"

bot = Bot(token=TOKEN)
dp = Dispatcher()

class SozdanieAnkety(StatesGroup):
    tekst = State()
    foto = State()
    strana = State()
    gorod = State()
    pol = State()
    vozrast = State()

glavnoe_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📢 Создать анкету")],
        [KeyboardButton(text="👤 Моя анкета")],
        [KeyboardButton(text="📋 Смотреть анкеты")],
        [KeyboardButton(text="📊 Статистика")]
    ],
    resize_keyboard=True
)

foto_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="⏭ Без фото")]
    ],
    resize_keyboard=True
)

strana_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🇰🇿 Казахстан")]
    ],
    resize_keyboard=True
)

pol_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="👩 Девушки")],
        [KeyboardButton(text="👨 Парни")],
        [KeyboardButton(text="🌍 Любой")]
    ],
    resize_keyboard=True
)

vozrast_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="до 16")],
        [KeyboardButton(text="16-18")],
        [KeyboardButton(text="18-23")],
        [KeyboardButton(text="23+")],
        [KeyboardButton(text="Любой")]
    ],
    resize_keyboard=True
)

@dp.message(Command("start"))
async def start(message: Message):

    add_user(
        message.from_user.id,
        message.from_user.username
    )

    await message.answer(
        "🎉 Добро пожаловать в BooHarikBot!\n\nВыберите действие:",
        reply_markup=glavnoe_menu
    )

@dp.message(F.text == "📊 Статистика")
async def statistika(message: Message):

    await message.answer(
        f"👥 Пользователей: {get_users_count()}\n"
        f"📄 Анкет: {kolichestvo_anket()}"
    )

@dp.message(F.text == "📢 Создать анкету")
async def sozdat_anketu(
    message: Message,
    state: FSMContext
):

    await state.set_state(
        SozdanieAnkety.tekst
    )

    await message.answer(
        "Введите текст для анкеты"
    )

@dp.message(SozdanieAnkety.tekst)
async def poluchit_tekst(
    message: Message,
    state: FSMContext
):

    await state.update_data(
        tekst=message.text
    )

    await state.set_state(
        SozdanieAnkety.foto
    )

    await message.answer(
        "Отправьте фото или нажмите Без фото",
        reply_markup=foto_menu
    )

@dp.message(
    SozdanieAnkety.foto,
    F.text == "⏭ Без фото"
)
async def bez_foto(
    message: Message,
    state: FSMContext
):

    await state.update_data(
        foto=None
    )

    await state.set_state(
        SozdanieAnkety.strana
    )

    await message.answer(
        "Выберите страну",
        reply_markup=strana_menu
    )

@dp.message(
    SozdanieAnkety.foto,
    F.photo
)
async def poluchit_foto(
    message: Message,
    state: FSMContext
):

    foto_id = message.photo[-1].file_id

    await state.update_data(
        foto=foto_id
    )

    await state.set_state(
        SozdanieAnkety.strana
    )

    await message.answer(
        "Выберите страну",
        reply_markup=strana_menu
    )

@dp.message(SozdanieAnkety.strana)
async def poluchit_stranu(
    message: Message,
    state: FSMContext
):

    await state.update_data(
        strana=message.text
    )

    await state.set_state(
        SozdanieAnkety.gorod
    )

    await message.answer(
        "Введите город"
    )

@dp.message(SozdanieAnkety.gorod)
async def poluchit_gorod(
    message: Message,
    state: FSMContext
):

    await state.update_data(
        gorod=message.text
    )

    await state.set_state(
        SozdanieAnkety.pol
    )

    await message.answer(
        "Укажите пол аудитории",
        reply_markup=pol_menu
    )

@dp.message(SozdanieAnkety.pol)
async def poluchit_pol(
    message: Message,
    state: FSMContext
):

    await state.update_data(
        pol=message.text
    )

    await state.set_state(
        SozdanieAnkety.vozrast
    )

    await message.answer(
        "Выберите возраст аудитории",
        reply_markup=vozrast_menu
    )

@dp.message(SozdanieAnkety.vozrast)
async def poluchit_vozrast(
    message: Message,
    state: FSMContext
):

    await state.update_data(
        vozrast=message.text
    )

    dannye = await state.get_data()

    sohranit_anketu(
        message.from_user.id,
        dannye["tekst"],
        dannye["foto"],
        dannye["strana"],
        dannye["gorod"],
        dannye["pol"],
        dannye["vozrast"]
    )

    text = (
        f"📄 Анкета опубликована\n\n"
        f"{dannye['tekst']}\n\n"
        f"🌍 {dannye['strana']}\n"
        f"🏙 {dannye['gorod']}\n"
        f"{dannye['pol']}\n"
        f"{dannye['vozrast']}\n\n"
        f"👁 Просмотров: 0\n"
        f"❤️ Лайков: 0\n"
        f"📌 Статус: Активна"
    )

    if dannye["foto"]:

        await message.answer_photo(
            photo=dannye["foto"],
            caption=text,
            reply_markup=glavnoe_menu
        )

    else:

        await message.answer(
            text,
            reply_markup=glavnoe_menu
        )

    await state.clear()

@dp.message(F.text == "👤 Моя анкета")
async def moya_anketa(message: Message):

    anketa = poluchit_anketu(
        message.from_user.id
    )

    if not anketa:

        await message.answer(
            "У вас пока нет анкеты"
        )

        return

    text = (
        f"📄 Моя анкета\n\n"
        f"{anketa[1]}\n\n"
        f"🌍 {anketa[3]}\n"
        f"🏙 {anketa[4]}\n"
        f"{anketa[5]}\n"
        f"{anketa[6]}\n\n"
        f"👁 Просмотров: {anketa[7]}\n"
        f"❤️ Лайков: {anketa[8]}\n"
        f"📌 Статус: {anketa[9]}"
    )

    if anketa[2]:

        await message.answer_photo(
            photo=anketa[2],
            caption=text
        )

    else:

        await message.answer(text)

@dp.message(F.text == "📋 Смотреть анкеты")
async def smotret_ankety(message: Message):

    ankety = poluchit_vse_ankety()

    if len(ankety) == 0:

        await message.answer(
            "Анкет пока нет"
        )

        return

    moya_id = message.from_user.id

    for anketa in ankety:

        if anketa[0] != moya_id:

            text = (
                f"{anketa[1]}\n\n"
                f"🌍 {anketa[3]}\n"
                f"🏙 {anketa[4]}\n"
                f"{anketa[5]}\n"
                f"{anketa[6]}"
            )

            if anketa[2]:

                await message.answer_photo(
                    photo=anketa[2],
                    caption=text
                )

            else:

                await message.answer(text)

            return

    await message.answer(
        "Подходящих анкет пока нет"
    )

@dp.message()
async def prochie_soobsheniya(message: Message):

    await message.answer(
        "Используйте кнопки меню"
    )

async def main():

    print("BooHarikBot zapushen")

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
