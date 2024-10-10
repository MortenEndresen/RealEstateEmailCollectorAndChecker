import csv
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# Sti til ChromeDriver (endre denne til hvor du har plassert chromedriver)
chrome_driver_path = "/Users/mortenendresen/kode/RealEstateEmailCollectorAndChecker/chromedriver-mac-x64/chromedriver"

# Konfigurer Selenium for å bruke Chrome
service = Service(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=service)

# Steg 1: Importer URLer fra CSV
def importer_urls(filbane):
    urls = []
    with open(filbane, mode='r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Hopp over overskriftsrad hvis det finnes
        for row in reader:
            if row:
                urls.append(row[0])  # Kolonne A er på indeks 0
    return urls

# Steg 2: Scrape email fra nettsidene ved hjelp av Selenium
def scrape_email_from_url(url):
    try:
        # Åpne nettsiden
        driver.get(url)

        # Vent litt for å sikre at dynamisk innhold lastes
        time.sleep(5)  # Juster tiden etter behov

        # Forsøk å finne e-postadressen basert på class
        email_element = driver.find_element(By.CLASS_NAME, "css-bbyz0x")
        if email_element:
            email = email_element.text
            print(f"Fant e-post på {url}: {email}")
            return email
        else:
            print(f"Ingen e-postadresse funnet på {url}")
            return None
    except Exception as e:
        print(f"Feil ved scraping av {url}: {e}")
        return None

# Steg 3: Les email listen som er sendt til fra CSV
def les_sendte_emailer(filbane):
    sendte_emailer = set()
    with open(filbane, mode='r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            sendte_emailer.add(row['Email'])
    return sendte_emailer

# Steg 4: Sammenlign og lag ny CSV-fil
def lag_ny_liste(urls, sendte_emailer, output_filbane):
    with open(output_filbane, mode='w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['URL', 'Email', 'Sendt?']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        for url in urls:
            email = scrape_email_from_url(url)
            if email:
                sendt = 'Ja' if email in sendte_emailer else 'Nei'
                writer.writerow({'URL': url, 'Email': email, 'Sendt?': sendt})
            else:
                writer.writerow({'URL': url, 'Email': 'Ingen funnet', 'Sendt?': 'Nei'})

# Filstier for input og output
url_fil = '/Users/mortenendresen/kode/RealEstateEmailCollectorAndChecker/newleads.csv'
sendt_email_fil = '/Users/mortenendresen/kode/RealEstateEmailCollectorAndChecker/hovedleads.csv'
output_fil = '/Users/mortenendresen/kode/RealEstateEmailCollectorAndChecker/ubrukteleads.csv'

# Kjør programmet
urls = importer_urls(url_fil)
sendte_emailer = les_sendte_emailer(sendt_email_fil)
lag_ny_liste(urls, sendte_emailer, output_fil)

# Lukk nettleseren når programmet er ferdig
driver.quit()

print("Prosessen er fullført, sjekk den nye CSV-filen for resultatene.")
