class WordListNode:
    '''Classe que possui um ponteiro para o primeiro item de uma lista de UrlLinkedListNode, dado uma palavra'''
    def __init__(self, word:str, addr:int):
        self.word = word
        self.addr = addr
    def to_dict(self):
        ''''Converte o WordListNode em um dicionário'''
        return {'word': self.word, 'addr': self.addr}
    def dict_types():
        '''Retorna um dicionário com os tipos dos atributos do WordListNode'''
        return {'word': str, 'addr': int}