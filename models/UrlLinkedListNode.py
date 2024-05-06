class UrlLinkedListNode:
    def __init__(self, url:str, title:str, prio:int, next:int):
        self.url = url
        self.prio = prio
        self.title = title
        self.next = next
    def to_dict(self):
        return {'title':self.title,'url': self.url, 'prio': self.prio, 'next': self.next}
    def dict_types():
        return {'title':str,'url': str, 'prio':int, 'next': int}