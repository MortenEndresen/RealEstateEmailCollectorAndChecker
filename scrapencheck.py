import csv
import requests
from bs4 import BeautifulSoup
import re

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

# Steg 2: Scrape email fra nettsidene
def scrape_email_from_url(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Eksempel for scraping ved bruk av class="css-bbyz0x"
        email_element = soup.find('span', class_='css-bbyz0x')
        if email_element:
            email = email_element.text
            return email
        else:
            # Fallback: Søker etter emails via regex som dekker de fleste email-formater
            email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            emails = re.findall(email_regex, soup.get_text())
            if emails:
                return emails[0]  # Returner første funn
            else:
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
url_fil = '/Users/mortenendresen/Documents/Thylo/sjekker program/vibbomails.csv'
sendt_email_fil = '/Users/mortenendresen/Documents/Thylo/sjekker program/sendte_email.csv'
output_fil = '/Users/mortenendresen/Documents/Thylo/sjekker program/nye_borettslag.csv'

# Kjør programmet
urls = importer_urls(url_fil)
sendte_emailer = les_sendte_emailer(sendt_email_fil)
lag_ny_liste(urls, sendte_emailer, output_fil)

print("Prosessen er fullført, sjekk den nye CSV-filen for resultatene.")
