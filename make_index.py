import time
from ObjectStream import ObjectStreamWriter, ObjectStreamReader, ObjectStreamAppender
from models.UrlLinkedListNode import UrlLinkedListNode
from models.WordListNode import WordListNode
import json


list_file = "data/word_list.bin"
url_linked_list_file = "data/url_linked_list.bin"
words_addr = dict()


wa_osw = ObjectStreamWriter(list_file)
ull_osr = ObjectStreamAppender(url_linked_list_file)
def write_word(word:str, title:str, url:str):
    global words_addr
    global wa_osw
    global ull_osr
    if word not in words_addr.keys():
        #print("A palavra " + word + " não está no dicionário")
        addr = ull_osr.size()
        word_list_node = WordListNode(word,addr)
        wa_osw.write(word_list_node.to_dict(), WordListNode.dict_types())
        ull_osr.seek(addr)
        ull_osr.write(UrlLinkedListNode(url,title,0,0).to_dict(), UrlLinkedListNode.dict_types())
        words_addr[word] = addr
    else:
        #print("A palavra " + word + " está no dicionário")
        
        word_addr = words_addr[word]
        previous_addr = word_addr
        word_addr
        ull_osr.seek(word_addr)
        ull_osr.file.tell()
        current_obj = ull_osr.read(UrlLinkedListNode.dict_types())
        while current_obj['next'] != 0:
            previous_addr = current_obj['next']
            ull_osr.seek(current_obj['next'])
            current_obj = ull_osr.read(UrlLinkedListNode.dict_types())
        new_addr = ull_osr.size()
        ull_osr = ObjectStreamAppender(url_linked_list_file)
        ull_osr.seek(previous_addr)
        current_obj['next'] = new_addr
        ull_osr.file.tell()
        ull_osr.write(current_obj, UrlLinkedListNode.dict_types())
        ull_osr.file.tell()
        #ull_osr.close()
        ull_osr = ObjectStreamAppender(url_linked_list_file)
        ull_osr.seek(new_addr)
        ull_osr.write(UrlLinkedListNode(url,title,0,0).to_dict(), UrlLinkedListNode.dict_types())

        
        

def main():
    with open(list_file, 'wb') as f:
        pass
    with open(url_linked_list_file, 'wb') as f:
        pass

    json_file = open('data/data_json.txt', 'r', encoding='utf_8')
    size = int(json_file.readline())
    index = 0
    for line in json_file:
        if index % 100 == 0:
            print(f'{round(100 *(float(index)/float(size)),2)}%')        
        line = line[:-1]
        item = eval(line)
        # for item in data:
        title = item['title'] if 'title' in item.keys() else item['url']
        words = item['words']
        url = item['url']
        for word in words:
            write_word(word, title,url)
        index += 1
        
    wa_osw.close()
    ull_osr.close()


initTime = time.time()
main()
finalTime = time.time()

print("Tempo de execução: ", finalTime - initTime)
