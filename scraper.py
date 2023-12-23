import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time

def clean(text):
    terms_to_check = ['announcer', 'applaud', 'applause', 'audience']
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)
    filtered_sentences = [sentence for sentence in sentences if not any(term in sentence.lower() for term in terms_to_check)]
    result = ' '.join(filtered_sentences)
    pat = re.compile("[♫♪]")
    res = pat.sub('', result)
    return res

def input(link):
    if not link:  # Skip processing if the URL is empty
        print("Skipping empty URL.")
        return None

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    # Introduce a delay between requests
    time.sleep(1)
    with requests.Session() as session:
        res = session.get(link, headers=headers)
        if res.is_redirect:
            print("Redirecting to:", res.url)
        doc = BeautifulSoup(res.content, "html.parser")
        
        input_elements = doc.find_all("div", class_="elementor-element") #intro/context of the transcript
        if len(input_elements) > 19:
            title = input_elements[14].text
            intro = input_elements[16].text
            con = input_elements[19].text.split(' * * * ') 
            if len(con) == 2:
                context = con[0]
                juice = con[1]
            else:
                context = ''
                juice = con
            st = "".join(juice)
            a = clean(st)
            return {'Title': title, 'Intro': intro, 'context': context, 'Text': a}
        else:
            print(f"Insufficient elements found in the HTML for {link}")
            return None

df = pd.DataFrame(columns=['Title', 'Intro', 'context', 'Text'])
lst = []
file = 'urls.txt'

with open(file, 'r') as f:
    for i in f:
        op = input(i.strip())  # Remove leading/trailing whitespaces
        lst.append(op)

df = pd.DataFrame(lst)

df.to_csv('your_file.csv', index=True)
