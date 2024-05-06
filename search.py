import time
from ObjectStream import ObjectStreamReader
from models.WordListNode import WordListNode
from models.UrlLinkedListNode import UrlLinkedListNode
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords
import sys


class Search_Engine():
    def __init__(self) -> None:
        self.wa_osr = ObjectStreamReader("data/word_list.bin")
        self.ull_osr = ObjectStreamReader("data/url_linked_list.bin")

    def search_word_in_index(self,word:str) -> list:
        inicial_addr = -1
        self.wa_osr.seek(0) #vai para o início do arquivo para começar a busca
        while True:
            current_obj = self.wa_osr.read(WordListNode.dict_types())
            if current_obj == None:
                break
            if current_obj['word'] == word:
                inicial_addr = current_obj['addr']
                break
        if inicial_addr == -1:
            print("Palavra não encontrada")
            return []
        self.ull_osr.seek(inicial_addr)
        urls = []
        while True:
            current_obj = self.ull_osr.read(UrlLinkedListNode.dict_types())
            if current_obj == None:
                break
            urls.append(current_obj)
            if current_obj['next'] == 0:
                break
            self.ull_osr.seek(current_obj['next'])
        return urls

    def search_word(self,word):
        pt_stemmer = SnowballStemmer('portuguese')
        en_stemmer = SnowballStemmer('english')
        stemmed_words = []
        stemmed_words.append(pt_stemmer.stem(word))
        stemmed_words.append(en_stemmer.stem(word))
        words = [word for word in stemmed_words if word]
        urls = []
        for word in words:
            urls.extend(self.search_word_in_index(word))
        #print(urls)
        return self.remove_duplicates(urls)
    
    def remove_duplicates(self,urls):
        urls_read = set()
        result = []
        for url in urls:
            if url['url'] not in urls_read:
                urls_read.add(url['url'])
                result.append(url)
        return result


    def intersect_lists(self,lists):
        if not lists:
            return []
        result = lists[0]
        for l in lists:
            if not l:
                continue
            if len(l) == 0:
                continue
            result = self.intersect(result, l)#list(set(result) & set(l))
        return result

    def intersect(self,l1,l2):
        result = []
        for i in l1:
            for j in l2:
                if i['url'] == j['url']:
                    result.append(i)
                    break
        return result

    def search_phrase(self,phrase:str):
        words = phrase.split()
        #remove stopwords
        stop_words = set(stopwords.words('english') + stopwords.words('portuguese'))
        words = [word for word in words if word not in stop_words]
        urls = []
        for word in words:
            urls.append(self.search_word(word))
        return self.intersect_lists(urls)

def main():
    searchEngine = Search_Engine()
    initTime = time.time()
    searchType = ''
    if len(args) == 2:
        searchType = 'ONE_WORD'
        print(searchEngine.search_word(args[1]))
    elif len(args) > 2:
        searchType = 'PHRASE'
        phrase = ' '.join(args[1:])
        print(searchEngine.search_phrase(phrase))
    else:
        searchType = 'DEFAULT'
        print(searchEngine.search_word("expect"))
    finalTime = time.time()
    print(searchType, "->Tempo de execução: ", finalTime - initTime, "segundos")


args = sys.argv

if __name__ == "__main__":
    main()

