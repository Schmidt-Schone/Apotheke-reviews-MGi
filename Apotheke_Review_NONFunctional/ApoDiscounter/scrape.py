def click_more_reviews(driver):
    click_count = 0
    while True:
        try:
            # Find the button by CSS Selector or XPath
            load_more_button = driver.find_element(By.XPATH, "//button[contains(@class, 'js-reload-product-reviews')]")
            
            # Use JavaScript to click the button
            driver.execute_script("arguments[0].click();", load_more_button)
            
            click_count += 1
            print(f"Clicked on 'mehr Bewertungen ansehen' button {click_count} times.")
            time.sleep(2)  # Pause between clicks to load new reviews
            
        except NoSuchElementException:
            print("Button not found.")
            break
        except ElementClickInterceptedException:
            print("Button cannot be clicked at the moment.")
            break
