from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import time

# binary = FirefoxBinary('/usr/bin/firefox')
# browser = webdriver.Firefox(firefox_binary=binary)
# 无界面版chrome使用方法
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument("user-agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'")
browser = webdriver.Chrome(chrome_options=chrome_options,executable_path='/usr/local/bin/chromedriver')
# 无界面版chrome使用方法

# browser = webdriver.Chrome()
# Firefox()
try:
    browser.get('https://www.guoguo-app.com/')
    input = browser.find_element_by_id('J_SearchInput')  # J_SearchBtn
    time.sleep(1)
    try:
        close = browser.find_element_by_xpath("html/body/div/div/a").click()
    except:
        pass
    wait = WebDriverWait(browser, 10)

    input.send_keys('3868932225395') # 顺丰的不支持 821438763102

    input.send_keys(Keys.ENTER)
    wait.until(EC.presence_of_element_located((By.ID, 'J_SearchBtn')))
    btn = browser.find_element_by_id('J_SearchBtn')
    btn.click()
    time.sleep(1)
    try:
        lis = browser.find_elements_by_tag_name('span')
        if len(lis)>10:
            lis = lis[6:-4]
            for i in lis:
                print(i.text)
    except:
        print('没有加载到信息,不去做处理')
        pass
finally:
    # browser.close()
    pass