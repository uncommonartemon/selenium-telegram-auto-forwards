from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import json
import os
import time
import datetime
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

# User interface
source_chat = 'https://web.telegram.org/a/#-your-id-source-chat'  # Enter the link of your chat, from where the bot will take messages for forwarding
source_name = "Source chat"  # Chat from which the bot will forward
chats_name = ["Chat 1", "Chat 2"]  # Name of chats from the list where the bot will forward
hash = '#laptop'  # Hashtag that is contained in the messages you want to forward
cooldown_message = 1  # Seconds must pass before the next message will start to be sent to chats_name
cooldown = 1  # Seconds to send one message between chats_name

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
# chrome_options.add_argument('--headless')  # Uncomment for headless mode

webdriver_path = ChromeDriverManager().install()

expect_binary_name = 'chromedriver'
if os.name == 'nt':
    expect_binary_name += '.exe'
actual_binary_name = os.path.basename(webdriver_path)
if actual_binary_name != expect_binary_name:
    webdriver_dir_path = os.path.dirname(webdriver_path)
    webdriver_path = os.path.join(webdriver_dir_path, expect_binary_name)

chrome_service = Service(executable_path=webdriver_path)
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
driver.maximize_window()
driver.get(source_chat)
actions = ActionChains(driver)

# Load localStorage data after page load
def load_local_storage():
    if os.path.isfile(json_path):
        print('Loading local_storage.json...')
        with open(json_path, 'r') as f:
            local_storage_data = json.load(f)
        for key, value in local_storage_data.items():
            driver.execute_script(f"window.localStorage.setItem('{key}', '{value}');")
        driver.refresh() 

def all_posts():
    time.sleep(cooldown)
    scroll()
    time.sleep(cooldown)
    message_list = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.CLASS_NAME, "messages-container")))
    actions.move_to_element(message_list).perform()
    time.sleep(cooldown)
    hashtags = message_list.find_elements(By.XPATH, ".//a[contains(text(), '" + hash + "' )]")
    all_posts = []
    for x in hashtags:
        post = x.find_element(By.XPATH, './ancestor::div[contains(@class, "message")][1]')
        all_posts.append(post)
    print("Messages detected: " + str(len(all_posts)))
    return all_posts

def scroll():
    container = driver.find_element(By.CLASS_NAME, 'messages-container')
    actions.move_to_element(container).perform()
    print("Chat height " + str(container.size['height']) + ', keep scrolling')
    size = container.size['height']
    while True:
        driver.execute_script("arguments[0].scrollIntoView(true);", container)
        time.sleep(cooldown)
        if container.size['height'] == size:
            break
        size = container.size['height']

def back_to_source():
    time.sleep(cooldown)
    try:
        button_source = WebDriverWait(driver, cooldown).until(EC.visibility_of_element_located((By.XPATH, '//h3[text()="' + source_name + '"]')))
    except:
        time.sleep(cooldown * 10)
        actions.send_keys(Keys.ESCAPE).perform()
        button_source = WebDriverWait(driver, cooldown).until(EC.visibility_of_element_located((By.XPATH, '//h3[text()="' + source_name + '"]')))
    
    button_source_parent = button_source.find_element(By.XPATH, './ancestor::div[contains(@class, "chat-item-clickable")]')
    time.sleep(0.5)
    time.sleep(cooldown)
    actions.click(button_source_parent).perform()  # Back to source
    time.sleep(cooldown)

def post_click(post):
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

def forwards(post):
    for name in range(len(chats_name)):
        post_click(post)  # Back to source
        time.sleep(cooldown)
        parent_picker = WebDriverWait(driver, cooldown).until(EC.presence_of_element_located((By.CLASS_NAME, 'modal-dialog')))
        time.sleep(cooldown)
        picker = WebDriverWait(parent_picker, cooldown).until(EC.presence_of_element_located((By.XPATH, './/h3[text()="' + chats_name[name] + '"]')))
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'auto', block: 'center', inline: 'center', scrollY: 0});", picker)
        actions.move_to_element(picker)
        actions.click(picker).perform()
        time.sleep(cooldown)
        button_send = driver.find_element(By.XPATH, '//button[contains(@class, "Button send main-button default secondary round click-allowed")]')
        time.sleep(cooldown)
        actions.click(button_send).perform()
        time.sleep(cooldown)

def local_storage_save():
    local_storage = driver.execute_script("return window.localStorage")
    print('Saving to local_storage.json...')
    with open(json_path, 'w') as f:
        json.dump(local_storage, f)

def push():
    posts = all_posts()
    for post in posts:
        try:
            forwards(post)
            print(datetime.datetime.now())
            print(post.text)
        except Exception as e:
            import traceback
            traceback.print_exc()
            print("Forwards ERROR: " + str(e))
            continue
        time.sleep(cooldown_message)

# Load localStorage and then proceed with the logic
load_local_storage()

while True:
    if driver.current_url == 'https://web.telegram.org/a/':
        try:
            driver.get(source_chat)
        except Exception as e:
            print(f"Auth..")
        time.sleep(cooldown * 2)

    time.sleep(cooldown)

    if driver.current_url == source_chat:
        time.sleep(cooldown)
        local_storage_save()
        push()
        driver.refresh()
        time.sleep(cooldown)
        back_to_source()