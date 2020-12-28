from selenium import webdriver
import time
import random

def delay():
    time.sleep(random.randint(1,3))

def selen_vin_check(VIN):
    driver = webdriver.Chrome()
    link_url = 'https://xn--90adear.xn--p1ai/check/auto#'+str(VIN)
    driver.get(link_url)
    delay()

    button = driver.find_element_by_class_name('checker')
    button.click()
    delay()
    time.sleep(50)

    # ловля капчи, нажатие на кнопку получить
    # capture = driver.find_element_by_id('captchaSubmit')
    # capture.click()

    result = driver.find_element_by_class_name('checkAutoSection')
    answer = result.text
    if 'По указанному VIN не найдена информация о регистрации транспортного средства' in answer:
        answer = 'По указанному VIN не найдена информация о регистрации транспортного средства.\nПроверьте правильность вводимого VIN-кода!'
    driver.quit()
    return answer





