import tiktoken 
import unittest 
import random
import ChatHistory as ch
import MyStuff as ms
def tokens_from_string(string):
    encoding = tiktoken.encoding_for_model("gpt-4")
    
    tokenized_string = encoding.encode(string)
    return len(tokenized_string)
def are_numbers_close(a, b) -> bool:
    """ Checks if numbers are within   100  of each other"""
    if abs(a - b) <= 100:
        return True
    else:
        return False

def tokens_from_chat_log(chat_log):
    """ Returns the number of tokens in a chat log"""
    tokens = 0
    for message in chat_log:
        tokens += tokens_from_string(message["content"])
    return tokens
def create_test_chat_log(tokens = 8000):
    sample_convo = [
        {"role": "user", "content": "Hello, who are you?"},
        {"role": "assistant", "content": "I am an AI assistant"},
    ]
    one_token_word = "the"
    chat_log = []
    sample_convo_tokens = tokens_from_chat_log(sample_convo)
    if tokens % sample_convo_tokens == 0:
        number_of_messages = tokens / sample_convo_tokens
        chat_log = sample_convo * int(number_of_messages)
    else: 
        number_of_messages = tokens // sample_convo_tokens
        chat_log = sample_convo * int(number_of_messages)
        chat_log.append({"role": "user", "content": one_token_word + " " * (tokens - tokens_from_chat_log(chat_log))})
    return chat_log
def trim_chat_log(chat_log, max_tokens):
    """trims a chat log to a maximum number of tokens"""
    tokens = tokens_from_chat_log(chat_log)
    if tokens <= max_tokens:
        return chat_log
    else:
        trimmed_chat_log = []
        while tokens_from_chat_log(trimmed_chat_log) < max_tokens:
            trimmed_chat_log.append(chat_log.pop(0))

        return trimmed_chat_log


class TestChatHistory(unittest.TestCase):

    def setUp(self):
        self.chat_history = ch.ChatHistory()
        self.chat_history.sys_prompt = "You are an AI assistant."

    def test_count_tokens(self):
        text = "Hello, who are you?"
        tokens = self.chat_history._count_tokens(text)
        self.assertEqual(tokens, tokens_from_string(text))

    def test_count_tokens_in_chat_log(self):
        chat_log = create_test_chat_log(tokens=8000)
        tokens = self.chat_history._count_tokens_in_chat_log( chat_log)
        self.assertEqual(tokens, tokens_from_chat_log(chat_log))

    def test_format_message(self):
        message = "Hello, who are you?"
        role = "user"
        formatted_message = self.chat_history._format_message(message, role)
        self.assertEqual(formatted_message, {"role": role, "content": message})

    def test_get_pretty_message(self):
        message = {"role": "user", "content": "Hello, who are you?"}
        pretty_message = self.chat_history._get_pretty_message(message)
        self.assertEqual(pretty_message, "> " + message["content"])

    def test_add_message(self):
        self.chat_history.add_message("Hello, who are you?", "user")
        self.assertEqual(len(self.chat_history.full_chat_log), 1)

    def test_trim_chat_log(self):
        chat_log = create_test_chat_log(tokens=8000)
        self.chat_history.trimmed_chat_log = chat_log
        self.chat_history.max_chat_log_tokens = 7500

        self.chat_history.trim_chat_log()
        trimmed_chat_log = trim_chat_log(chat_log, self.chat_history.max_chat_log_tokens)
        self.assertEqual(self.chat_history.trimmed_chat_log, trimmed_chat_log)

    def test_get_messages(self):
        self.chat_history.add_message("Hello, who are you?", "user")
        self.chat_history.add_message("I am an AI assistant", "assistant")
        last_message = self.chat_history.get_messages(n=1, role="assistant")
        self.assertEqual(last_message, {"role": "assistant", "content": "I am an AI assistant"})

    def test_assistant_message(self):
        self.chat_history.assistant_message = "I am an AI assistant"
        last_assistant_message = self.chat_history.assistant_message
        self.assertEqual(last_assistant_message, ">> " + ms.cyan("I am an AI assistant"))

    def test_user_message(self):
        self.chat_history.user_message = "Hello, who are you?"
        last_user_message = self.chat_history.user_message
        self.assertEqual(last_user_message, "> Hello, who are you?")

    def test_len(self):
        self.chat_history.add_message("Hello, who are you?", "user")
        self.chat_history.add_message("I am an AI assistant", "assistant")
        self.assertEqual(len(self.chat_history), 2)

unittest.main()
