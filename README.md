# selenium-telegram-auto-forwards
Selenium: Forwarding web telegram messages from chat to chat with cooldown + deletion 
#Selenium 4.8.2 
#Python 3.11.2

Цей бот буде актуальним, якщо користувачеві необхідно публікувати пости в чаті, в якому діє Затримка між відправкою повідомлень. Для реалізації цього бота необхідно встановити пітон, селеніум через термінал, так само завантажити webdriver chrome. І так само створити новий/особистий чат в телеграмі, в якому бот перевірятиме наявність смс з хештегом для пересилання. Wе простий бот я писав для друга в некомерційних цілях, будучи не досвідченим розробником на селеніум. Робот буде тестуватися, можливо він буде доповнений. HTML елементи web telegram версії z є актуальними на 03.2023. обов'язково використовуйте z версію телеграма -https://web.telegram.org/z/

вам необхідно заповнити поля:
chat_url = юрл чату, в який ви хочете робити пересилання
chat_name = ім'я цього телеграм чату
source_name = ім'я чату в якому ви пишете пост і з якого бот пересилатиме смс
hash = хештег по якому бот буде чіплятися до смс, пишіть зі знаком # , у тексті посту повинен бути такий самий хештег як і в цьому рядку
source_chat = юрл вашого чату, з якого бот буде робити пересилання
driver_url = ваш локальний шлях до chromedriver.exe
cooldown = час проміжку пересилання смс

-This bot will be relevant if the user needs to publish posts in a chat in which there is a delay between sending messages. To implement this bot, you need to install python, selenium through the terminal, as well as download webdriver chrome. And also create a new / personal chat in the telegram, in which the bot will check for the presence of SMS with a hashtag for forwarding. This is a simple bot I wrote for a friend for non-commercial purposes, being an inexperienced selenium developer. The bot will be tested, possibly it will be added. The html elements of web telegram version z are current as of 03.2023. be sure to use the z version of telegram - https://web.telegram.org/z/

you need to fill in the fields:
chat_url = chat url you want to forward to
chat_name = name of this telegram chat
source_name = the name of the chat in which you write a post and from which the bot will send SMS
hash = hashtag by which the bot will cling to SMS, write with a # sign, the text of the post must have the same hashtag as in this line
source_chat = URL of your chat from which the bot will forward
driver_url = your local path to chromedriver.exe
cooldown = SMS forwarding interval time
