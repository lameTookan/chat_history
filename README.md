### To do on the readme 
- more bullet points
- be more concise, this was a brain dump I know
- Usage examples
This will get a little better, but if I didnt do this now I was never going to. Hit me up on here for now until I set up other places to contact me because I'm honestly not on a lot of platforms. 

Hey yo. I wanted to post this before I lost the nerve. I'm a newbie Python dev, and this is my first real project. It still needs a ton of work, I haven't even written test classes yet. But I wanted to get something up on here before I lost the nerve to post it.

This is a class designed to deal with chat history for use with the OpenAI API. Right now, the tokenizer is set to GPT-4, but I'm planning on making the token counter configurable during construction by passing a reference.

Basically, during construction, you specify the following token information:
- max_model_tokens: the max tokens the model you're using can take. Set to 8K by default but I'm planning on adding some way to load templates for other models like GPT-3.
- max_completion_tokens: whatever the max_tokens value you're using with the API. Set to 1K by default.
- token_padding: a number that's subtracted from the max_chat_log tokens to be extra safe.
You then need to use the .sys_prompt setter before you can do much else. Once you do that, it'll then count the tokens in the string, and will work out the max tokens allowed in the chat log by using the following formula: 
max_chat_tokens = max_model_tokens - (token_padding + max_completion_tokens + sys_prompt_tokens) - reminder_tokens if it isn't none.

Then you use either the .add_message(content, role) or the user_message and assistant_message setters to add messages to the chat log.

The message gets added to full_chat_log and trimmed_chat_log. Then the trim_chat_log() method is called that will check the tokens in the chat log and keep popping off the rightmost message until it's less than the max for the chat log.

(I realize now I should probably use a deque container for this, but I only learned that was a thing today so it's on the list.)

When you want the finished chat log, you use the .finished_chat_log getter and it will output the system prompt + the trimmed chat log and finally the reminder value if one is set, to be sent to the API.

There's also a method to retrieve messages right now there's no searching you just specify how many messages you want what role you want and if you want them to be formatted using the `_make_message_pretty()` method.

There are also two nested classes related to loading and saving the chat log to a file. One generates a save dictionary or loads from them and the other handles the files. You can use the save and load methods to accomplish this without dealing with them, I just thought it made things more organized. I separated the dictionary system from the file saving system as I realized I might want to retrieve or load dictionaries directly for other projects.

There are also three wildcards you can use in the system prompt and reminder:
- date -> today's date and time
- cut_off_date -> I don't know why I added this but it's just September 21, 2021
- shift -> this one's a little more complicated but check out the set prompt shift method for more details. Basically, you can use the method to dynamically change this value for x assistant messages or if none forever. I picture this being used to give a chat bot various modes easily like if you're making a chatbot for companionship and you want it do be harsh you can set it up so that sending the |harsh command will cause it to offer constructive criticism for x messages. I might remove this, but I think it's a fun idea

.

You can specify your own wildcard dict in the constructor using the following format:
```
{ "wildcard_name": {
  "description": "description for the prompt for use if you want to give users the option to change the system prompt",
  "value": "the value that the wildcard will be replaced with" }, 
  "next wildcard":  etc...}
```
Adding any wildcard name in brackets will cause it to be replaced when the getters are used. Also, in the saving system, they aren't replaced so for example, the date will stay current.

I think that's basically it? I've worked pretty hard on this thing. It's more of a practice project, I'm only like a month and a half into this whole Python thing, and I felt like at this point just making stuff first and studying second is the best way to continue my learning process. This is very much a work in progress, but if anyone ends up using it please let me know and I'll keep working on it.

Also, I only half know what exactly this means but pull requests are welcome and encouraged. As well as feedback, this is the first time I've made anything longer than 100 lines of code so any thoughts or opinions are not only welcome but appreciated.

Oh yeah, I need to make a requirements file but right now the only required module you need to install to use this is tiktoken, but you don't even need that if you use your own tokenizer.
