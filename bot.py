from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import tkinter as tk
import time
import datetime

root = tk.Tk()
your_width = root.winfo_screenwidth()
your_height = root.winfo_screenheight()

source_chat = ''
chat_name = ''                     
source_name = ''                          
hash = '#пост'                                       
driver_url = 'C:\\chromedriver\\chromedriver.exe'      
cooldown_message = 10 * 60 #sec    
cooldown = 2
#window_height = your_height - 100
#window_width = your_width - 100  
                                  

chrome_options = Options()
chrome_options.add_argument('--disable-notifications')
driver = webdriver.Chrome(driver_url, options=chrome_options)
driver.maximize_window()
#driver.set_window_size(window_width , window_height) 
driver.get(source_chat)
actions = ActionChains(driver)

while True:
    while driver.current_url == 'https://web.telegram.org/z/':
        print("Авторизация")
        time.sleep(10)

    def all_posts():
        message_list = WebDriverWait(driver, 0).until(EC.presence_of_element_located((By.CLASS_NAME, "messages-container")))
        actions.move_to_element(message_list).perform()
        hashtags = message_list.find_elements(By.XPATH, ".//a[contains(text(), '"+ hash +"' )]")
        all_posts = []
        for x in hashtags:
            post = x.find_element(By.XPATH, './ancestor::div[contains(@class, "message")][1]')
            all_posts.append(post)
        return all_posts

    def back_to_source():
        button_source = driver.find_element(By.XPATH, '//h3[text()="' + source_name +'"]')
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'auto', block: 'center', inline: 'center', scrollY: 0});", button_source)
        button_source_parent = button_source.find_element(By.XPATH, './ancestor::div[contains(@class, "chat-item-clickable")]')
        time.sleep(cooldown)
        actions.click(button_source_parent).perform() #back to source
        time.sleep(cooldown_message)

    def post_click(post):
        back_to_source() #back to source
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'auto', block: 'center', inline: 'center', scrollY: 0});", post)
        time.sleep(cooldown)
        actions.move_to_element(post).perform()
        actions.context_click(post).perform() 
        time.sleep(cooldown)
        forward = WebDriverWait(post, cooldown).until(EC.presence_of_all_elements_located((By.XPATH, '//i[@class="icon-forward"]')))[0].find_element(By.XPATH, '..')
        forward = WebDriverWait(post, cooldown).until(EC.presence_of_all_elements_located((By.XPATH, '//i[@class="icon-forward"]')))[0].find_element(By.XPATH, '..')
        time.sleep(cooldown)
        actions.move_to_element(forward).perform()
        actions.click(forward).perform()

    def push():
        posts = all_posts() #find all posts in source chat function
        for post in posts:
            post_click(post)
            picker = WebDriverWait(driver, cooldown).until(EC.presence_of_element_located((By.XPATH, '//div[@class="ListItem-button"]//h3[text()= "'+ chat_name +'"]')))
            actions.move_to_element(picker)
            time.sleep(cooldown)
            actions.click(picker).perform()
            button_send = driver.find_element(By.XPATH, '//button[contains(@class, "Button send")]')
            time.sleep(cooldown)
            actions.click(button_send).perform()
            print(datetime.datetime.now())
            print(post.text)
            time.sleep(cooldown)
            back_to_source() #back to source
    if driver.current_url == source_chat:
        push()
            
    time.sleep(cooldown)
