from time import sleep
import random
from numpy import save
from selenium import webdriver
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

def save_to_csv(data):
    try:
        df = pd.DataFrame(data)
        df.to_csv('google_places.csv', index=False)
        print('[Datos Guardados]')
    except Exception as e:
        print(f'[Error al guardar][{e}]')
        
scrolling_script = '''
    document.getElementsByClassName("m6QErb DxyBCb kA9KIf dS8AEf")[0].scroll(0, 100000)
'''

opt = Options()
opt.add_argument(
    'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36'
)

url = 'https://www.google.com/maps/place/Restaurante+Amaz%C3%B3nico/@40.423706,-3.6872655,17z/data=!4m10!1m2!3m1!2sRestaurante+Amazonico!3m6!1s0xd422899dc90366b:0xce28a1dc0f39911d!8m2!3d40.4236974!4d-3.6850925!9m1!1b1'
driver = webdriver.Chrome(options=opt)

driver.get(url)
sleep(random.uniform(4.0,5.0))
SCROLLS = 0
data = []
while SCROLLS != 3:
    driver.execute_script(scrolling_script)
    sleep(random.uniform(5,6))
    SCROLLS += 1

reviews_restaurante = driver.find_elements(By.XPATH, '//div[@data-review-id]//div[@data-review-id]/div[3]/div[2]/div[2]/div[1]')
MAXIMOS_PERFILES = 2
CONTADOR_PERFILES = 0
for review in reviews_restaurante:
    if CONTADOR_PERFILES>=MAXIMOS_PERFILES:
        driver.quit()
        break
    CONTADOR_PERFILES+=1
    link = review.find_element(By.XPATH, './a')
    try:
        link.click()
        driver.switch_to.window(driver.window_handles[1])

        # boton_opiniones = WebDriverWait(driver, 15).until(
        #     EC.presence_of_element_located((By.XPATH, '//div/div/div[1]/div[2]/div/div[1]/div/div/div[4]/div/div/button[1]'))
        # )
        # boton_opiniones.click()
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH,'//div[@class="m6QErb DxyBCb kA9KIf dS8AEf"]'))
        )
        
        USER_SCROLLS = 0
        while(USER_SCROLLS !=3):
            driver.execute_script(scrolling_script)
            sleep(random.uniform(5,6))
            USER_SCROLLS += 1
        
        #user_reviews = driver.find_elements(By.XPATH,  '//div/div/div[1]/div[2]/div/div[1]/div/div/div[4]/div[2]/div[@aria-label]')
        user_reviews = driver.find_elements(By.XPATH, '//div[@class="m6QErb"]/div[not(contains(@role,"presentation"))]')
        print(len(user_reviews))
        for rev in user_reviews:
            texto = rev.find_element(By.XPATH, './/div[4]/div[2]/span[2]').text
            if texto is None or texto == "":
                texto = 'N/A'
            rating = rev.find_element(By.XPATH, './/div[4]/div[1]//span[@aria-label]').get_attribute('aria-label')
            data.append({'rating':rating, 'texto':texto})
            print(texto, rating)
        
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        
    except Exception as e:
        save_to_csv(data)
        print(e)
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

save_to_csv(data)
       
