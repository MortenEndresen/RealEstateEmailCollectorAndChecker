from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

# Sti til ChromeDriver (endre denne til hvor du har plassert chromedriver)
chrome_driver_path = "/Users/mortenendresen/kode/RealEstateEmailCollectorAndChecker/chromedriver-mac-x64/chromedriver"

# Konfigurer Selenium for å bruke Chrome
service = Service(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=service)

# URL til nettsiden du vil scrape
url = "https://vibbo.no/se-stokkagarden"  # Sett inn riktig URL her

# Åpne nettsiden
driver.get(url)

# Vent litt slik at dynamisk innhold får tid til å lastes (juster hvis nødvendig)
time.sleep(5)  # 5 sekunder, kan justeres basert på nettsidens hastighet

# Forsøk å finne e-postadressen basert på class
try:
    email_element = driver.find_element(By.CLASS_NAME, "css-bbyz0x")
    if email_element:
        print(f"Fant e-post: {email_element.text}")
    else:
        print("E-postadresse ikke funnet.")
except Exception as e:
    print(f"Feil: {e}")

# Lukk nettleseren
driver.quit()
