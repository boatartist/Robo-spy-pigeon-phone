#password input: id=txtPwd, password = Admin
#login button: id=btnLogin
#each text conversation on the main page's id starts with smslist-item- then a long number
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

print('installed the things')
#driver = webdriver.Chrome(ChromeDriverManager().install())
#driver = webdriver.Chrome('/usr/bin/chromedriver')
driver = webdriver.Chrome()
print('driver exists')
driver.get('http://192.168.0.1/index.html')
print('got a webpage')
try:
    login = driver.find_element(By.ID, 'txtPwd')
    login.clear()
    login.send_keys('Admin')
    login_button = driver.find_element(By.ID, 'btnLogin')
    login_button.click()
except:
    pass
while True:
    try:
        sms_link = driver.find_element(By.LINK_TEXT, 'SMS')
        sms_link.click()
        break
    except:
        pass
try:
    right_sms_mode = driver.find_element(By.LINK_TEXT, 'Device SMS')
    right_sms_mode.click()
except:
    pass
while True:
    try:
        new_sms_button = driver.find_element(By.ID, 'smslist-new-sms')
        new_sms_button.click()
        break
    except:
        pass
while True:
    try:
        contact_input = driver.find_element(By.ID, 'chosenUserSelect_chzn')
        contact_input.click()
        break
    except:
        pass
contact_select = driver.find_element(By.CLASS_NAME, 'chzn-results')
contacts = {}
try:
    for i in range(59):
        person = driver.find_element(By.ID, f'chosenUserSelect_chzn_o_{i}')
        name = person.get_attribute('value')
        contacts[name] = f'chosenUserSelect_chzn_o_{i}'
except:
    pass
for name in contacts:
    print(name)
contact = input('Contact: ')
contact_input = driver.find_element(By.ID, 'chosen-search-field-input')
contact_input.send_keys(contact + Keys.RETURN)
message = input('Message: ')
text_input = driver.find_element(By.ID, 'chat-input')
text_input.send_keys(message)
send_message = driver.find_element(By.ID, 'btn-send')
send_message.click()
time.sleep(60)
driver.close()
