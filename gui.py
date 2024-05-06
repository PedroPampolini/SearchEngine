from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout,QHBoxLayout, QLabel, QLineEdit, QScrollArea
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QIcon, QDesktopServices
from PyQt5.QtWidgets import QDesktopWidget
import sys
import requests
from bs4 import BeautifulSoup
from ObjectStream import ObjectStreamReader
from models.WordListNode import WordListNode
from models.UrlLinkedListNode import UrlLinkedListNode
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Search Engine'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()
        self.search_engine = Search_Engine()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.center()
        self.layout = self.buildLayout()
       
        self.show()

    def buildLayout(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        self.setLayout(layout)
        self.search_header = QHBoxLayout()

        self.scroll_area_layout = QVBoxLayout()
        self.scroll_area_layout.setAlignment(Qt.AlignTop)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget(self.scroll_area)
        self.scroll_content.setLayout(self.scroll_area_layout)
        self.scroll_area.setWidget(self.scroll_content)

        self.search_bar = QLineEdit()
        self.search_button = QPushButton('Search')
        self.search_button.clicked.connect(self.search)
        self.search_header.addWidget(self.search_bar)
        self.search_header.addWidget(self.search_button)
        layout.addLayout(self.search_header)
        layout.addWidget(self.scroll_area)
        return layout
    

    def search(self):
        search_text = self.search_bar.text()
        urls = self.search_engine.search_phrase(search_text)
        self.show_results(urls)

    def show_results(self,results):
        # limpa os resultados anteriores
        for i in reversed(range(self.scroll_area_layout.count())):
            widget = self.scroll_area_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
                
        for result in results:
            result_widget = ResultWidget(result['title'], result['url'])
            self.scroll_area_layout.addWidget(result_widget)

        self.scroll_area.update()

    def GetSiteTitle(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.find('title')
        if title is None:
            return url
        return title.text

    def buildResultWidget(self, name, url):
        widget = QWidget()
        layout = QVBoxLayout()
        name = QLabel()
        url = QLabel()
        layout.addWidget(name)
        layout.addWidget(url)
        widget.setLayout(layout)
        return widget

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

class ResultWidget(QWidget):
    def __init__(self, term, url):
        super().__init__()
        self.term = term
        self.url = url
        self.init_ui()

    def init_ui(self):
        # Crie um layout vertical
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        # Adicione um QLabel para o termo
        term_label = QLabel(self.term)
        layout.addWidget(term_label)

        url_label = QLabel(f'<a href="{self.url}">{self.url}</a>')
        url_label.setOpenExternalLinks(True)
        url_label.setTextInteractionFlags(Qt.TextBrowserInteraction)
        layout.addWidget(url_label)

        self.setLayout(layout)

    def open_url(self):
        # Abra a URL no navegador da web padrão
        QDesktopServices.openUrl(QUrl(self.url))


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
        print(urls)
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



if __name__ == '__main__':
    app = QApplication([])
    ex = App()
    sys.exit(app.exec_())