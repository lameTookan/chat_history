from ChatHistory import ChatHistory, NoSystemPromptError, MalformedSaveDictError, RoleError
from functions import create_test_chat_log, tokens_from_chat_log, tokens_from_string, trim_chat_log
import unittest
import os
import MyStuff as ms
from datetime import datetime

def make_message_pretty(message: dict ):
    role = message['role']
        
    pretty_message = ""
        
    if message['role'] == 'user':
            pretty_message = "> " + message['content']
    elif message['role'] == 'system':
            pretty_message = ">>> " + ms.yellow(message['content'])
    elif message['role'] == 'assistant':
            pretty_message = ">> " + ms.cyan(message['content'])
    return pretty_message
class TestChatHistory(unittest.TestCase):
    def setUp(self) -> None:
        self.chat_history = ChatHistory()
        #self.chat_history.sys_prompt = "You are a helpful AI Assistant. You are here to help the user with their tasks."
    def test_sys_prompt_wildcards(self):
        test_sys_prompt = "Today is {date}, and your knowledge cuts off {cut_off_date}."
        formatted_sys_prompt = test_sys_prompt.format(
            date = datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
            cut_off_date = datetime.now().strftime("09/21/2021, 00:00:00")

        )
        self.chat_history.sys_prompt = test_sys_prompt
        self.assertEqual(self.chat_history.sys_prompt, formatted_sys_prompt)
    def test_user_message (self):
        self.chat_history.sys_prompt = "You are a helpful AI Assistant. You are here to help the user with their tasks."
        self.chat_history.user_message = "Hello, I am a user."
        self.assertEqual(self.chat_history.user_message, make_message_pretty({
            'role': 'user',
            "content": "Hello, I am a user."
        }))
    def test_finished_chat_log(self):
            self.chat_history.sys_prompt = "You are a helpful AI Assistant. You are here to help the user with their tasks."
            expected_chat_log = [
                {"role": "system", 
                 "content": "You are a helpful AI Assistant. You are here to help the user with their tasks."},
                {"role": "user", "content": "Hello, I am a user."},
                {"role": "assistant", "content": "Hello, I am a helpful AI Assistant."},
                {"role": "user", "content": "I need help with my tasks."},
                {"role": "assistant", "content": "I can help you with that."},
          ]
            self.chat_history.user_message = "Hello, I am a user."
            self.chat_history.assistant_message = "Hello, I am a helpful AI Assistant."
            self.chat_history.user_message = "I need help with my tasks."
            self.chat_history.assistant_message = "I can help you with that."
            self.assertEqual(self.chat_history.finished_chat_log, expected_chat_log)
    def test_trimming_chat_log(self):
        self.chat_history.sys_prompt = "You are a helpful AI Assistant. You are here to help the user with their tasks."
        test_log = create_test_chat_log(10000)
        self.chat_history.load_from_list(test_log)
        total_tokens = 0
        for message in self.chat_history.trimmed_chat_log:
             message_tokens = tokens_from_string(message['content'])
             total_tokens += message_tokens
        self.assertLessEqual(total_tokens, self.chat_history.max_chat_log_tokens)
    def test_SystemPromptError(self):
      
         self.assertRaises(NoSystemPromptError, self.chat_history.add_message, role='user', message='Hello, I am a user.')
    def test_RoleError(self):
         self.chat_history.sys_prompt = "You are a helpful AI Assistant. You are here to help the user with their tasks."
         self.assertRaises(RoleError, self.chat_history.add_message, role='monkey', message='Hello, I am a user.')
    def test_MalformedSaveDictError(self):
         self.assertRaises(MalformedSaveDictError, self.chat_history.save_dict.load_from_dict, save_dict={
              "sys_prompt": "You are a helpful AI Assistant. You are here to help the user with their tasks.",
              "user_message": "Hello, I am a user.",
              "Incorrect": "Wrong"
         })
    def test_load_from_dict(self):
         
         """
         refrence for save dict:
         save_dict = {
                "sys_prompt": sys_prompt,
                "full_chat_log": full_chat_log,
                "trimmed_chat_log": trimmed_chat_log,
                "token_info": {
                    "max_chat_log_tokens": max_chat_log_tokens,
                    "token_padding": token_padding,
                    "max_model_tokens": max_model_tokens,
                    "max_completion_tokens": max_completion_tokens

                }
         """

         pass
    def tearDown(self):
        self.chat_history = None


        
      