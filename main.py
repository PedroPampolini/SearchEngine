import time
from ObjectStream import ObjectStreamReader
from models.WordListNode import WordListNode
from models.UrlLinkedListNode import UrlLinkedListNode
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords
import sys


wa_osr = ObjectStreamReader("data/word_list.bin")
ull_osr = ObjectStreamReader("data/url_linked_list.bin")

def search_word_in_index(word:str) -> list:
    inicial_addr = -1
    wa_osr.seek(0) #vai para o início do arquivo para começar a busca
    while True:
        current_obj = wa_osr.read(WordListNode.dict_types())
        if current_obj == None:
            break
        if current_obj['word'] == word:
            inicial_addr = current_obj['addr']
            break
    if inicial_addr == -1:
        print("Palavra não encontrada")
        return []
    ull_osr.seek(inicial_addr)
    urls = []
    while True:
        current_obj = ull_osr.read(UrlLinkedListNode.dict_types())
        if current_obj == None:
            break
        urls.append(current_obj['url'])
        if current_obj['next'] == 0:
            break
        ull_osr.seek(current_obj['next'])
    return urls

def search_word(word):
    pt_stemmer = SnowballStemmer('portuguese')
    en_stemmer = SnowballStemmer('english')
    stemmed_words = []
    stemmed_words.append(pt_stemmer.stem(word))
    stemmed_words.append(en_stemmer.stem(word))
    words = [word for word in stemmed_words if word]
    urls = []
    for word in words:
        
            urls.extend(search_word_in_index(word))

    return list(set(urls))


def intersect_lists(lists):
    lists
    if not lists:
        return []
    result = lists[0]
    for l in lists:
        if not l:
            continue
        if len(l) == 0:
            continue
        result = list(set(result) & set(l))
    return result

def search_phrase(phrase):
    words = phrase.split()
    #remove stopwords
    stop_words = set(stopwords.words('english') + stopwords.words('portuguese'))
    words = [word for word in words if word not in stop_words]
    urls = []
    for word in words:
        urls.append(search_word(word))
    return intersect_lists(urls)
    return list(set(urls))

def main():
    initTime = time.time()
    searchType = ''
    if len(args) == 2:
        searchType = 'ONE_WORD'
        print(search_word(args[1]))
    elif len(args) > 2:
        searchType = 'PHRASE'
        phrase = ' '.join(args[1:])
        print(search_phrase(phrase))
    else:
        searchType = 'DEFAULT'
        print(search_word("expect"))
    finalTime = time.time()
    print(searchType, "->Tempo de execução: ", finalTime - initTime, "segundos")


args = sys.argv

if __name__ == "__main__":
    main()

