import unittest
from English_bot import cmd_words, cmd_add, words

class TestEnglishBot(unittest.TestCase):

    def test_add_and_check(self):
      class MockMessage:  # создание мок класса для Message
        def __init__(self, text):
            self.text = text

      message_mock = MockMessage(text = "/add house дом")
      cmd_add(message_mock)
      self.assertIn("house", words)
      self.assertEqual(words["house"], "дом")

      class MockMessage2:
            def __init__(self):
               pass

      message_mock_words = MockMessage2()
      result = cmd_words(message_mock_words)
      self.assertIn("house - дом", result)


if __name__ == '__main__':
    unittest.main()
