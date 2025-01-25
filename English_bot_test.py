import unittest
from unittest.mock import AsyncMock, MagicMock, patch
from English_bot import cmd_add, cmd_grammar, handle_level_request, handle_subtopic_request

class TestCmdAdd(unittest.TestCase):
    # Тест добавления слова
    @patch("builtins.open", new_callable=MagicMock)
    async def test_cmd_add_correct(self, mock_open):
        message = AsyncMock()
        message.text = "/add word translation"
        message.answer = AsyncMock()
        await cmd_add(message)
        message.answer.assert_called_with("Word 'word' has been added to the list.")
        mock_open.assert_called_with("words.json", "w", encoding="utf-8")

    # Тест случая, когда команда введена с неправильными аргументами
    async def test_cmd_add_incorrect_format(self):
        message = AsyncMock()
        message.text = "/add word"
        message.answer = AsyncMock()
        await cmd_add(message)
        message.answer.assert_called_with("Use the command like this: /add English_word Russian_translation")

class TestGrammar(unittest.TestCase):
    # Тест команды /grammar
    async def test_cmd_grammar(self):
        message = AsyncMock()
        message.answer = AsyncMock()
        await cmd_grammar(message)
        expected_levels = "\n".join([f"{level.capitalize()} - /{level}" for level in grammar_rules])
        message.answer.assert_called_with(f"Select a level:\n{expected_levels}")

    # Тест запроса уровня (/beginner)
    async def test_handle_level_request(self):
        message = AsyncMock()
        message.text = "/beginner"
        message.answer = AsyncMock()
        await handle_level_request(message)
        expected_subtopics = "\n".join([f"{subtopic.replace('_', ' ').title()} - /{subtopic}" for subtopic in grammar_rules["beginner"]])
        message.answer.assert_called_with(f"Topics for the level Beginner: \n{expected_subtopics}")

    # Тест запроса подтемы (/present_simple)
    async def test_handle_subtopic_request(self):
        message = AsyncMock()
        message.text = "/present_simple"
        message.answer = AsyncMock()
        await handle_subtopic_request(message)
        message.answer.assert_called_with(f"Information on the topic 'Present Simple':\n\n{grammar_rules['beginner']['present_simple']}")
        
if __name__ == '__main__':
    unittest.main()
