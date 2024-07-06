import google.generativeai as genai
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import PIL.Image
from googletrans import Translator
from ocr import image2text

bot = Bot(token="7365783074:AAFxmkvnk-fK9CAEuAQk3EMm-Qg-RDcE3HQ")
dp = Dispatcher(bot)

def uz_to_eng(text):
    # Initialize the translator
    translator = Translator()

    # Translate from Uzbek to English
    translation = translator.translate(text, src='uz', dest='en')

    return translation.text

def eng_to_uz(text):
    translator = Translator()
    translation = translator.translate(text, src='en', dest='uz')
    return translation.text


genai.configure(api_key="AIzaSyBVDDB6cRhJjlcrQNir6wDg2sQmfJpK4lw")

def get_response(image_path):
    try:
        # Open the image file
        img = PIL.Image.open(image_path)

        # Assuming genai.GenerativeModel is used for generating content
        model = genai.GenerativeModel(model_name="gemini-1.5-pro")
        # texti = image2text(image_path)
        # print(texti)
        # eng_text = uz_to_eng(texti)
        # print(eng_text)
        # Generate content from the image
        response = model.generate_content(["what can i write to her? give me such an answer to pleasantly surprise her and so that she will have an even better opinion of me. \nwrite in Uzbek. write 1 short and beautiful sentence", img])
        print(response)
        # Return or print the response
        return response.text

    except Exception as e:
        print(f"Error processing image: {e}")


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer("Salom rasm yuboring!")

@dp.message_handler(content_types=['photo'])
async def handle_photo(message: types.Message):

    file_info = await bot.get_file(message.photo[-1].file_id)
    downloaded_file = await bot.download_file(file_info.file_path)

    with open("chat.jpg", "wb") as f:
        f.write(downloaded_file.read())

    # Get response from Generative AI
    response_text = get_response("chat.jpg")
    print(response_text)
    # Create inline keyboard with two buttons
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton(text="Qaytadan Urinish", callback_data="button1"),
        InlineKeyboardButton(text="Yaxshi", callback_data="button2"),
    )

    await message.reply(response_text, reply_markup=keyboard)


# Callback query handler for inline buttons
@dp.callback_query_handler(lambda callback_query: True)
async def handle_callback(callback_query: types.CallbackQuery):
    if callback_query.data == "button1":
        await callback_query.answer()
        await callback_query.message.answer("Iltimos qaytadan rasm tashang")
    elif callback_query.data == "button2":
        await callback_query.answer()
        await callback_query.message.answer("Xursandmiz:)")


# Regular message handler
@dp.message_handler()
async def handle_message(message: types.Message):
    await message.answer(message.text)


# Start polling
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

