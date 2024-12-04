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

def accept_or_reject_cookies(driver):
    try:
        # Wait for the cookie banner to appear and check for the 'Alle ablehnen' or 'Alle akzeptieren' buttons
        cookie_accept_selector = (By.ID, "btn-cookie-accept")
        cookie_reject_selector = (By.ID, "btn-cookie-decline")
        
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


def click_customer_reviews(driver):
    try:
        # Locate the span element with class 'a.highlight.arrow-large.sp2p'
        customer_reviews_selector = (By.CSS_SELECTOR, "a.count.product-review-short__link")
        
        # Check if the element is present before clicking
        if is_element_present(driver, customer_reviews_selector):
            # Wait until the element is clickable
            customer_reviews_link = WebDriverWait(driver, 2).until(
                EC.element_to_be_clickable(customer_reviews_selector)
            )
            # Scroll into view (if necessary) and click the element
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", customer_reviews_link)
            customer_reviews_link.click()
            print("Customer review icon clicked.")
        else:
            print("No reviews available")
            return
    except (TimeoutException, NoSuchElementException) as e:
        print(f"Failed to click the Customer review icon: {e}")
        print("No reviews available")  

def scrape_MyCare(base_url, PZN):  
    driver = setup_driver()  
    try:  
        
        driver.get(base_url)
        time.sleep(2)
          
        # Schließen aller Pop-ups  
        accept_or_reject_cookies(driver)
        time.sleep(2)

        #Main interaction
        click_customer_reviews(driver)
        time.sleep(2)

        html = driver.page_source  
        # save html to file in folder Reviews  
        with open(f"Reviews/Mycare_{PZN}.html", "w", encoding="utf-8") as f:  
            f.write(html)
  
        # Going to next page  
        next_page_selector = (By.CSS_SELECTOR, "a.btn.btn-icon.btn-outline.btn-next")  
        time.sleep(2)
  
        click_count = 0  
        while is_element_present(driver, next_page_selector):  
            if wait_and_click(driver, next_page_selector):  
                click_count += 1  
                print(f"Element erfolgreich geklickt. Klick Nummer: {click_count}")
                html = driver.page_source  
                # save html to file in folder Reviews  
                with open(f"Reviews/Mycare_{PZN}.html", "a", encoding="utf-8") as f:  
                    f.write(html) 
                time.sleep(2)  
            else:  
                print("Klicken fehlgeschlagen, versuche es erneut") 
                break 
            time.sleep(2)  # Pause zwischen den Klicks  
  
        print(f"Button nicht mehr verfügbar. Insgesamt {click_count} mal geklickt.")  
         
    except Exception as e:  
        print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")  
    finally:  
        print("Schließe den Browser")  
        driver.quit()  
  
