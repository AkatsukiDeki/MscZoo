# main.py
import telebot
from telebot import types
from confiq import TOKEN
from animal_data import animals_dict
from quizy import Quiz  # Импортируем класс викторины
from quizy_data import quiz_questions_classes, quiz_questions_animals, special_questions  # Импортируем вопросы викторины

bot = telebot.TeleBot(TOKEN)
quiz = Quiz()  # Создаем экземпляр класса викторины


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, 'Привет! Я бот, который проведет тебя в удивительный мир Московского зоопарка...')


@bot.message_handler(commands=['help'])
def help(message):
    text = 'Чтобы начать наше приключение, выбери класс животного, используя команду /animals.'
    bot.reply_to(message, text)


@bot.message_handler(commands=['animals'])
def list_animals(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for animal_class in animals_dict.keys():
        keyboard.add(types.KeyboardButton(animal_class))
    bot.reply_to(message, "Выберите класс животных:", reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text in animals_dict)
def choose_animal(message):
    selected_class = message.text
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for animal in animals_dict[selected_class].keys():
        keyboard.add(types.KeyboardButton(animal))
    keyboard.add(types.KeyboardButton("Назад к классам"))
    keyboard.add(types.KeyboardButton("Начать викторину"))
    bot.reply_to(message, f"Вы выбрали класс: {selected_class}. Теперь выберите животное:", reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text == "Начать викторину")
def start_quiz_classes(message):
    quiz.start_quiz_classes(bot, message)


@bot.message_handler(func=lambda message: message.text in [option for question in quiz_questions_classes for option in question["options"]])
def check_class_answer(message):
    dominant_class = quiz.check_class_answer(bot, message)
    if dominant_class:
        quiz.start_quiz_animals(bot, message, dominant_class)


@bot.message_handler(func=lambda message: message.text in [option for question in quiz_questions_animals for option in question["options"]])
def check_animal_answer(message):
    quiz.check_animal_answer(bot, message)


if __name__ == "__main__":
    bot.polling()
