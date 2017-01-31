class VigenereCracker:
    def __init__(self, language, minLen, maxLen):
        self.LANGUAGE = language
        
        #Key length could be from 1 to 13 bytes
        self.KEYLENBOUNDS = range(minLen,maxLen)
        
        self.SUMQPSQUARE = 0.065
        
        self.KEYLENGTHFOUND = -1
        self.KEY = []
        self.CONTENT = None
    
    def setContent(self, _content):
        self.CONTENT = _content
    
    def reset(self):
        self.KEYLENGTHFOUND = -1
        self.CONTENT = None
        self.KEY = []
        
    def __FoundKeyLen(self):
        if not self.CONTENT:
            return None
        
        _KEYLENDICT_ = {}
        for i in self.KEYLENBOUNDS:
            retChar = self.takeCharEveryKPos(0, i, self.CONTENT)
            mapChar = self.countOccurrenceAndFrequency(retChar)
            _KEYLENDICT_[i] = mapChar
        _kMAX = -1
        _sumQsquareMAX = 0
        for k in _KEYLENDICT_:
            _val = self.computeSumQiSquare(_KEYLENDICT_[k])
            if _val > _sumQsquareMAX:
                _sumQsquareMAX = _val
                _kMAX = k
        
        self.KEYLENGTHFOUND = _kMAX
        return _kMAX
    
    def getKeyLen(self):
        return self.KEYLENGTHFOUND
    def FoundKey(self):
        if not self.CONTENT:
            return None
        
        self.__FoundKeyLen()
        if self.KEYLENGTHFOUND == -1:
            return None
        
        for i in range(self.KEYLENGTHFOUND):
            _resultsDecrypt = {}
            
            _firstTryCrypt = self.takeCharEveryKPos(i, self.KEYLENGTHFOUND, self.CONTENT)
            for tryK in range(1,256):
                _resultsDecrypt[tryK] = []
                for el in _firstTryCrypt:
                    _resultsDecrypt[tryK].append(el ^ tryK)
            
            _candidateDecrypt = {}
            for tryK in _resultsDecrypt:
                if self.verifyDecrypt(_resultsDecrypt[tryK]):
                    _candidateDecrypt[tryK] = _resultsDecrypt[tryK]

            _maximizeK = 0
            _maximizeSum = 0
            for candidateK in _candidateDecrypt:
                _map = self.countOccurrenceAndFrequency(_candidateDecrypt[candidateK])
                _val = self.computeSumQPiSquareLowerCaseLetter(_map)
                if abs(_val - self.SUMQPSQUARE) < abs(_maximizeSum - self.SUMQPSQUARE):
                    _maximizeK = candidateK
                    _maximizeSum = _val
            
            self.KEY.append(_maximizeK)
        
        return self.KEY
    
    def takeCharEveryKPos(self, start_pos, k_pos, content):
        _Index = start_pos
    
        _retChars = []
        _retChars.append(content[_Index])
    
        _Index+=k_pos
        while _Index < len(content):
            _retChars.append(content[_Index])
            _Index+=k_pos
    
        return _retChars
    
    def countOccurrenceAndFrequency(self, content):
        _map = {}
        for value in content:
            if not value in _map:
                _map[value] = {'Occurence':0,'Frequency':0}
            _map[value]['Occurence'] += 1
        
        for value in _map:
            _map[value]['Frequency'] = float(_map[value]['Occurence'])/len(content)*1.0
        return _map
    
    def computeSumQiSquare(self, _map):
        _sum = float(0.0)
        for el in _map:
            _q = _map[el]['Frequency']
            _qsquare = _q * _q
            _sum += _qsquare
        return _sum
    
    def computeSumQPiSquareLowerCaseLetter(self,_map):
        _sum = float(0.0)
        for el in _map:
            if self.LANGUAGE.containsLetter(el):
                _q = _map[el]['Frequency']
                _qsquare = _q * self.LANGUAGE.getFrequency(el)
                _sum += _qsquare
        return _sum
    
    def verifyDecrypt(self, content):
        for el in content:
            if el < 32 or el > 127:
                return False
            return True
