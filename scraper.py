from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time


# Set up the Firefox WebDriver
service = Service("/home/jgoria/bin/geckodriver")  # Replace with your actual path
options = Options()
options.add_argument("--headless")
#options.headless = True  # Set to True if you don't want to open the browser window

driver = webdriver.Firefox(service=service, options=options)

# Open the IMDb page
actor_id = "nm0000023"
url = f"https://www.imdb.com/name/{actor_id}/"
driver.get(url)
driver.set_page_load_timeout(15)


try:
    # Wait until the parent <li> that contains the button appears
    parent_li = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//li[@data-testid="nm_pd_ch"]'))
    )
    
    # Find the button inside that <li>
    button = parent_li.find_element(By.TAG_NAME, "button")

    # Scroll into view
    driver.execute_script("arguments[0].scrollIntoView();", button)

except Exception as e:
    print("Button not found", e)

# Extract the children names
children = []
try:
    personal_details = driver.find_element(By.XPATH, "//section[@data-testid='PersonalDetails']")
    driver.execute_script("arguments[0].click();", button)
    time.sleep(2)  # Wait for content to load

    # Find the specific <li> that contains children names
    children_li = personal_details.find_element(By.XPATH, ".//li[@data-testid='nm_pd_ch']")
    
    # Extract only the <a> links inside this specific <li>
    child_elements = children_li.find_elements(By.XPATH, ".//a[contains(@href, '/name/')]")

    # Save names and URLs
    children = [{"name": child.text, "url": child.get_attribute("href")} for child in child_elements]

except Exception as e:
    print("Children section not found:", e)

# Print results
print({"parent": actor_id, "children": children})

# Close the browser
driver.quit()