import pyautogui
import time
import subprocess
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

URL = "https://www.google.com/"

subprocess.Popen(["google-chrome"])
time.sleep(0.5)

print("Iniciando Chrome WebDriver...")
service=Service(ChromeDriverManager().install())
option = webdriver.ChromeOptions()

option.add_argument("--window-size=1920,1080")
driver = Chrome(service=service, options=option)
driver.get(URL)
time.sleep(1)

pyautogui.typewrite("calculadora\n", interval=0.05)
time.sleep(1)

# Escribimos la operación, por ejemplo, 2+5, y presionamos Enter para ver el resultado
pyautogui.typewrite("2+5\n", interval=0.1)

print("Proceso de cálculo en Google Chrome completado.")