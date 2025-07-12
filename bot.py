from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import Message
from config import BOT_TOKEN, PAYMENT_URL, ADMIN_ID
from forecast import get_forecast

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Простой in-memory список оплативших (в боевом варианте — база данных)
paid_users = set()

@dp.message_handler(commands=['start'])
async def start(message: Message):
    await message.answer("👋 Привет! Я бот, продающий реальные прогнозы на спорт.\n"
                         "Чтобы получить прогноз, нажми /buy")

@dp.message_handler(commands=['buy'])
async def buy(message: Message):
    await message.answer(f"💳 Стоимость прогноза: 100 руб.\n"
                         f"Оплатить можно здесь:\n{PAYMENT_URL}\n\n"
                         f"После оплаты напишите /paid")

@dp.message_handler(commands=['paid'])
async def paid(message: Message):
    if message.from_user.id == ADMIN_ID:
        await message.answer("🛠 Вы админ. Используйте /confirm <user_id> для подтверждения оплаты.")
    else:
        await bot.send_message(ADMIN_ID, f"👤 Пользователь {message.from_user.full_name} (ID: {message.from_user.id}) сообщил об оплате.")
        await message.answer("⏳ Спасибо. После подтверждения оплаты админом вы получите прогноз.")

@dp.message_handler(commands=['confirm'])
async def confirm(message: Message):
    if message.from_user.id != ADMIN_ID:
        return await message.answer("⛔ Нет доступа.")

    try:
        _, user_id = message.text.strip().split()
        user_id = int(user_id)
        paid_users.add(user_id)
        await bot.send_message(user_id, "✅ Оплата подтверждена! Вот ваш прогноз:")
        await bot.send_message(user_id, get_forecast())
        await message.answer("Пользователю отправлен прогноз.")
    except Exception as e:
        await message.answer("⚠ Ошибка. Используйте формат: /confirm <user_id>")

@dp.message_handler(commands=['forecast'])
async def forecast(message: Message):
    if message.from_user.id in paid_users:
        await message.answer(get_forecast())
    else:
        await message.answer("💸 Сначала оплатите прогноз. Введите /buy")
