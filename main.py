import os
from selenium import webdriver
from selenium.webdriver import Chrome
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.chrome.service import Service
import time

URL = "https://desafiodataentryait.vercel.app/"
USER = "desafiodataentry"
PASSWORD = "desafiodataentrypass"

def main():
    downloads_path = os.path.join(os.getcwd(), "downloads")
    if not os.path.exists(downloads_path):
        os.makedirs(downloads_path)
        print(f"Carpeta creada: {downloads_path}")

    print("Iniciando Chrome WebDriver...")
    service=Service(ChromeDriverManager().install())
    option = webdriver.ChromeOptions()

    prefs = {"download.default_directory": downloads_path}
    option.add_experimental_option("prefs", prefs)

    # option.add_argument("--headless=new") 
    option.add_argument("--window-size=1920,1080")
    driver = Chrome(service=service, options=option)
    driver.get(URL)
    time.sleep(5)

    download_buttons = driver.find_elements("css selector", "[id*='download-button-']")
    for btn in download_buttons:
        print(btn.get_attribute("id"))
        btn.click()
        time.sleep(1)  # Espera breve para que cargue el formulario si es necesario

        # Buscar input de usuario
        try:
            username_input = driver.find_element("id", "username")
            username_input.clear()
            username_input.send_keys(USER)
            print("Usuario ingresado.")

            password_input = driver.find_element("id", "password")
            password_input.clear()
            password_input.send_keys(PASSWORD)
            print("Contraseña ingresada.")

            # Buscar y presionar el botón submit
            submit_btn = driver.find_element("css selector", "button[type='submit']")
            submit_btn.click()
            print("Botón submit presionado.")
            time.sleep(2)  # Espera para que procese el login
        except Exception as e:
            print("No se encontró formulario de login para este botón.")

    driver.quit()


if __name__ == "__main__":
    main()