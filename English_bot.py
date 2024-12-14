import asyncio
import random
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import json
import webbrowser


#ОТКРЫТИЕ ТГ
webbrowser.open('https://t.me/Teacher0fEnglishBot')


#СОЗДАНИЕ БОТА
bot = Bot(token='8042796539:AAFkT26J-Ei4JmD9RtegegNQMLkw_wKT3Hs')
dp = Dispatcher(bot=bot)


##CОЗДАНИЕ СПИСКА СЛОВ
words = {}
with open("words.json", "r", encoding="utf-8") as f:
    words = json.load(f)


#СОЗДАНИЕ СПИСКА ПРАВИЛ
grammar_rules = {}
with open("grammar_rules.json", "r", encoding="utf-8") as f:
    grammar_rules = json.load(f)
        

##ФУНКЦИЯ ДЛЯ СТАРТА
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Hello! I am a bot for learning English.")
    await message.answer("I'll help you with your language studies.\
To find out what I can do, write /help")


##ФУНКЦИЯ ДЛЯ ОПРЕДЕЛЕНИЯ ВОЗМОЖНОСТЕЙ БОТА
@dp.message(Command('help'))
async def cmd_help(message: types.Message):
    await message.answer("That's all I can do to help you:\nYou can\
 see the list of the most necessary basic words - /words\nYou can also add\
 the words with translation to the list - /add\nYou can take\
 a test on the knowledge of words - /test\nYou can choose\
 a topic about grammar that you would like to learn - /grammar")


##ВЫВОД СПИСКА СЛОВ
@dp.message(Command("words"))
async def cmd_words(message: types.Message):
    output_text = "List of words with translation:\n\n"
    for word, data in words.items():
        translation = data.get("translation") 
        if translation:
            output_text += f"{word}  -  {translation}\n"
    await message.answer(output_text)


##ДОБАВЛЕНИЕ СЛОВ В СПИСОК
@dp.message(Command("add"))
async def cmd_add(message: types.Message):
    try:
        parts = message.text.split(maxsplit=1)
        if len(parts) != 2:
            await message.answer("Use the command like this: /add English_word Russian_translation")
            return
        word, translation = parts[1].split(" ", 1)
        words[word.lower()] = {"translation": translation}
        await message.answer(f"Word '{word}' has been added to the list.")
        with open("words.json", "w", encoding="utf-8") as f:
            json.dump(words, f, ensure_ascii=False, indent=4)
    except ValueError:
        await message.answer("The command format is incorrect. Use it: /add English_word Russian_translation")


#ФУНКЦИЯ ТЕКСТОВ ПО ГРАММАТИКЕ
@dp.message(Command("grammar"))
async def cmd_grammar(message: types.Message):
    levels = "\n".join([f"{level.capitalize()} - /{level}" for level in grammar_rules])
    await message.answer(f"Select a level:\n{levels}")


@dp.message(lambda message: message.text.startswith('/') and len(message.text.split('_')) == 1 and message.text[1:] in grammar_rules and message.text[1:] != "test")
async def handle_level_request(message: types.Message):
    level = message.text[1:]
    if level in grammar_rules:
        subtopics = grammar_rules[level]
        formatted_subtopics = "\n".join([f"{subtopic.replace('_', ' ').title()} - /{subtopic}" for subtopic in subtopics])
        await message.answer(f"Topics for the level {level.capitalize()}: \n{formatted_subtopics}")
    else:
        await message.answer("Incorrect level.")


@dp.message(lambda message: message.text.startswith('/') and len(message.text.split('_')) > 1)
async def handle_subtopic_request(message: types.Message):
    topic = message.text[1:]
    found = False
    for level, subtopics in grammar_rules.items():
        if topic in subtopics:
            await message.answer(f"Information on the topic '{topic.replace('_', ' ').title()}':\n\n{grammar_rules[level][topic]}")
            found = True
            break
    if not found:
        await message.answer("Wrong topic.")


        
#ТЕСТ НА ЗНАНИЕ СЛОВ
@dp.message(Command("test"))
async def cmd_test(message: types.Message):
    if not words:
        await message.answer("The list is empty. Add the words with the /add command.")
        return
    test_words = random.sample(list(words.keys()), 5)
    correct_answers = 0
    current_word_index = 0
    await dp.storage.set_data(message.chat.id, {"test_words": test_words, "correct_answers": correct_answers, "current_word_index": current_word_index, "user_answers": [None] * len(test_words)})
    await ask_next_word(message) 
    
async def ask_next_word(message: types.Message):
    data = await dp.storage.get_data(message.chat.id)
    if data:
        test_words = data.get("test_words")
        current_word_index = data.get("current_word_index")
        if current_word_index < len(test_words):
            word = test_words[current_word_index]
            await message.answer(f"Translate the word '{word}'.")
        else:
            correct_answers = data.get("correct_answers")
            await message.answer(f"The test is completed. You answered correctly {correct_answers} times out of {len(test_words)} words.")
            await dp.storage.set_data(message.chat.id, {"test_words": None, "correct_answers": None, "current_word_index": None, "user_answers": None})

        
@dp.message()
async def check_answer(message: types.Message):
    data = await dp.storage.get_data(message.chat.id)
    if data:
        test_words = data.get("test_words")
        correct_answers = data.get("correct_answers")
        current_word_index = data.get("current_word_index")
        user_answers = data.get("user_answers")
        if test_words and current_word_index is not None:
            word = test_words[current_word_index]
            user_answer = message.text.lower()
            user_answers[current_word_index] = user_answer
            if user_answer == words[word]["translation"]:
                await message.answer("Right!")
                correct_answers += 1
            else:
                await message.answer(f"Wrong. Right answer is: {words[word]['translation']}")
            current_word_index += 1
            await dp.storage.set_data(message.chat.id, {"test_words": test_words, "correct_answers": correct_answers, "current_word_index": current_word_index, "user_answers": user_answers})
            await ask_next_word(message)

##ОФОРМЛЕНИЕ БОТА
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

    
