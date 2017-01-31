class Language:
    def __init__(self,code,description):
        self.code = code
        self.description = description
        self.letter = {}
    
    def setLetterFrequency(self, _freq):
        for k,v in _freq.items():
            self.letter[k] = v
    
    def containsLetter(self, el):
        return True if el in self.letter.keys() else False
    
    def getFrequency(self, el):
        return self.letter[el] if self.containsLetter(el) else None
