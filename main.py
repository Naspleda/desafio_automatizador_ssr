import os
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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

        # Usamos una espera explícita para asegurar que la página y los botones carguen
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "[id*='download-button-']")))

    # --- CAMBIO CLAVE 1: Contamos los botones una sola vez ---
    num_buttons = len(driver.find_elements(By.CSS_SELECTOR, "[id*='download-button-']"))
    print(f"Se encontraron {num_buttons} botones de descarga.")

    # download_buttons = driver.find_elements("css selector", "[id*='download-button-']")
    # for btn in download_buttons:
    for i in range(num_buttons):
        download_buttons = driver.find_elements(By.CSS_SELECTOR, "[id*='download-button-']")
        btn = download_buttons[i]
        print(f"Procesando botón con ID: {btn.get_attribute('id')}")
        btn.click()
        time.sleep(1)  # Espera breve para que cargue el formulario si es necesario

        # Buscar input de usuario
        try:
            username_input = wait.until(EC.visibility_of_element_located((By.ID, "username")))
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
            time.sleep(10)  # Espera para que procese el login
            print("===> Archivo descargado <===")
            print(btn.get_attribute("id"))
            print("-------------------------")
        except Exception:
            print("No se encontró formulario de login. Verificando otras interacciones...")

            # CASO ESPECIAL: Tercera iteración (i == 2)
            if i == 2:
                try:
                    print("Manejando caso especial para la tercera iteración...")
                    download_button_selector = "#root > div > div > main > div > div > div.grid.grid-cols-1.gap-4.lg\\:col-span-2 > section:nth-child(1) > div > div > div > div.mt-5.flex.justify-center.sm\\:mt-0 > button"
                    
                    # Esperar a que el botón específico sea clickeable
                    special_download_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, download_button_selector)))
                    
                    print("Botón de descarga especial encontrado. Haciendo clic...")
                    special_download_button.click()
                    
                    # Aquí puedes agregar la lógica de espera de descarga si es necesario
                    time.sleep(10) # Espera para la descarga
                    print("===> Archivo descargado (3) <===")
                    print("-------------------------")
                    # Continuar con la siguiente iteración del bucle
                    continue 
                except Exception as e:
                    print(f"No se pudo manejar el caso especial de la tercera iteración: {e}")
            
           # CASO 2a: Se necesita marcar checkboxes (Botón 3)
            try:
                # Buscar el botón de continuar/descargar ANTES de marcar los checkboxes
                continue_button = driver.find_element(
                    By.CSS_SELECTOR,
                    "#price-list-form > div > div.px-4.py-3.bg-gray-50.text-right.sm\\:px-6 > button"
                )
                is_disabled = continue_button.get_attribute("disabled")
                if is_disabled:
                    print("Botón de continuar está deshabilitado. Procediendo a marcar los checkboxes...")
                    print("Esperando por los checkboxes...")
                    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='checkbox']")))

                    print("Checkboxes encontrados. Marcándolos...")
                    checkboxes = driver.find_elements(By.CSS_SELECTOR, "input[type='checkbox']")
                    for checkbox in checkboxes:
                        if not checkbox.is_selected():
                            driver.execute_script("arguments[0].click();", checkbox)
                            print(f"Checkbox '{checkbox.get_attribute('name')}' marcado.")
                            time.sleep(0.3)

                    # Verificar si el mismo botón ahora está habilitado
                    is_disabled = continue_button.get_attribute("disabled")
                    print("Verificando si el botón de continuar sigue deshabilitado...")
                    if not is_disabled:
                         # Obtener archivos en la carpeta de descargas ANTES de hacer clic
                        files_before = set(os.listdir(downloads_path))
                        print("Botón habilitado. Haciendo clic para descargar...")
                        continue_button.click()

                        try:
                            # Espera hasta 120 segundos a que aparezca un nuevo archivo
                            wait_download = WebDriverWait(driver, 120)
                            wait_download.until(
                                lambda d: len(set(os.listdir(downloads_path)) - files_before) > 0
                            )
                            print("La descarga ha comenzado.")

                            # Opcional: Esperar a que el archivo .crdownload se complete
                            new_files = set(os.listdir(downloads_path)) - files_before
                            downloading_file = next(iter(new_files)) # Obtener el nombre del archivo que se está descargando

                            # Esperar a que el archivo deje de tener la extensión temporal de Chrome
                            while downloading_file.endswith(".crdownload"):
                                time.sleep(1)
                                # Actualizar el nombre del archivo si ha cambiado (raro, pero posible)
                                current_files = set(os.listdir(downloads_path)) - files_before
                                if not current_files:
                                    break # El archivo desapareció, salir del bucle
                                downloading_file = next(iter(current_files))


                            print("===> Archivo descargado <===")
                        except Exception as e:
                            print(f"Error o tiempo de espera agotado para la descarga: {e}")

                         # Por ejemplo, verificar que aparece un mensaje de descarga o que cambia la URL
                        # wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
                        # time.sleep(90)  # Espera para la descarga
                        print("===> Archivo descargado <===")
                    else:
                        print("El botón de continuar sigue deshabilitado después de marcar los checkboxes.")
                else:
                    print("Botón de continuar ya estaba habilitado. Haciendo clic para descargar...")
                    continue_button.click()
                    time.sleep(5)
                    print("===> Archivo descargado <===")
            # CASO 2b: Descarga directa (Botón 1)
            except Exception:
                print("No se encontraron checkboxes. Asumiendo descarga directa.")
                time.sleep(5) # Espera para la descarga directa
                print("===> Archivo descargado <===")

        # Verificar si la URL es la original, si no, volver a la página principal
        if driver.current_url != URL:
            print(f"========= Estoy en otra URL en la iteracion {i}")
            print("Volviendo a la página principal...")
            driver.get(URL)
            wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "[id*='download-button-']")))

    print("======== Proceso completado. Cerrando el navegador. ========")
    driver.quit()


if __name__ == "__main__":
    main()