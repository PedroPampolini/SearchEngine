class WordListNode:
    def __init__(self, word:str, addr:int):
        self.word = word
        self.addr = addr
    def to_dict(self):
        return {'word': self.word, 'addr': self.addr}
    def dict_types():
        return {'word': str, 'addr': int}