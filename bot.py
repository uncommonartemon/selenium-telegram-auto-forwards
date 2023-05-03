from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from random import shuffle
import json
import tkinter as tk
import time
import datetime
import os

root = tk.Tk()
your_width = root.winfo_screenwidth()
your_height = root.winfo_screenheight()

source_chat = 'https://web.telegram.org/z/URL_SOURCE_CHAT' #add url source  
chat_name = ["Chat name", "Chat name"] #Where to send from source (take into account all indentations)
source_name = "Для бота" #name source chat (tested in a fixed state in the chat lists . from here the bot will take messages)
hash = '#пост' #forwards messages by this hashtag                                       
driver_url = 'C:\\driver\\chromedriver.exe'      
cooldown_message = 15 * 60     
cooldown = 4
cd_after_refresh = 10

chrome_options = Options()
chrome_options.add_argument('--disable-notifications')
json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'local_storage.json')
if os.path.isfile(json_path):
    print('Open local_storage.json')
    with open(json_path, 'r') as f:
        local_storage_data = json.load(f)
    chrome_options.add_argument('--user-data-dir=' + os.path.join(os.getcwd(), 'User_Data'))
    prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': os.getcwd()}
    chrome_options.add_experimental_option('prefs', prefs)
#chrome_options.add_argument('--headless') 
driver = webdriver.Chrome(driver_url, options=chrome_options)
driver.maximize_window() 
driver.get(source_chat)
actions = ActionChains(driver)
local_storage = driver.execute_script("return window.localStorage")

while True:
    while driver.current_url == 'https://web.telegram.org/z/':
        print("Авторизация")
        time.sleep(10)

    def all_posts(): #2
        time.sleep(cooldown)
        scroll()
        time.sleep(cooldown)
        message_list = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.CLASS_NAME, "messages-container")))
        actions.move_to_element(message_list).perform()
        time.sleep(cooldown)
        hashtags = message_list.find_elements(By.XPATH, ".//a[contains(text(), '"+ hash +"' )]")
        all_posts = []
        for x in hashtags:
            post = x.find_element(By.XPATH, './ancestor::div[contains(@class, "message")][1]')
            all_posts.append(post)
        print("Всего обнаружено постов :" + str(len(all_posts)))
        return all_posts

    def scroll():
        container = driver.find_element(By.CLASS_NAME, 'messages-container')
        actions.move_to_element(container).perform()
        print("Высота чата " + str(container.size['height']) + ', скролим')
        size = container.size['height']
        while True:
            driver.execute_script("arguments[0].scrollIntoView(true);", container)
            time.sleep(cooldown)
            time.sleep(cooldown)
            if container.size['height'] == size:
                break
            size = container.size['height']
        
    
    def back_to_source():
        time.sleep(cooldown)
        search = driver.find_element(By.ID, 'telegram-search-input')
        #search.send_keys(source_name)
        time.sleep(cooldown)
        button_source = driver.find_element(By.XPATH, '//h3[text()="' + source_name +'"]')
        driver.execute_script("arguments[0].scrollIntoView();", button_source)
        
        button_source_parent = button_source.find_element(By.XPATH, './ancestor::div[contains(@class, "chat-item-clickable")]')
        time.sleep(1)
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'auto', block: 'center', inline: 'center', scrollY: 0});", button_source_parent)
        time.sleep(cooldown)
        actions.click(button_source_parent).perform() #back to source
        time.sleep(cooldown)

    def post_click(post): #3
        if driver.current_url != source_chat:
            back_to_source()
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'auto', block: 'center', inline: 'center', scrollY: 0});", post)
        time.sleep(cooldown)
        actions.move_to_element(post).perform()
        actions.context_click(post).perform() 
        time.sleep(cooldown)
        forward = WebDriverWait(post, cooldown).until(EC.presence_of_all_elements_located((By.XPATH, '//i[@class="icon icon-forward"]')))[0].find_element(By.XPATH, '..')
        time.sleep(cooldown)
        actions.move_to_element(forward).perform()
        actions.click(forward).perform()


    def forwards(post): #4
        for name in range(len(chat_name)):
            post_click(post) #back to source
            time.sleep(cooldown)
            picker = WebDriverWait(driver, cooldown).until(EC.presence_of_element_located((By.XPATH, '//div[@class="ListItem-button"]//h3[text()= "'+ chat_name[name] +'"]')))
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'auto', block: 'center', inline: 'center', scrollY: 0});", picker)
            actions.move_to_element(picker)
            actions.click(picker).perform()
            time.sleep(cooldown + 1)
            button_send = driver.find_element(By.XPATH, '//button[contains(@class, "Button send default secondary round click-allowed")]')
            time.sleep(cooldown)
            actions.click(button_send).perform()
            time.sleep(cooldown)

    def local_storage_save():
        local_storage = driver.execute_script("return window.localStorage")
        print('Saving to local_storage.json...')
        with open(json_path, 'w') as f:
            json.dump(local_storage, f)

    def push(): #1
        posts = all_posts() #2
        for post in posts:
            try:
                forwards(post)
                print(datetime.datetime.now())
                print(post.text)
            except Exception as e:
                import traceback
                traceback.print_exc()
                print("Forwards ERROR : " + str(e))
                continue
            time.sleep(cooldown_message)

    if driver.current_url == source_chat:
        time.sleep(cooldown)
        local_storage_save()
        push()
        driver.refresh()
        time.sleep(cooldown)
        back_to_source()
            
    time.sleep(cooldown)
