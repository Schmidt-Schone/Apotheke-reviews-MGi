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
  
def wait_and_click(driver, selector, timeout=2):  
    try:  
        element = WebDriverWait(driver, timeout).until(  
            EC.element_to_be_clickable(selector)  
        )  
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)  
        time.sleep(2)  # Kurze Pause nach dem Scrollen  
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
    
def click_kundenbewertungen(driver):
    try:
        # CSS selector for the "Kundenbewertungen" tab using its ID
        kundenbewertungen_selector = (By.ID, "productReviewTab")        
        # Wait until the "Kundenbewertungen" tab is clickable
        kundenbewertungen_tab = WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable(kundenbewertungen_selector)
        )       
        # Scroll into view and click the "Kundenbewertungen" tab
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", kundenbewertungen_tab)
        kundenbewertungen_tab.click()
        print("Clicked on 'Kundenbewertungen' successfully.")       
    except (TimeoutException, NoSuchElementException) as e:
        print(f"Failed to click on 'Kundenbewertungen': {e}")

def click_load_more_reviews(driver):
    try:
        # Selector for the "Load More Reviews" button
        load_more_button_selector = (By.ID, "btn-load")        
        click_count = 0  # To track how many times the button is clicked       
        while True:
            try:
                # Wait until the button is visible and clickable
                load_more_button = WebDriverWait(driver, 2).until(
                    EC.element_to_be_clickable(load_more_button_selector)
                )               
                # Scroll into view and click the button
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", load_more_button)
                load_more_button.click()
                click_count += 1
                time.sleep(2)
                print(f"Clicked 'Load More Reviews' button {click_count} times.")                
                # Adding a short wait to avoid too many requests in quick succession
                WebDriverWait(driver, 2)
            except (TimeoutException, NoSuchElementException):
                # Exit the loop when the button is no longer present
                print("No more 'Load More Reviews' button available.")
                break
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def accept_or_reject_cookies(driver):
    try:
        # Wait for the cookie banner to appear and check for the 'Alle ablehnen' or 'Alle akzeptieren' buttons
        cookie_accept_selector = (By.XPATH, "//a[text()='Zustimmen']")
        cookie_reject_selector = (By.XPATH, "//a[text()='Ablehnen']")
        
        # Wait until either the accept or reject button is clickable
        WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable(cookie_accept_selector)
        )

        # Click the "Alle ablehnen" button to reject cookies (or you can click "Alle akzeptieren" based on your preference)
        try:
            driver.find_element(*cookie_reject_selector).click()
            print("Cookie settings rejected.")
        except NoSuchElementException:
            driver.find_element(*cookie_accept_selector).click()
            print("Cookies accepted.")
            
        time.sleep(2)  # Allow time for the banner to disappear

    except (TimeoutException, NoSuchElementException) as e:
        print(f"Cookie banner not found or click failed: {e}")

def main():  
    driver = setup_driver()  
    try:  
        base_url = "https://www.medikamente-per-klick.de/dysto-loges-tabletten-50st-12346465"  
        driver.get(base_url)
        time.sleep(2)
        
        accept_or_reject_cookies(driver)
        time.sleep(2)

        # Main Interaction
        click_kundenbewertungen(driver)
        time.sleep(2)
        click_load_more_reviews(driver)  
        
        html = driver.page_source  
        # save html to file in folder Reviews  
        with open("Reviews/MedikamentePerKlick.html", "w", encoding="utf-8") as f:  
            f.write(html)  
            # print(html)  
    except Exception as e:  
        print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")  
    finally:  
        print("Schließe den Browser")  
        driver.quit()  
  
if __name__ == "__main__":  
    main()  