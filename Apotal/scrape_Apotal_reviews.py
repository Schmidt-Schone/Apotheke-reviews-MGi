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

def accept_cookies(driver):
    """Try to accept cookies by clicking the appropriate button."""
    cookie_buttons = [
        (By.CSS_SELECTOR, "button.mb3.accept-all-cookies"),  # "Alles akzeptieren" button
        (By.CSS_SELECTOR, "button.mb[onclick='checkSettings(undefined)']")  # "Auswahl bestätigen" button
    ]
    for button in cookie_buttons:
        if is_element_present(driver, button):
            if wait_and_click(driver, button):
                print(f"Cookies accepted using button: {button}")
                return True
            else:
                print(f"Error clicking cookie button: {button}")
    print("No cookie acceptance button found or clickable.")
    return False


def click_customer_reviews(driver):
    try:
        # Locate the span element with class 'a#productReviewTab'
        customer_reviews_selector = (By.CSS_SELECTOR, "a#productReviewTab")
        
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

def click_load_more_reviews(driver):
    load_more_locator = (By.CSS_SELECTOR, '#btn-load.buttonLinks.btnSave')
    click_count = 0

    while True:
        try:
            load_more_button = WebDriverWait(driver, 2).until(EC.presence_of_element_located(load_more_locator))
            if not load_more_button.is_displayed() or not load_more_button.is_enabled():
                print("No more 'Load More Reviews' button available.")
                break
            load_more_button.click()
            click_count += 1
            time.sleep(2)
            print(f"Clicked 'Load More Reviews' button {click_count} times.")
        except (TimeoutException, NoSuchElementException):
            print("'Load More Reviews' button not found. Stopping the process.")
            break
        except ElementClickInterceptedException:
            print("Could not click the 'Load More Reviews' button due to an interception. Trying again.")
            continue
        except Exception as e:
            print(f"Error clicking 'Load More Reviews' button: {e}")
            break

def scrape_Apotal(base_url, PZN):  
    driver = setup_driver()  
    try:  
        
        driver.get(base_url)
        time.sleep(2)
          
        # Schließen aller Pop-ups 
        accept_cookies(driver)
        time.sleep(2) 

        #Main interaction
        click_customer_reviews(driver)
        time.sleep(2)

        
  
        # Going to next page  
        click_load_more_reviews(driver) 
        time.sleep(2)
  
        
        html = driver.page_source  
        # save html to file in folder Reviews  
        with open(f"Reviews/Apotal_{PZN}.html", "w", encoding="utf-8") as f:  
            f.write(html) 
        time.sleep(2)  

    except Exception as e:  
        print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")  
    finally:  
        print("Schließe den Browser")  
        driver.quit()  
  
