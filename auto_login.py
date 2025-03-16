# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "00BABD54995A4E0DC8A3A10127E4915A9EE9DD33127B7920FEECC6156D4FADC0037478D7F542F923C037CB002D61BC9A68D327159C092CFFFAB64D59A8677273006A9CFF45FA651A65E30CEBAAAA319BBCCA39AF5700B0788106158172F67E50687D955AF4931E265E0CAA2B39176BA561932B511980EB3590128717258DC21D7669191FF34BD0609D9F3101D15D95ACC408503347ACF4170D6588FE4536F04CCCFCE38744EDCAA54D64D7D58A18A5259145F8BB6DF28384E93B866A01932A5AEC794D0B2BE5A2C98B79DABAE041A52A4813666786D15A286E10E371923C8B13D0A5B6836A03D02AB49BDE5F40233C6ED5AE50E05AF0C65686A29CE55CD63D239F7BA72FF3C800739320A3CA7FFA3DE349F52A18BFF4A8AEF7689F8CDA232835DCD767254B2D44E57D27D3F8EECB92416034E2BAB82AD8FCD997AEEE518E34226D570C7368FFEC229FEA8E7B5C996792A7417C678201303D10FCFB635D4BA6D004"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
