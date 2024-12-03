from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, NoSuchElementException
import time

def setup_driver():
    edge_options = EdgeOptions()
    edge_options.add_argument('--ignore-certificate-errors')
    edge_options.add_argument('--ignore-ssl-errors')
    service = EdgeService(EdgeChromiumDriverManager().install())
    return webdriver.Edge(service=service, options=edge_options)

def wait_and_click(driver, selector, timeout=10):
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable(selector)
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        time.sleep(1)  # Kurze Pause nach dem Scrollen
        element.click()
        return True
    except (TimeoutException, ElementClickInterceptedException):
        print(f"Fehler beim Klicken auf Element: {selector}")
        return False

def is_element_present(driver, selector):
    try:
        driver.find_element(*selector)
        return True
    except NoSuchElementException:
        return False

def scrape_ShopApotheke(base_url, PZN):
    driver = setup_driver()
    try:
        
        driver.get(base_url)
        
        # Warten und Schließen des Dialogs
        if wait_and_click(driver, (By.CLASS_NAME, "dialog-title__close-button")):
            print("Dialog geschlossen")
        
        # Hauptinteraktion mit dem Element
        main_element_selector = (By.CSS_SELECTOR, ".tablet\\3Aw-auto:nth-child(1)")
        
        click_count = 0
        while is_element_present(driver, main_element_selector):
            if wait_and_click(driver, main_element_selector):
                click_count += 1
                print(f"Element erfolgreich geklickt. Klick Nummer: {click_count}")
            else:
                print("Klicken fehlgeschlagen, versuche es erneut")
            time.sleep(2)  # Pause zwischen den Klicks
        
        print(f"Button nicht mehr verfügbar. Insgesamt {click_count} mal geklickt.")
        html = driver.page_source
        #save html to file in folder Reviews
        with open(f"Reviews/ShopApotheke_{PZN}.html", "w", encoding="utf-8") as f:
            f.write(html)
            #print(html)
        
    except Exception as e:
        print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")
    finally:
        print("Schließe den Browser")
        driver.quit()

