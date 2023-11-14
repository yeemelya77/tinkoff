import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pyautogui

# Установите путь к вашему ChromeDriver
chrome_driver_path = 'C:\\Users\\Denis\\Desktop\\11\\chromedriver.exe'

# Получите путь к вашему основному профилю пользователя Chrome
current_profile_path = r'C:\\Users\\Denis\\AppData\\Local\\Google\\Chrome\\User Data\\Default'

# Создайте объект ChromeOptions
chrome_options = Options()

# Установите путь к основному профилю пользователя Chrome в ChromeOptions
chrome_options.profile = current_profile_path

# Запустите веб-драйвер в основном профиле пользователя Chrome
driver = webdriver.Chrome(service=ChromeService(chrome_driver_path), options=chrome_options)

# Эмуляция нажатия Ctrl+T для открытия новой вкладки
pyautogui.hotkey('ctrl', 't')
time.sleep(2)  # Ждем, чтобы вкладка успела открыться

# Откройте страницу по ссылке
driver.get('https://twork.tinkoff.ru/workspace/klecks/task')

# Получение содержимого страницы
html_content = driver.page_source

# Использование BeautifulSoup для парсинга HTML
soup = BeautifulSoup(html_content, 'html.parser')

# Таймер
start_time = time.time()

# Ждем 30 секунд
while time.time() - start_time < 80:
    time.sleep(1)

# Извлечение намерения
if soup.find("div", class_="flex-text__content", string=" Намерение: "):
    intention = soup.find("div", class_="flex-text__content", string=" Намерение: ").find_next_sibling("div").get_text(strip=True)
else:
    intention = None

# Извлечение описания
if soup.find("div", class_="flex-text__content", string=" Описание: "):
    description = soup.find("div", class_="flex-text__content", string=" Описание: ").find_next_sibling("div").get_text(strip=True)
else:
    description = None

# Извлечение текста из блоков
user_message = soup.find("div", class_="flex-text__content", string=" Текст сообщения: ").find_next_sibling("div").get_text(strip=True)
examples = soup.find("div", class_="flex-text__content", string=" Подходящие примеры: ").find_next_sibling("div").get_text(strip=True)

# Анализ элементов
correct_answer = None
for element in [intention, description, user_message, examples]:
    if element is not None and element.lower() in ["да", "подходит", "подобно"]:
        correct_answer = "Да, подходит"
    if element is not None and element.lower() in ["нет", "не подходит", "не похоже"]:
        correct_answer = "Нет, не подходит"

# Вывод результатов
print("Намерение:", intention)
print("Описание:", description)
print("Текст сообщения пользователя:", user_message)
print("Подходящие примеры:", examples)
print("Варианты ответов:", response_options)
print("Правильный ответ:", correct_answer)

# Закрытие веб-драйвера
driver.quit()
