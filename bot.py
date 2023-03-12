from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import time
import datetime
import os

#Selenium 4.8.2
#Все url телеграма должны быть через версию z - https://web.telegram.org/z/

chat_url = ''                                 #url ссылка чата куда  пересылать
chat_name = ""                               #Имя чата куда пересылать
source_name = ""                              #Имя чата источника
hash = '#пост'                                        #Напиши хэштег 
source_chat = ''                              #Создай чат куда ты будешь писать посты,и в котором бот будет парсить посты ,и первый попавшийся пост с хэштегом hash бот перешлет 
driver_url = ''                              #Локальный путь в комьютере где храниться chromedriver.exe, если у тебя его нет - скачай его с chromium
cooldown = 15                                          #Время переодичности пересылки смс в минутах 

chrome_options = Options()
chrome_options.add_argument('--disable-notifications')
driver = webdriver.Chrome(driver_url, options=chrome_options)
driver.set_window_size(1024, 1024) 
driver.get(source_chat)
actions = ActionChains(driver)

if not os.path.exists("selenium_images"):
    os.makedirs("selenium_images")

while True: 
    post = ''
    post_text = ''
    while driver.current_url == 'https://web.telegram.org/z/':
        print("Авторизация")
        time.sleep(10)
    if driver.current_url == source_chat:
        middle = driver.find_element(By.ID, 'MiddleColumn')
        actions.move_to_element(middle).perform()
        message_list = WebDriverWait(driver, 0).until(EC.presence_of_element_located((By.CLASS_NAME, "messages-container")))
        actions.move_to_element(message_list).perform()
        hashtags = message_list.find_elements(By.XPATH, ".//a[contains(text(), '"+ hash +"' )]")
        if len(hashtags) > 0:
            hashtag = hashtags[0]
            post = hashtag.find_element(By.XPATH, '..//..//..//..//..//..//div[contains(@class, "Message")]')
            post_text = post.text
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'auto', block: 'center', inline: 'center', scrollY: -100});", post)
            actions.move_to_element(post).perform()
            actions.context_click(post).perform() 
            time.sleep(2)
            menuitems = WebDriverWait(post, 0).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@class="MenuItem compact"]//*[contains(@class, "icon-forward")]')))
            if len(menuitems) > 0:
                forward = menuitems[0]
                actions.move_to_element(forward).perform()
                actions.click(forward).perform()
                picker = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, '//div[@class="ListItem-button"]//h3[text()= "'+ chat_name +'"]')))
                actions.move_to_element(picker)
                actions.click(picker).pause(1).perform()
        if driver.current_url == chat_url:
            if driver.find_element(By.XPATH, '//div[contains(@class, "ComposerEmbeddedMessage")]'):
                print(datetime.datetime.now())
                print(post_text)
                button_send = driver.find_element(By.XPATH, '//button[contains(@class, "Button send")]')
                actions.click(button_send).perform()
                button_source = driver.find_element(By.XPATH, '//h3[text()="' + source_name +'"]')
                button_source_parent = button_source.find_element(By.XPATH, './ancestor::div[contains(@class, "chat-item-clickable")]')
                actions.click(button_source_parent).perform()
                driver.execute_script("arguments[0].scrollIntoView();", post)
                time.sleep(1)
                actions.move_to_element(post).perform()
                actions.context_click(post).perform()
                time.sleep(2)
                delete = WebDriverWait(post, 2).until(EC.presence_of_all_elements_located((By.XPATH, '//i[@class="icon-delete"]')))
                delete_button = delete[0].find_element(By.XPATH, '..')
                actions.move_to_element(delete_button).perform()
                actions.click(delete_button).perform()
                modal = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'Modal delete')]//button[@class='Button confirm-dialog-button default danger text']")))
                actions.click(modal).perform()
    time.sleep(cooldown * 60)
