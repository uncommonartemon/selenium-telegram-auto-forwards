# selenium-telegram-auto-forwards
Selenium: Forwarding web telegram messages from chat to chat with cooldown 
I recommend using venv and taking advantage of requirements.txt, or just install webdriver_manager and selenium.
User interface in bot.py:
```
source_chat = 'https://web.telegram.org/a/#-your-id-source-chat'  # Enter the link of your chat, from where the bot will take messages for forwarding
source_name = "Source chat"  # Chat from which the bot will forward
chats_name = ["Chat 1", "Chat 2"]  # Name of chats from the list where the bot will forward
hash = '#laptop'  # Hashtag that is contained in the messages you want to forward
cooldown_message = 1  # Seconds must pass before the next message will start to be sent to chats_name
cooldown = 1  # Seconds to send one message between chats_name
```
