import os

INT_SIZE = 8
ENCODING = 'UTF-8'
ENCODING_LIST = ['UTF-8', 'ISO-8859-1', 'ISO-8859-15', 'ASCII', 'UTF-16', 'UTF-32']
class ObjectStreamWriter:
    '''Classe que escreve um objeto em um arquivo binário.
    Deve sesr entregue o objeto em forma de dicionário e os tipos de cada um dos atributos que serão escritos, por exemplo:
    -> obj = {\'name\':\'John\', \'age\': 25}
    -> types = {\'name\':str, \'age\':int}
    '''
    #-------------------------------------------------------------------------------#

    def __init__(self, fileName):
        self.fileName = fileName
        self.file = open(fileName, 'wb')
        self.__sizeof_int = INT_SIZE
    
    def write(self, obj:dict, types:dict):
        '''Escreve um objeto no arquivo binário. Faz uma verificação de cada tipo para ter um método específico de escrita para cada tipo.
        Os tipos suportados são int e str a princípio.'''
        obj_type_match = self.__verify_types(obj, types)
        if (not obj_type_match):
            raise TypeError('Types do not match')
        for key in obj:
            if types[key] == int:
                self.__write_int(obj[key])
            elif types[key] == str:
                self.__write_string(obj[key])
            else:
                raise TypeError('Type not supported: key=' + str(key) + str(types[key]))
        
    def __write_int(self, value:int):
        '''Escreve um inteiro no arquivo binário. É colocada uma marcação com \'i\' para sinalizar que é de tipo inteiro.
        O inteiro é escrito em 8 bytes.'''
        self.file.write(b'i')
        self.file.write(value.to_bytes(self.__sizeof_int, byteorder='big'))

    def __write_string(self, value:str):
        '''Escreve uma string no arquivo binário. É colocada uma marcação com \'s\' para sinalizar que é de tipo string.
        É utilizado o encoding UTF-8 para escrever a string. A string é terminada com um byte nulo (\'\0\').'''
        self.file.write(b's')
        self.file.write(value.encode(ENCODING))
        self.file.write(b'\0')

    def __verify_types(self, obj:dict, types:dict) -> bool:
        '''Verifica se os tipos dos atributos do objeto estão de acordo com os tipos esperados.
        Ver possibilidade de retirar a necessidade de passar os tipos como parâmetro,
        pois posso apenas verificar o tipo de cada atributo do objeto.'''
        for key in obj:
            if key not in types:
                raise TypeError(f'Key {key} not expected')
            if types[key] != type(obj[key]):
                raise TypeError(f'Key {key} has wrong type')
        return True
    
    def seek(self, offset, whence=0):
        '''Posiciona o ponteiro de leitura/escrita do arquivo na posição desejada.'''
        self.file.seek(offset, whence)

    def size(self):
        '''Retorna o tamanho do arquivo.'''
        self.file.seek(0, 2)
        return self.file.tell()

    def close(self):
        '''Fecha o arquivo.'''
        self.file.close()

class ObjectStreamReader:
    '''Classe que lê um objeto de um arquivo binário.
    Deve ser entregue os tipos de cada um dos atributos que serão lidos, por exemplo:
    -> types = {\'name\':str, \'age\':int}
    '''
    def __init__(self, fileName):
        self.fileName = fileName
        self.file = open(fileName, 'rb')
        self.__sizeof_int = INT_SIZE

    def read(self, types:dict) -> dict:
        '''Lê um objeto do arquivo binário. Faz uma verificação de cada tipo para ter um método específico de leitura para cada tipo.
        Os tipos suportados são int e str a princípio.'''

        # verifica se o arquivo está vazio
        if self.file.read(1) == b'':
            return None
        self.file.seek(-1, 1)
        obj = {}
        for key in types:
            if types[key] == int:
                obj[key] = self.__read_int()
            elif types[key] == str:
                obj[key] = self.__read_string()
            else:
                raise TypeError('Type not supported: key=' + str(key) + str(types[key]))
        return obj

    def __read_int(self) -> int:
        '''Faz a leitura de 9 bytes que representam um inteiro. Se o primeiro byte,
        que é uma marcação do tipo inteiro, não for igual a \'i\', lança uma exceção de typeError.'''
        if self.file.read(1) != b'i':
            raise TypeError('Type does not match')
        return int.from_bytes(self.file.read(self.__sizeof_int), byteorder='big')

    def __read_string(self) -> str:
        '''Inicia a leitura de uma string, até o caractere \\0. Se o primeiro byte, que é uma marcação do tipo string,
        não for igual a \'s\', lança uma exceção de typeError. Tenta realizar a leitura de um caractere dado uma lista de Encodings,
        Retirar isso em atualizações futuras'''
        if self.file.read(1) != b's':
            raise TypeError('Type does not match')
        string = ''
        while True:
            char = self.file.read(1)
            if char == b'\0' or char == b'':
                break
            try:
                string += char.decode(ENCODING)
            except UnicodeDecodeError:
                for encoding in ENCODING_LIST:
                    try:
                        string += char.decode(encoding)
                        break
                    except UnicodeDecodeError:
                        pass
        return string
    
    def seek(self, offset, whence=0):
        '''Posiciona o ponteiro de leitura/escrita do arquivo na posição desejada.'''
        self.file.seek(offset, whence)

    def size(self):
        '''Retorna o tamanho do arquivo.'''
        self.file.seek(0, 2)
        return self.file.tell()

    def close(self):
        '''Fecha o arquivo.'''
        self.file.close()

