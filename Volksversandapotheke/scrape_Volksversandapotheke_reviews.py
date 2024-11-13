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

def accept_or_reject_cookies(driver):
    try:
        # Wait for the cookie banner to appear and check for the 'Alle ablehnen' or 'Alle akzeptieren' buttons
        cookie_accept_selector = (By.XPATH, "//a[text()='Zustimmen']")
        cookie_reject_selector = (By.XPATH, "//a[text()='ablehnen']")
        
        # Wait until either the accept or reject button is clickable
        WebDriverWait(driver, 10).until(
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
        # Locate the product rating link using the class 'product--rating-link'
        customer_reviews_selector = (By.CLASS_NAME, "product--rating-link")
        
        # Check if the element is present before clicking
        if is_element_present(driver, customer_reviews_selector):
            # Wait until the element is clickable
            customer_reviews_link = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable(customer_reviews_selector)
            )
            # Scroll into view (if necessary) and click the element
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", customer_reviews_link)
            customer_reviews_link.click()
            print("Customer review link clicked.")
        else:
            print("No reviews available")
            return
    except (TimeoutException, NoSuchElementException) as e:
        print(f"Failed to click the customer review link: {e}")
        print("No reviews available")


def main():  
    driver = setup_driver()  
    try:  
        base_url = "https://volksversand.de/arzneimittel/grippostad-c-24-kapseln-pzn-00571748-2055572"  
        driver.get(base_url)
        time.sleep(20)
          
        # Schließen aller Pop-ups  
        accept_or_reject_cookies(driver)
        time.sleep(5)

        #Main interaction
        click_customer_reviews(driver)
        time.sleep(5)

        html = driver.page_source  
        # save html to file in folder Reviews  
        with open("Reviews/Volksversandapotheke.html", "w", encoding="utf-8") as f:  
            f.write(html) 
         
    except Exception as e:  
        print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")  
    finally:  
        print("Schließe den Browser")  
        driver.quit()  
  
if __name__ == "__main__":  
    main()  