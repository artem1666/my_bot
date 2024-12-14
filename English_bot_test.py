import unittest
import asyncio
from unittest.mock import MagicMock
from English_bot import handle_level_request, grammar_rules

class TestEnglishBot(unittest.TestCase):

    async def test_handle_level_request_correct_level(self):
         # Создаем мок-объект для message
        message_mock = MagicMock()
        message_mock.text = "/a1"
        # Вызываем функцию
        await handle_level_request(message_mock)
        # Проверяем, что функция ответила с нужным текстом
        expected_answer = "Topics for the level A1: \nPast Simple - /past_simple\nPresent Simple - /present_simple"
        message_mock.answer.assert_called_with(expected_answer)


if __name__ == '__main__':
    unittest.main()
