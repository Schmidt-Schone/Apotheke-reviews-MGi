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
  
def close_first_popups(driver):  
    popups = [  
        (By.CLASS_NAME, "cmpboxbtnyes")  # First pop-up button class
    ]  
    for popup in popups:  
        while is_element_present(driver, popup):  
            if wait_and_click(driver, popup):  
                print(f"Popup geschlossen: {popup}") 
            else:  
                print(f"Fehler beim Schließen des Popups: {popup}")  
            time.sleep(2)  # Kurze Pause nach jedem Schließen
def close_usemax_popup(driver):
    try:
        # Select the container or close button element
        close_button_selector = (By.ID, "um273817101101_closebtn")  # Change ID if needed
        # Wait until the close button is clickable
        close_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(close_button_selector)
        )
        # Scroll into view (if necessary) and click the close button
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", close_button)
        close_button.click()
        print("Closed the Usemax popup successfully.")        
    except (TimeoutException, NoSuchElementException, ElementClickInterceptedException) as e:
        print(f"Failed to close the Usemax popup: {e}")
def force_close_usemax_popup(driver):
    try:
        # Use JavaScript to hide the popup by setting its style to 'none'
        driver.execute_script("document.getElementById('um72652101101_exint').style.display = 'none';")
        print("Force closed the Usemax popup.")       
    except Exception as e:
        print(f"Failed to force close the Usemax popup: {e}")


def click_customer_reviews(driver):
    try:
        # Locate the span element with class 'a.highlight.arrow-large.sp2p'
        customer_reviews_selector = (By.CSS_SELECTOR, "a.highlight.arrow-large.sp2p")
        
        # Check if the element is present before clicking
        if is_element_present(driver, customer_reviews_selector):
            # Wait until the element is clickable
            customer_reviews_link = WebDriverWait(driver, 20).until(
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

def main():  
    driver = setup_driver()  
    try:  
        base_url = "https://www.medpex.de/sinupret-extract/9285547"  
        driver.get(base_url)
        time.sleep(20)
          
        # Schließen aller Pop-ups  
        close_first_popups(driver)
        close_usemax_popup(driver)
        time.sleep(10)
        force_close_usemax_popup(driver)

        #Main interaction
        click_customer_reviews(driver)
        time.sleep(10)

        html = driver.page_source  
        # save html to file in folder Reviews  
        with open("Reviews/Medpex.html", "w", encoding="utf-8") as f:  
            f.write(html)
  
        # Going to next page  
        next_page_selector = (By.XPATH, "//a[text()='>']")  
        time.sleep(10)
  
        click_count = 0  
        while is_element_present(driver, next_page_selector):  
            if wait_and_click(driver, next_page_selector):  
                click_count += 1  
                print(f"Element erfolgreich geklickt. Klick Nummer: {click_count}")
                html = driver.page_source  
                # save html to file in folder Reviews  
                with open("Reviews/Medpex.html", "a", encoding="utf-8") as f:  
                    f.write(html) 
                time.sleep(10)  
            else:  
                print("Klicken fehlgeschlagen, versuche es erneut")  
            time.sleep(10)  # Pause zwischen den Klicks  
  
        print(f"Button nicht mehr verfügbar. Insgesamt {click_count} mal geklickt.")  
         
    except Exception as e:  
        print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")  
    finally:  
        print("Schließe den Browser")  
        driver.quit()  
  
if __name__ == "__main__":  
    main()  