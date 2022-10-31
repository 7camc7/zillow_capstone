from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import time

# Get Zillow website:
BROWSER_HEADER = {
    "Accept-Language": "en-US",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36"
}

response = requests.get("https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3Anull%2C%22mapBounds%22%3A%7B%22west%22%3A-122.56276167822266%2C%22east%22%3A-122.30389632177734%2C%22south%22%3A37.69261345230467%2C%22north%22%3A37.857877098316834%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%7D", headers=BROWSER_HEADER)
zillow_page = response.text

# Create soup for Zillow:
soup = BeautifulSoup(zillow_page, "html.parser")

# Create list for addresses:
all_addresses = soup.select(selector="#grid-search-results address")
address_list = [address.getText() for address in all_addresses]
print(address_list)

# Create list for prices:
all_prices = soup.select(selector="article span")
price_list = [price.getText() for price in all_prices if "$" in price.getText()]
print(price_list)

# Create list for links:
all_links = soup.find_all(name="a", class_="property-card-link")
link_list = []
for link in all_links:
    if "https" not in link.get("href"):
        new_link = "https://www.zillow.com" + link.get("href")
        link_list.append(new_link)
print(link_list)

# Get google form and set chrome driver path:
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLScaOMk0pkIZ52EbVJrXXPSYD7oqtD0oTvIbJJfV0mm-qL6qEA/viewform"
chrome_driver_path = "/Users/claudiachurch/Desktop/web_dev/chromedriver"
service = ChromeService(executable_path=chrome_driver_path)
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(service=service, options=options)
driver.get(FORM_URL)
time.sleep(5)

# Use selenium to fill out google form:
for n in range(len(address_list)):
    input_address = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    ActionChains(driver).move_to_element(input_address).click(input_address).perform()
    input_address.send_keys(address_list[n])
    time.sleep(2)

    input_price = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    ActionChains(driver).move_to_element(input_price).click(input_price).perform()
    input_price.send_keys(price_list[n])
    time.sleep(2)

    input_link = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div[2]/textarea')
    ActionChains(driver).move_to_element(input_link).click(input_link).perform()
    input_link.send_keys(link_list[n])
    time.sleep(2)

    submit_button = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')
    submit_button.click()
    time.sleep(2)

    next_form = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
    next_form.click()
    time.sleep(5)

driver.quit()
