class UrlLinkedListNode:
    '''Classe que representa um nó de uma lista ligada, dentro do nó contém informações sobre a URL'''
    def __init__(self, url:str, title:str, prio:int, next:int):
        self.url = url
        self.prio = prio
        self.title = title
        self.next = next
    def to_dict(self):
        '''Converte o UrlLinkedListNode em um dicionário'''
        return {'title':self.title,'url': self.url, 'prio': self.prio, 'next': self.next}
    def dict_types():
        '''Retorna um dicionário com os tipos dos atributos do UrlLinkedListNode'''
        return {'title':str,'url': str, 'prio':int, 'next': int}