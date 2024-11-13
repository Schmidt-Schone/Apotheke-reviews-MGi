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
  
def wait_and_click(driver, selector, timeout=20):  
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
  
def close_all_popups(driver):  
    popups = [
        (By.CLASS_NAME, "btn.btn-lg.btn-primary.text-center.order-md-2.order-1.w-100"),
        (By.CLASS_NAME, "flexbox"),
        (By.CSS_SELECTOR, "div[data-sn-type='close'][data-click='hideBox']"),
        # Add more pop-up selectors as needed  
    ]
    max_retries = 2  # Set the maximum number of retries for each popup
    for popup in popups:  
        retry_count = 0
        while is_element_present(driver, popup) and retry_count < max_retries:  
            if wait_and_click(driver, popup):  
                print(f"Popup geschlossen: {popup}")
                break  # Exit the while loop once the popup is closed
            else:  
                print(f"Fehler beim Schließen des Popups: {popup}")
            retry_count += 1
            time.sleep(2)  # Short pause after each attempt
        if retry_count >= max_retries:
            print(f"Popup konnte nach {max_retries} Versuchen nicht geschlossen werden: {popup}")

  
def main():  
    driver = setup_driver()  
    try:  
        base_url = "https://www.apo.com/ducray-kelual-ds-anti-schuppen-shampoo-100ml-pzn-02894355"  
        driver.get(base_url)
        time.sleep(30)

        # closing all popups
        close_all_popups(driver)

        # Hauptinteraktion mit dem Element  
        try:
            element = driver.find_element(By.CSS_SELECTOR, "div.ps-spacing-8.micro")
            element.click()
            time.sleep(20)

            element_produkt = driver.find_element(By.CSS_SELECTOR, "button.btn.btn-primary.btn-lg.mb-spacing-0.mb-md-spacing-32.my-spacing-32.w-100.d-none.d-md-block")
            element_produkt.click()
            time.sleep(20)
            
            main_element_selector = (By.CSS_SELECTOR, "a[data-action='show_more_reviews']")  
            time.sleep(20)

            click_count = 0  
            max_clicks = 10  # Set the maximum number of clicks
            while is_element_present(driver, main_element_selector) and click_count < max_clicks:  
                if wait_and_click(driver, main_element_selector):  
                    click_count += 1  
                    print(f"Element erfolgreich geklickt. Klick Nummer: {click_count}")
                    time.sleep(120) 
                else:  
                    print("Klicken fehlgeschlagen, versuche es erneut")  
                    time.sleep(120)  # Pause zwischen den Klicks
            
            if click_count >= max_clicks:
                print(f"Maximale Anzahl von {max_clicks} Klicks erreicht, Schleife beendet.")
            else:
                print(f"Button nicht mehr verfügbar nach {click_count} Klicks.")
                
            print(f"Button nicht mehr verfügbar. Insgesamt {click_count} mal geklickt.")  
            html = driver.page_source  
            # save html to file in folder Reviews  
            with open("Reviews/Apo.html", "w", encoding="utf-8") as f:  
                f.write(html)  
                # print(html)  
        except:
            print("No reviews available")
  
    except Exception as e:  
        print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")  
    finally:  
        print("Schließe den Browser")  
        driver.quit()  
  
if __name__ == "__main__":  
    main()