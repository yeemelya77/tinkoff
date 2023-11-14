import json
import requests
from bs4 import BeautifulSoup
from json.decoder import JSONDecodeError
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

def get_csrf_token(driver):
    try:
        # Look for the CSRF token in the entire HTML source
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        csrf_token_tag = soup.find_all(name='meta', attrs={'name': 'csrf-token', 'content': True})

        if csrf_token_tag:
            return csrf_token_tag[0].attrs['content']

    except KeyError:
        print("CSRF token not found. Exiting.")
        return None

def get_answer_from_bard(intent, api_key):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    response = requests.post(
        "https://api.bard.ai/v1/query",
        headers=headers,
        data=json.dumps({"query": intent}),
    )

    return response.json()

def main():
    api_key = "cwiWSJHYpLcf3mikEJ8GygLFZwonlfOOu1BVbNmymmYCKTONVAHGe18jylpCykRtuVK5WQ"

    driver = webdriver.Chrome()
    driver.get("https://twork.tinkoff.ru/auth/Account/Login?ReturnUrl=%2Fauth%2Fconnect%2Fauthorize%2Fcallback%3Fapproval_prompt%3Dforce%26client_id%3DTWorkOAuth2Proxy%26code_challenge%3DWRaUpTDHENW36_h0Q_s3F-bjTD1QGj8Syinn60cK608%26code_challenge_method%3DS256%26redirect_uri%3Dhttps%253A%252F%252Ftwork.tinkoff.ru%252Foauth2%252Fcallback%26response_type%3Dcode%26scope%3Dopenid%2520profile%2520offline_access%2520gateway%253Atwork-api%26state%3Du4uaVDMkBoO1dKMCrzDE3QonCpkD4H_Lhz6Kfm7vX6U%253Ahttps%253A%252F%252Ftwork.tinkoff.ru%252Fworkspace%252Fklecks%252F%253Fwsreauth%253D1699755188718")

    wait = WebDriverWait(driver, 10)

    # Ждем, пока появится поле ввода логина
    username_selector = "input#Login"
    username_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, username_selector)))

    # Ввод логина
    username_element.send_keys("daemelin65830")

    # Используем ActionChains для последовательности действий
    actions = ActionChains(driver)
    actions.send_keys(Keys.TAB)  # Переключение фокуса на поле ввода пароля
    actions.send_keys("Z67dEVAi")  # Ввод пароля
    actions.send_keys(Keys.RETURN)  # Нажатие Enter после ввода пароля
    actions.perform()  # Выполнение последовательности действий

    # Получаем CSRF токен
    csrf_token = get_csrf_token(driver)

    if csrf_token:
        # Continue with the rest of the code

        # Ждем, пока загрузится страница с элементом с ID `intent`
        intent_element = wait.until(EC.presence_of_element_located((By.ID, "intent")))

        intent = intent_element.text
        try:
            answer = get_answer_from_bard(intent, api_key)

            # Добавьте соответствующие селекторы для description_element и examples_element
            description_element = driver.find_element_by_id("description")
            examples_element = driver.find_element_by_id("examples")

            if answer["intent"] in description_element.text and answer["intent"] in examples_element.text:
                for answer_option in driver.find_elements_by_class_name("answer-option"):
                    if answer_option.text == answer["intent"]:
                        answer_option.click()
                        break
                else:
                    driver.find_element_by_id("answer-error").click()
            else:
                driver.find_element_by_id("answer-error").click()

            # Ждем, пока появится поле для ввода кода
            code_input_selector = "input#secondFactorCode"
            code_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, code_input_selector)))

            # Вводим 4 цифры в поле ввода кода
            code_input.send_keys("1234")  # Замените "1234" на ваш фактический код

            # Нажимаем Enter после ввода кода
            code_input.send_keys(Keys.RETURN)

            # Ждем, пока появится кнопка "Приступить"
            start_button_selector = "span.t-content"
            start_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, start_button_selector)))

            # Нажимаем кнопку "Приступить"
            start_button.click()

        except JSONDecodeError:
            print("Error decoding JSON response from Bard API")

    else:
        print("CSRF token not retrieved. Exiting.")

    driver.quit()

if __name__ == "__main__":
    main()
