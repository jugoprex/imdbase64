from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException, TimeoutException, NoSuchElementException
import time
import re


def smart_scroll_to_load_images(driver, max_images=100, max_attempts=3, wait_time=2):
    last_img_count = 0
    attempts = 0

    while True:
        images = driver.find_elements(By.TAG_NAME, "img")
        current_img_count = len(images)

        if current_img_count >= max_images:
            print(f"Reached image limit: {current_img_count}")
            break

        if current_img_count == last_img_count:
            attempts += 1
            if attempts >= max_attempts:
                print(f"No new images after {attempts} attempts. Stopping scroll.")
                break
        else:
            attempts = 0
            last_img_count = current_img_count

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(wait_time)

    return images[:max_images]  # return only up to max_images


def scroll_down(driver, max_scrolls=10, pause_time=1):
    last_height = driver.execute_script("return document.body.scrollHeight")

    for i in range(max_scrolls):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(pause_time)  # Let new content load

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break  # No more content to load
        last_height = new_height

def get_with_retries(driver, url, retries=3, delay=10):
    attempt = 0
    while attempt < retries:
        try:
            #print(f"Navigating to {url} (attempt {attempt + 1})...")
            driver.get(url)
            return  # Success
        except TimeoutException as e:
            print(f"Timeout navigating to {url}: {e}")
            attempt += 1
            if attempt < retries:
                #print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                print("Max navigation retries reached.")
                raise

def launch_driver(driver_path="/home/jgoria/bin/geckodriver", headless=True, retries=3, delay=5):
    attempt = 0
    while attempt < retries:
        try:
            print(f"Launching driver (attempt {attempt + 1})...")
            service = Service(driver_path)
            options = Options()
            if headless:
                options.add_argument("--headless")
            driver = webdriver.Firefox(service=service, options=options)
            driver.set_page_load_timeout(10)
            return driver
        except WebDriverException as e:
            print(f"Failed to launch driver.")
            attempt += 1
            if attempt < retries:
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                print("Max retries reached. Could not launch WebDriver.")
                raise

def get_imdb_children_with_driver(actor_id, driver):
    """
    Scrapes IMDb to get the children of a given actor.
    """

    url = f"https://www.imdb.com/name/{actor_id}/"
    get_with_retries(driver, url)

    children = []

    try:
        # Wait for the expandable section to load
        parent_li = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//li[@data-testid="nm_pd_ch"]'))
        )
        button = parent_li.find_element(By.TAG_NAME, "button")

        # Scroll and click
        driver.execute_script("arguments[0].scrollIntoView();", button)
        driver.execute_script("arguments[0].click();", button)
        time.sleep(2)  # Allow content to load

        # Find the specific <li> with children names
        personal_details = driver.find_element(By.XPATH, "//section[@data-testid='PersonalDetails']")
        children_li = personal_details.find_element(By.XPATH, ".//li[@data-testid='nm_pd_ch']")
        child_elements = children_li.find_elements(By.XPATH, ".//a[contains(@href, '/name/')]")

        # Extract names and IMDb IDs
        for child in child_elements:
            name = child.text
            href = child.get_attribute("href")
            match = re.search(r"/name/(nm\d+)/", href)  # Extract IMDb ID from URL
            imdb_id = match.group(1) if match else None

            children.append({"name": name, "imdb_id": imdb_id})
    except NoSuchElementException as e:
        pass
    except Exception as e:
        print(f"Error retrieving children for {actor_id}: {e}")
    return {"parent": actor_id, "children": children}

def get_imdb_images_with_driver(actor_id, actor_name, driver):
    """
    Scrapes IMDb to get images of a given actor.

    :param actor_id: IMDb ID of the actor (e.g., 'nm0000023').
    :param driver_path: Path to the geckodriver binary.
    :param headless: Whether to run the browser in headless mode.
    :return: List of image URLs.
    """
    url = f"https://www.imdb.com/name/{actor_id}/mediaindex"
    get_with_retries(driver, url)

    try:
        #scroll_down(driver, max_scrolls=15, pause_time=3)
        smart_scroll_to_load_images(driver)
        list_of_img = driver.find_elements(By.TAG_NAME, "img")
        images = extract_images(list_of_img, actor_name)

    except Exception as e:
        print(f"Error retrieving images for {actor_id}: {e}")
    return images

def extract_images(list_of_img, name):
    images = []
    for img in list_of_img:
        try:
            src = img.get_attribute("src")
            # keep only the images with alt text that include a (year)
            if not re.search(r"\(\d{4}\)", img.get_attribute("alt")):
                continue
            #only return images with alt text that include the actors name
            if not re.search(rf"{name}", img.get_attribute("alt"), re.IGNORECASE):
                continue
            alt = img.get_attribute("alt")
            srcset = img.get_attribute("srcset")
            best_src = get_best_image_from_srcset(srcset)
            if best_src:
                images.append((best_src, alt))
            # pic = [s for s in srcset.split(",")]
            # # if it is a url,
            # links = [s for s in pic if "https://" in s]
            # if links:
            #     best_src = links[-1]
            #     #print(links)
            #     images.append((best_src, alt))
        except Exception as e:
            continue
    return images

def get_best_image_from_srcset(srcset):
    sources = [s.strip() for s in srcset.split(",") if "https://" in s]
    best_url = None
    best_density = 0.0

    for source in sources:
        parts = source.split()
        if len(parts) == 2:
            url, density = parts
            try:
                if density.endswith('x'):
                    value = float(density[:-1])
                    if value > best_density:
                        best_density = value
                        best_url = url
            except ValueError as e:
                print(e)
    return best_url


# def get_best_image_from_srcset(srcset):
#     """
#     Extracts the highest resolution image from a srcset string.
#     """
#     if not srcset:
#         return None
#     candidates = [s for s in srcset.split(",")]
#     # if it is a url,
#     links = [s for s in candidates if "https://" in s]

#     return links[0] if links else None

def extract_year_from_alt(alt_text):
    """
    Extracts the year from the alt text of an image.

    :param alt_text: Alt text of the image.
    :return: Year extracted from the alt text.
    """
    match = re.search(r"\((\d{4})\)", alt_text)
    return match.group(1) if match else None


# TODO:
# la foto que se guarda no es siempre la de mejor calidad
# si solo tiene un hijo o no tiene categoría de hijos, se rompe