class ObjectStreamAppender:
    '''Classe que lê e escreve um objeto em um arquivo binário.
    Deve ser entregue os tipos de cada um dos atributos que serão lidos, por exemplo:
    -> types = {\'name\':str, \'age\':int}
    '''
    def __init__(self, fileName):
        self.fileName = fileName
        self.file = None
        self.__sizeof_int = INT_SIZE
        if os.path.exists(fileName):
            self.file = open(fileName, 'r+b')
        else:
            # cria o arquivo se ele não existir
            self.file = open(fileName, 'wb')
            self.file.close()
            self.file = open(fileName, 'r+b')
        

    def read(self, types:dict) -> dict:
        '''Lê um objeto do arquivo binário. Faz uma verificação de cada tipo para ter um método específico de leitura para cada tipo.
        Os tipos suportados são int e str a princípio.'''

        # verifica se o arquivo está vazio
        if self.file.read(1) == b'':
            return None
        self.file.seek(-1, 1)
        obj = {}
        for key in types:
            if types[key] == int:
                obj[key] = self.__read_int()
            elif types[key] == str:
                obj[key] = self.__read_string()
            else:
                raise TypeError('Type not supported: key=' + str(key) + str(types[key]))
        return obj

    def __read_int(self) -> int:
        '''Faz a leitura de 9 bytes que representam um inteiro. Se o primeiro byte,
        que é uma marcação do tipo inteiro, não for igual a \'i\', lança uma exceção de typeError.'''
        if self.file.read(1) != b'i':
            raise TypeError('Type does not match')
        return int.from_bytes(self.file.read(self.__sizeof_int), byteorder='big')
    
    def __read_string(self) -> str:
        '''Inicia a leitura de uma string, até o caractere \\0. Se o primeiro byte, que é uma marcação do tipo string,
        não for igual a \'s\', lança uma exceção de typeError. Tenta realizar a leitura de um caractere dado uma lista de Encodings,
        Retirar isso em atualizações futuras.'''
        if self.file.read(1) != b's':
            raise TypeError('Type does not match')
        string = ''
        while True:
            char = self.file.read(1)
            if char == b'\0' or char == b'':
                break
            try:
                string += char.decode(ENCODING)
            except UnicodeDecodeError:
                for encoding in ENCODING_LIST:
                    try:
                        string += char.decode(encoding)
                        break
                    except UnicodeDecodeError:
                        pass
        return string
    

    def write(self, obj:dict, types:dict):
        '''Escreve um objeto no arquivo binário. Faz uma verificação de cada tipo para ter um método específico de escrita para cada tipo.
        Os tipos suportados são int e str a princípio.'''

        obj_type_match = self.__verify_types(obj, types)
        if (not obj_type_match):
            raise TypeError('Types do not match')
        for key in obj:
            if types[key] == int:
                self.__write_int(obj[key])
            elif types[key] == str:
                self.__write_string(obj[key])
            else:
                raise TypeError('Type not supported: key=' + str(key) + str(types[key]))
        
    def __write_int(self, value:int):
        '''Escreve um inteiro no arquivo binário. É colocada uma marcação com \'i\' para sinalizar que é de tipo inteiro.
        O inteiro é escrito em 8 bytes.'''
        self.file.write(b'i')
        self.file.write(value.to_bytes(self.__sizeof_int, byteorder='big'))

    def __write_string(self, value:str):
        '''Escreve uma string no arquivo binário. É colocada uma marcação com \'s\' para sinalizar que é de tipo string.
        É utilizado o encoding UTF-8 para escrever a string. A string é terminada com um byte nulo (\'\0\').'''
        self.file.write(b's')
        self.file.write(value.encode(ENCODING))
        self.file.write(b'\0')

    def __verify_types(self, obj:dict, types:dict) -> bool:
        '''Verifica se os tipos dos atributos do objeto estão de acordo com os tipos esperados.
        Ver possibilidade de retirar a necessidade de passar os tipos como parâmetro,
        pois posso apenas verificar o tipo de cada atributo do objeto.'''

        for key in obj:
            if key not in types:
                raise TypeError(f'Key {key} not expected')
            if types[key] != type(obj[key]):
                raise TypeError(f'Key {key} has wrong type')
        return True
    
    def seek(self, offset, whence=0):
        '''Posiciona o ponteiro de leitura/escrita do arquivo na posição desejada.'''
        return self.file.seek(offset, whence)

    def size(self):
        '''Retorna o tamanho do arquivo.'''
        self.file.seek(0, 2)
        return self.file.tell()

    def close(self):
        '''Fecha o arquivo.'''
        self.file.close()