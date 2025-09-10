from selenium import webdriver
from selenium.webdriver import Chrome
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.chrome.service import Service
import time

URL = "https://desafiodataentryait.vercel.app/"
USER = "desafiodataentry"
PASSWORD = "desafiodataentrypass"

def main():
    print("Starting Chrome WebDriver...")
    service=Service(ChromeDriverManager().install())
    option = webdriver.ChromeOptions()
    # option.add_argument("--headless=new") 
    option.add_argument("--window-size=1920,1080")
    driver = Chrome(service=service, options=option)
    driver.get(URL)
    time.sleep(5)

    download_buttons = driver.find_elements("css selector", "[id*='download-button-']")
    for btn in download_buttons:
        print(btn.get_attribute("id"))

    driver.quit()


if __name__ == "__main__":
    main()