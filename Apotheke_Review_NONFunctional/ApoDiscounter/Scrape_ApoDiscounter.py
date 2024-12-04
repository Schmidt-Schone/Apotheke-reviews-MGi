from selenium import webdriver  
from selenium.webdriver.common.by import By  
from selenium.webdriver.edge.service import Service as EdgeService  
from selenium.webdriver.edge.options import Options as EdgeOptions  
from selenium.webdriver.support.ui import WebDriverWait  
from selenium.webdriver.support import expected_conditions as EC  
from webdriver_manager.microsoft import EdgeChromiumDriverManager  
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, NoSuchElementException  
import time  
import random
  
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
    try:
        popup = (By.XPATH, "//button[@data-selector='accept_button']")  # First pop-up button class 
        wait_and_click(driver, popup) 
        print("Cookies are accepted successfully.")
    except Exception as e:
        print(f"Failed to close the popup: {e}")
        time.sleep(2)  # Kurze Pause nach jedem Schließen

def close_banner(driver):
    try:
        # Wait until the close button is present
        popup_close_button = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.CLASS_NAME, "element"))
        )
        
        # Check if the close button is clickable
        try:
            WebDriverWait(driver, 2).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "element"))
            )
            # Scroll into view and click the close button if clickable
            driver.execute_script("arguments[0].scrollIntoView(true);", popup_close_button)
            popup_close_button.click()
            print("Popup closed successfully.")
        
        except (ElementClickInterceptedException, TimeoutException):
            print("Close button not clickable or hidden, trying to trigger the close event.")
            # Execute the close event directly using the `data-click="hideBox"`
            driver.execute_script("arguments[0].click();", popup_close_button)
            print("Popup closed by triggering the event directly.")
        
    except TimeoutException:
        print("Popup close button not found.")
    except Exception as e:
        print(f"Failed to close the popup: {e}")

def click_rating_stars(driver):
    try:
        rating_stars_selector = (By.XPATH, "//div[@class='d-flex mb-spacing-16']//img[@height='20']")
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable(rating_stars_selector)).click()
        print("Rating stars clicked successfully.")
    except Exception as e:
        print(f"Error clicking the rating stars: {e}")


def click_more_reviews(driver):
    click_count = 0
    
    while True:
        try:
            # Wait for the button to be clickable
            load_more_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'js-reload-product-reviews')]"))
            )
            
            # Scroll to the button to simulate human behavior
            driver.execute_script("arguments[0].scrollIntoView(true);", load_more_button)
            
            # Check if the button is disabled (button becomes disabled after last click)
            if load_more_button.get_attribute("disabled"):
                print("Button is disabled, stopping clicks.")
                break
            
            # Click the button
            load_more_button.click()
            click_count += 1
            print(f"Clicked on 'mehr Bewertungen ansehen' button {click_count} times.")
            
            # Add random delay between 2 and 5 seconds to simulate human behavior
            time.sleep(random.uniform(2, 5))
        
        except NoSuchElementException:
            print("Button not found, stopping.")
            break

def main():  
    driver = setup_driver()  
    try:  
        base_url = "https://www.apodiscounter.de/hoggar-melatonin-balance-einschlafspray-20ml-pzn-17877575"  
        driver.get(base_url)
        time.sleep(2)
          
        # Schließen aller Pop-ups  
        accept_cookies(driver)
        time.sleep(2)
        click_rating_stars(driver)
        time.sleep(2)
        #close_banner(driver)

        #Main interaction
        click_more_reviews(driver)
        time.sleep(2)
        html = driver.page_source  
        # save html to file in folder Reviews  
        with open("Reviews/ApoDiscounter.html", "w", encoding="utf-8") as f:  
            f.write(html)
    except Exception as e:  
        print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")  
    finally:  
        print("Schließe den Browser")  
        driver.quit()  
  
if __name__ == "__main__":  
    main()  