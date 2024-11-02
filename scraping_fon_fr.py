import csv
import requests
from bs4 import BeautifulSoup
import pandas as pd

baseurl="https://www.fongbebenin.com/traduction/francais-fongbe/"
firstUrl="https://www.fongbebenin.com/traduction/francais-fongbe/traduction-francais-fongbe-phrasescomplexes-a.html"


req = requests.get(firstUrl)

soup = BeautifulSoup(req.content, 'html.parser')

""" 
  Find all elements with class "parlettre"
  The class "parlette" is for the element that contains all the links for all the pages to scrape.
"""
palette_elements = soup.find_all('p', class_='parlettre')[0].children

"""
 Extract every other child element's href attribute for extracts links of all pages to scrape.
"""
allLinks= [child.get('href') for index,child in enumerate(palette_elements) if index%2 ]

listeSentencesFr=list()
listeSentencesFon=list()

def getCurrentPageListSentences(currentSoup):
    for ligne_element in currentSoup.find_all('div', class_='ligne'):
       # Extract text before ":"
       fr_sentente = ligne_element.text.split(':')[0].strip()
       listeSentencesFr.append(fr_sentente)
       # Extract text within "<strong>" tag
       strong_element = ligne_element.find('strong')
       if strong_element:
          fon_translation = strong_element.text
          listeSentencesFon.append(fon_translation)
          
# 
print("Get link of each page to scrape and do scraping...")
for link in allLinks:
   currentReq = requests.get(baseurl+link)
   currentSoup = BeautifulSoup(currentReq.content, 'html.parser')
   getCurrentPageListSentences(currentSoup)


output_file_path = "french_fon_translations.csv"
print("Writing the results in csv file")
with open(output_file_path, 'w',encoding='utf-8',  newline='') as output_file:
    # Create a CSV writer object
    csv_writer = csv.writer(output_file)

    # Write the header row with column names
    csv_writer.writerow(["fr", "fon"])

    # Combine and write data rows
    for i in range(len(listeSentencesFr)):
        french_translation = listeSentencesFr[i]
        fon_translation = listeSentencesFon[i]
        french_translation_encoded = french_translation.encode('utf-8')
        fon_translation_encoded = fon_translation.encode('utf-8')
        csv_writer.writerow([french_translation, fon_translation ])       
df=pd.read_csv(output_file_path)

df.head()
print(df.count())

print("That's all !")


