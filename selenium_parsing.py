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

def selen_nomer_check(gosnomer):
    driver = webdriver.Chrome()
    driver.get('https://vin01.ru/')

    input_window = driver.find_element_by_id('num')
    input_window.send_keys(gosnomer)

    find_button = driver.find_element_by_id('searchByGosNumberButton')
    find_button.click()

    #задержка 1сек нужна для загрузки страницы и получения ответа от сервера. Если убрать - то элемент не успевает прогрузиться в браузере и захват не происходит.
    time.sleep(1)

    try:
        result = driver.find_element_by_id('vinNumbers')
        answer = 'Зарегистрированные VIN для госномера '+str(gosnomer).upper()+' :\n'+str(result.text)
    except:
        answer = 'Не удалось найти VIN в базе РСА для данного номера. Возможно, автомобиль не проходил техосмотр, так как ему менее 3-х лет, либо полис ОСАГО никогда не оформлялся.'

    driver.quit()

    return answer




