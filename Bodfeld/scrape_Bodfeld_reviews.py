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
  
def close_first_popups(driver):  
    popups = [  
        (By.CLASS_NAME, "cmpboxbtnyes")  # First pop-up button class
        
        # Add more pop-up selectors as needed  
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
        close_button_selector = (By.ID, "um273817100896_closebtn")  # Change ID if needed
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
        driver.execute_script("document.getElementById('um72652100896_exint').style.display = 'none';")
        print("Force closed the Usemax popup.")       
    except Exception as e:
        print(f"Failed to force close the Usemax popup: {e}")
  
def main():  
    driver = setup_driver()  
    try:  
        base_url = "https://www.docmorris.de/tebonin-konzent-240-mg/07752016"  
        driver.get(base_url)
        time.sleep(60)
          
        # Schließen aller Pop-ups  
        close_first_popups(driver)
        close_usemax_popup(driver)
        force_close_usemax_popup(driver)

        # Define the selector for the target paragraph
        target_element_selector = (By.CSS_SELECTOR, "h2.ReviewSection_title__UxXNQ")
        # Scroll until the target element is found
        while True:
            try:
                # Check if the target element is present and visible
                WebDriverWait(driver, 10).until(EC.presence_of_element_located(target_element_selector))
                # Once the element is found, scroll to it
                target_element = driver.find_element(*target_element_selector)
                driver.execute_script("arguments[0].scrollIntoView(true);", target_element)
                print("Target element found and scrolled to.")
                break  # Exit the loop once the element is found and scrolled to
            except Exception as e:
                # Scroll down a bit more if the element is not found yet
                driver.execute_script("window.scrollBy(0, 500);")
                print(f"Scrolling... Target element not found yet.")
  
        # Hauptinteraktion mit dem Element  
        main_element_selector = (By.CLASS_NAME, "bv-content-btn-pages-load-more-text")  
        time.sleep(30)
  
        click_count = 0  
        while is_element_present(driver, main_element_selector):  
            if wait_and_click(driver, main_element_selector):  
                click_count += 1  
                print(f"Element erfolgreich geklickt. Klick Nummer: {click_count}")
                time.sleep(30)  
            else:  
                print("Klicken fehlgeschlagen, versuche es erneut")  
            time.sleep(30)  # Pause zwischen den Klicks  
  
        print(f"Button nicht mehr verfügbar. Insgesamt {click_count} mal geklickt.")  
        
        html = driver.page_source  
        # save html to file in folder Reviews  
        with open("Reviews/DocMorris.html", "w", encoding="utf-8") as f:  
            f.write(html)  
            # print(html)  
    except Exception as e:  
        print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")  
    finally:  
        print("Schließe den Browser")  
        driver.quit()  
  
if __name__ == "__main__":  
    main()  