import pandas as pd
import requests
from bs4 import BeautifulSoup

url = "https://de.wikipedia.org/wiki/Benutzer:FordPrefect42/Liste_der_Telemann-Kantaten"

response = requests.get(url)
response.raise_for_status()

soup = BeautifulSoup(response.content, 'html.parser')

table = soup.find('table', {'class': 'wikitable sortable'})

kantaten_table = pd.read_html(str(table))[0]

kantaten_table['Interwiki Links'] = ""
kantaten_table['Outgoing Links'] = ""

for index, row in enumerate(table.find_all('tr')[1:]):  # Skip header row
    interwiki_links = []
    outgoing_links = []
    
    for cell in row.find_all('td'):
        for link in cell.find_all('a', href=True):
            href = link['href']
            if href.startswith('/wiki/'):
                interwiki_links.append("https://de.wikipedia.org" + href)
            elif href.startswith('http'):
                outgoing_links.append(href)
    
    kantaten_table.at[index, 'Interwiki Links'] = interwiki_links
    kantaten_table.at[index, 'Outgoing Links'] = outgoing_links

output_file = "telemann_kantaten_with_links.jsonl"
kantaten_table.to_json(output_file, orient="records", lines=True, force_ascii=False)

print(f"Data has been saved to {output_file}")
