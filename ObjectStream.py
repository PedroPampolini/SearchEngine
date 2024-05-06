import os

INT_SIZE = 8
ENCODING = 'UTF-8'
ENCODING_LIST = ['UTF-8', 'ISO-8859-1', 'ISO-8859-15', 'ASCII', 'UTF-16', 'UTF-32']
class ObjectStreamWriter:
    def __init__(self, fileName):
        self.fileName = fileName
        self.file = open(fileName, 'wb')
        self.__sizeof_int = INT_SIZE
    

    def write(self, obj:dict, types:dict):
        obj_type_match = self.__verify_types(obj, types)
        if (not obj_type_match):
            raise TypeError('Pedro: Types do not match')
        for key in obj:
            if types[key] == int:
                self.__write_int(obj[key])
            elif types[key] == str:
                self.__write_string(obj[key])
            else:
                raise TypeError('Pedro: Type not supported: key=' + str(key) + str(types[key]))
        
    def __write_int(self, value:int):
        self.file.write(b'i')
        self.file.write(value.to_bytes(self.__sizeof_int, byteorder='big'))

    def __write_string(self, value:str):
        self.file.write(b's')
        self.file.write(value.encode(ENCODING))
        self.file.write(b'\0')

    def __verify_types(self, obj:dict, types:dict) -> bool:
        for key in obj:
            if key not in types:
                raise TypeError(f'Pedro: Key {key} not expected')
            if types[key] != type(obj[key]):
                raise TypeError(f'Pedro: Key {key} has wrong type')
        return True
    
    def seek(self, offset, whence=0):
        self.file.seek(offset, whence)

    def size(self):
        self.file.seek(0, 2)
        return self.file.tell()

    def close(self):
        self.file.close()

class ObjectStreamReader:
    def __init__(self, fileName):
        self.fileName = fileName
        self.file = open(fileName, 'rb')
        self.__sizeof_int = INT_SIZE

    def read(self, types:dict) -> dict:
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
                raise TypeError('Pedro: Type not supported: key=' + str(key) + str(types[key]))
        return obj

    def __read_int(self) -> int:
        if self.file.read(1) != b'i':
            raise TypeError('Pedro: Type does not match')
        return int.from_bytes(self.file.read(self.__sizeof_int), byteorder='big')

    def __read_string(self) -> str:
        if self.file.read(1) != b's':
            raise TypeError('Pedro: Type does not match')
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
        self.file.seek(offset, whence)

    def size(self):
        self.file.seek(0, 2)
        return self.file.tell()

    def close(self):
        self.file.close()

class ObjectStreamAppender:
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
                raise TypeError('Pedro: Type not supported: key=' + str(key) + str(types[key]))
        return obj

    def __read_int(self) -> int:
        if self.file.read(1) != b'i':
            raise TypeError('Pedro: Type does not match')
        return int.from_bytes(self.file.read(self.__sizeof_int), byteorder='big')
    
    def __read_string(self) -> str:
        if self.file.read(1) != b's':
            raise TypeError('Pedro: Type does not match')
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
        obj_type_match = self.__verify_types(obj, types)
        if (not obj_type_match):
            raise TypeError('Pedro: Types do not match')
        for key in obj:
            if types[key] == int:
                self.__write_int(obj[key])
            elif types[key] == str:
                self.__write_string(obj[key])
            else:
                raise TypeError('Pedro: Type not supported: key=' + str(key) + str(types[key]))
        
    def __write_int(self, value:int):
        self.file.write(b'i')
        self.file.write(value.to_bytes(self.__sizeof_int, byteorder='big'))

    def __write_string(self, value:str):
        self.file.write(b's')
        self.file.write(value.encode(ENCODING))
        self.file.write(b'\0')

    def __verify_types(self, obj:dict, types:dict) -> bool:
        for key in obj:
            if key not in types:
                raise TypeError(f'Pedro: Key {key} not expected')
            if types[key] != type(obj[key]):
                raise TypeError(f'Pedro: Key {key} has wrong type')
        return True
    
    def seek(self, offset, whence=0):
        return self.file.seek(offset, whence)

    def size(self):
        self.file.seek(0, 2)
        return self.file.tell()

    def close(self):
        self.file.close()