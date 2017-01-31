class VigenereVerifier:
    def __init__(self, ciphercontent, key):
        self.ciphercontent = ciphercontent
        
        self.plaincontent = []
        self.encodedcontent = []
        
        self.key = key
    
    def __decode(self):
        self.plaincontent = []
        posKey = 0
        for el in self.ciphercontent:
            decoded = el ^ self.key[posKey]
            posKey = (posKey + 1) % len(self.key)
            self.plaincontent.append(decoded)
    
    def __encode(self):
        if(len(self.plaincontent) == 0):
            return None
        self.encodedcontent = []
        
        posKey = 0
        for el in self.plaincontent:
            encoded = el ^ self.key[posKey]
            posKey = (posKey + 1) % len(self.key)
            self.encodedcontent.append(encoded)
    
    def verify(self):
        self.__decode()
        self.__encode()
        
        return self.encodedcontent == self.ciphercontent
    
    def getPlainContent(self):
        return self.plaincontent
