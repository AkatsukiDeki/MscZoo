# quizy.py
from telebot import types
from animal_data import animals_dict
from quizy_data import quiz_questions_classes, quiz_questions_animals


class Quiz:
    def __init__(self):
        self.class_scores = {"Млекопитающие": 0, "Птицы": 0, "Рептилии": 0}
        self.animal_scores = {}
        self.dominant_class = None
        self.current_class_question_index = 0  # Индекс текущего вопроса по классам
        self.current_animal_question_index = 0  # Индекс текущего вопроса по животным

    def start_quiz_classes(self, bot, message):
        self.class_scores = {"Млекопитающие": 0, "Птицы": 0, "Рептилии": 0}
        self.current_class_question_index = 0  # Сбросить индекс вопросов
        self.ask_class_question(bot, message)

    def ask_class_question(self, bot, message):
        if self.current_class_question_index < len(quiz_questions_classes):
            question = quiz_questions_classes[self.current_class_question_index]
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            for option in question["options"]:
                keyboard.add(types.KeyboardButton(option))
            bot.reply_to(message, question["question"], reply_markup=keyboard)
        else:
            self.dominant_class = max(self.class_scores, key=self.class_scores.get)
            bot.reply_to(message, f"Ваш класс животного: {self.dominant_class}. Теперь давайте выберем конкретное животное.")

    def check_class_answer(self, bot, message):
        question = quiz_questions_classes[self.current_class_question_index]
        if message.text in question["options"]:
            for cls, points in question["points"].items():
                self.class_scores[cls] += points

        self.current_class_question_index += 1  # Переход к следующему вопросу
        self.ask_class_question(bot, message)

    def start_quiz_animals(self, bot, message, dominant_class):
        self.animal_scores = {animal: 0 for animal in animals_dict[dominant_class].keys()}
        self.current_animal_question_index = 0  # Сбросить индекс вопросов
        self.ask_animal_question(bot, message)

    def ask_animal_question(self, bot, message):
        if self.current_animal_question_index < len(quiz_questions_animals):
            question = quiz_questions_animals[self.current_animal_question_index]
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            for option in question["options"]:
                keyboard.add(types.KeyboardButton(option))
            bot.reply_to(message, question["question"], reply_markup=keyboard)
        else:
            # Завершение викторины
            results = "\n".join([f"{animal}: {score}" for animal, score in self.animal_scores.items()])
            bot.reply_to(message, f"Спасибо за участие в викторине! Ваши результаты:\n{results}")

    def check_animal_answer(self, bot, message):
        question = quiz_questions_animals[self.current_animal_question_index]
        if message.text in question["options"]:
            # Обработка правильного ответа (например, подсчет очков)
            for animal, points in question["points"].items():
                self.animal_scores[animal] += points

        self.current_animal_question_index += 1  # Переход к следующему вопросу
        self.ask_animal_question(bot, message)