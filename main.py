import asyncio
import uuid

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from aiogram.types import Message, BotCommand, PreCheckoutQuery, FSInputFile

# Замените 'YOUR_BOT_TOKEN' на токен вашего бота
bot = Bot(token='123:ABC')
dp = Dispatcher()

PROVIDER_TOKEN = '401643678:TEST:78de6c4b-372b-47b9-ad90-e6b48eeea748'
FILENAME = 'Грокаем_алгоритмы_Библиотека_программиста_2022.pdf'

# НЕ РАБОТАЕТ
# @dp.message(Command(commands='inline_pay'))
# async def start(message: Message):
#     kb = InlineKeyboardBuilder()
#     kb.button(text=f"Оплатить 20 ⭐️", pay=True)  # Кнопка с оплатой всегда первая
#     await message.answer('Вам выставлен счет за оплату услуг', reply_markup=kb.as_markup())


@dp.message(Command(commands='create_invoice'))
async def create_invoice(message: Message):
    payment_id = str(uuid.uuid4())  # Идентификатор для платежа

    await message.answer_invoice(
        title='Электронная книга по Python',
        description='Грокаем алгоритмы. Автор: Пудов К.Д.',
        payload=payment_id,
        provider_token=PROVIDER_TOKEN,
        currency='RUB',
        prices=[
            types.LabeledPrice(label='Оплата услуг', amount=29990)
        ]
    )


@dp.pre_checkout_query()
async def process_pre_checkout_query(query: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query_id=query.id, ok=True)


@dp.message(F.successful_payment)
async def success_payment_handler(message: Message):
    await message.answer(text="Спасибо за покупку книги!🤗")
    await message.answer_document(FSInputFile(FILENAME))


async def main():
    main_menu_commands = [
        BotCommand(command='/inline_pay',
                   description='Параметр pay=True'),
        BotCommand(command='/create_invoice',
                   description='Большие возможности')
    ]
    await bot.set_my_commands(main_menu_commands)

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
