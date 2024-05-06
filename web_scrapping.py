# código que recupera o html do site e salva em uma string
import requests
import time
import json
import re
import threading
import nltk
from datetime import datetime
from bs4 import BeautifulSoup
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords


animes = 'https://animesonlinecc.to/'
youtube = 'https://www.youtube.com'
google = 'https://google.com'
wikipedia_generico = 'https://www.wikipedia.org/'
microbiologia = 'https://pt.wikipedia.org/wiki/Microbiologia'
microbiology = 'https://en.wikipedia.org/wiki/Microbiology'
url = animes

STOP = False
RUNNING_TIME = 60 * 30



def stop_scrapping_timer():
    global STOP
    timer = RUNNING_TIME
    print("Começou em:", datetime.now().strftime('%H:%M:%S'))
    time.sleep(timer)
    STOP = True

def printTime():
    _5_minutes_passed = 0
    while not STOP:
        #print(datetime.now().strftime('%H:%M:%S'))
        print(5 * _5_minutes_passed,"minutes passed")
        time.sleep(60*5)
        _5_minutes_passed += 1

def filter_links(links):
    links = [link.get('href') for link in links]
    
    #filtra os none types
    links = [link.split('#')[0].split('?')[0] for link in links if link and link.startswith('http')]
    return list(set(links))


def filter_h1(h1_tags):
    h1_tags = [tag.get_text() for tag in h1_tags]
    new_h1_tags = []
    for i in range(len(h1_tags)):
        
        h1 = re.sub(r"(?:\s\s+|\n+|\r+)", " ", h1_tags[i]) #re.sub(r"^\s+|\s+$", "", h1_tags[i])
        if (len(h1) > 0 and h1 != '\r' and h1 != ' '):
            h1 = h1.lower()
            replace = {'á': 'a', 'à': 'a', 'é': 'e', 'è': 'e', 'í': 'i', 'ì': 'i', 'ó': 'o', 'ò': 'o', 'ú': 'u', 'ù': 'u', 'ü': 'u', 'â': 'a', 'ê': 'e', 'î': 'i', 'ô': 'o', 'û': 'u', 'ã': 'a', 'õ': 'o', 'ç': 'c'}
            for key in replace:
                h1 = h1.replace(key, replace[key])
            new_h1_tags.append(h1)
    return list(set(new_h1_tags))

def get_words_from_h1(h1_tags):
    stop_words = set(nltk.corpus.stopwords.words('english') + nltk.corpus.stopwords.words('portuguese'))
    pt_stemmer = SnowballStemmer('portuguese')
    en_stemmer = SnowballStemmer('english')
    words = []
    keywords = []
    #detecta as palavras chaves de cada h1 e adiciona à lista de keywords

    for h1 in h1_tags:
        h1_split = h1.split()
        stemmed_words = []
        for word in h1_split:
            stemmed_words.append(pt_stemmer.stem(word))
            stemmed_words.append(en_stemmer.stem(word))
        words.extend(stemmed_words)
    #remove strings que não são palavras
    for i in range(len(words)):
        words[i] = re.sub(r'\W+', '', words[i])


    words = [word for word in words if word not in stop_words and len(word) > 1]
    words = [re.sub(r'\W+', '', word) for word in words]
    return list(set(words))

def filter_title(title):
    if title:
        title = title.get_text()
        title = title.lower()
        title = re.sub(r"(?:\s\s+|\n+|\r+)", " ", title)
        replace = {'á': 'a', 'à': 'a', 'é': 'e', 'è': 'e', 'í': 'i', 'ì': 'i', 'ó': 'o', 'ò': 'o', 'ú': 'u', 'ù': 'u', 'ü': 'u', 'â': 'a', 'ê': 'e', 'î': 'i', 'ô': 'o', 'û': 'u', 'ã': 'a', 'õ': 'o', 'ç': 'c'}
        for key in replace:
            title = title.replace(key, replace[key])
        accepted = 'abcdefghijklmnopqrstuvwxyz0123456789 '
        title = ''.join([char for char in title if char in accepted])
        if len(title) > 0:
            return title
    return "title not found"

def get_html(url):
    response = requests.get(url)
    if response.status_code != 200:
        return {'url': url, 'h1': [], 'words': [], 'links': []}
    soup = BeautifulSoup(response.text, 'html.parser')
    h1_tags = soup.find_all(['h1', 'h2'])
    h1_tags = filter_h1(h1_tags)
    external_links = soup.find_all(['a'])
    external_links = filter_links(external_links)
    title = soup.find('title')
    title = filter_title(title)
    title_words = get_words_from_h1(h1_tags)
    return {'title':title,'url': url, 'h1': h1_tags, 'words': title_words, 'links': external_links}

def salva_dados(data, file):
    print('SCRAPPING URL: ', data['url'])
    for key in data:
        if key == 'url':
            file.write(key.upper() + ': ' + data[key] + '\n')
            continue
        elif key == 'title':
            file.write(key.upper() + ': ' + data[key] + '\n')
            continue
        file.write(key.upper() + ': \n')
        for item in data[key]:
            file.write("---" + item + '\n')


def verify_nltk():
    try:
        stemmer = SnowballStemmer('portuguese')
        stemmer = SnowballStemmer('english')
    except:
        nltk.download('SnowballStemmer')
    try:
        stopwords.words('portuguese')
        stopwords.words('english')
    except:
        nltk.download('stopwords')

def main():
    verify_nltk()
    global STOP
    thread_stopper = threading.Thread(target=stop_scrapping_timer)
    thread_printer = threading.Thread(target=printTime)
    file = open('data/data.txt', 'w', encoding='utf_8')
    file_json = open('data/data_json.txt', 'w', encoding='utf_8')
    #file_json.write('[\n')
    queue = [url]
    queue_set = set()
    queue_set.add(url)
    thread_stopper.start()
    #thread_printer.start()
    while not STOP:
        current_url = queue.pop(0)
        #queue_set.remove(current_url)
        try:
            data = get_html(current_url)
        except:
            continue
        salva_dados(data, file)
        file_json.write(json.dumps(data) + ',\n')
        file.write('--------------------------------------------------------------------\n\n')
        file.write('\n')
        for link in data['links']:
            if link not in queue_set:
                queue.append(link)
                queue_set.add(link)
        #queue.extend(data['links'])
        if len(queue) == 0:
            print("SCRAPPING FINISHED")
            break
    #remove a ultima virgula do arquivo json
    file_json.seek(file_json.tell() - 3, 0)
    #file_json.write('\n]')
    file.close()
    file_json.close()
    print("END")


main()