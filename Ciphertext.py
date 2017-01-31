class CipherText:
    def __init__(self, ctext):
        self.ciphertext = ctext
        self.asciitext = self.decodeHex()
    
    def decodeHex(self):
        try:
            return [ord(c) for c in self.ciphertext.decode('hex')]
        except:
            raise
    
    def getContentChar(self):
        return self.asciitext
