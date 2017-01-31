import json,sys,os
import ConfigParser
from Language import Language
from Ciphertext import CipherText
from VigenereCracker import VigenereCracker
from VigenereVerifier import VigenereVerifier

def loadFrequency(jsoncontent):
    FREQUENCY = {}
    if not "letters" in jsoncontent:
        raise
    for letter in jsoncontent["letters"]:
        try:
            FREQUENCY[int(letter["letter"])] = float(letter["value"])
        except:
            raise
    return FREQUENCY

def displayLanguage(AVAILABLE_LANG):
    print "## Available language ##"
    for key, value in AVAILABLE_LANG.items():
        print key+":"+value


if __name__ == '__main__':
    Config = ConfigParser.ConfigParser()
    try:
        Config.read("Config.ini")
    except:
        print("No Config file found in the directory")
        exit(-1)
    if "LANGDIRECTORY" not in Config.sections():
        print("Missing LANGDIRECTORY section")
        exit(-1)
    if "AVAILABLELANG" not in Config.sections():
        print("Missing AVAILABLELANG section")
        exit(-1)
        
    _LANGDIR_ = Config.get("LANGDIRECTORY", "PATH")
    AVAILABLE_LANG = dict(s.split('-') for s in filter(None,Config.get("AVAILABLELANG", "LANGS").split(",")))
    
    
    if len(sys.argv) != 5:
        print("usage: ciphertextpath twolettercodelanguage minlenkey maxlenkey")
        exit(-1)    
    if not os.path.exists(sys.argv[1]) or not os.path.isfile(sys.argv[1]):
        print("Incorrect ciphertext filename")
        exit(-1)
    if len(sys.argv[2]) != 2 or str(sys.argv[2]).upper() not in AVAILABLE_LANG.keys():
        print("Incorrect language code")
        displayLanguage(AVAILABLE_LANG)
        exit(-1)
    if not str(sys.argv[3]).isdigit() or not str(sys.argv[4]).isdigit():
        print("Incorrect bounds")
        exit(-1)
    
    _minbound = int(sys.argv[3])
    _maxbound = int(sys.argv[4])
    
    if(_minbound > _maxbound):
        print("Incorrect bounds: minbounds must be lower than equal maxbounds")
        exit(-1)
    
    _filename = sys.argv[1]
    
    _langcode = str(sys.argv[2]).upper()
    _langdescription = AVAILABLE_LANG[str(sys.argv[2]).upper()]
    
    _selectedLanguage = None
    try:
        _selectedLanguage = Language(_langcode,_langdescription)
        _selectedLanguage.setLetterFrequency(loadFrequency(json.load(open(os.path.join(_LANGDIR_,"".join(["FREQ_",_langcode,".json"]))))))
    except:
        print("Problem in loading language "+_langcode)
        exit(-1) 
     
    _ciphertext = None    
    try:
        _ciphertext = CipherText(open(_filename,'rb').read())
    except:
        print("Problem in loading ciphertext")
        exit(-1)
    
    
    cracker = VigenereCracker(_selectedLanguage, _minbound, _maxbound)
    cracker.setContent(_ciphertext.getContentChar())
    
    ########## FIND KEY ###########
    _MYKEY = cracker.FoundKey()
    _KEYLENGTHFOUND = cracker.getKeyLen()
    ###############################

    
    ########## VERIFY KEY ###########
    verifier = VigenereVerifier(_ciphertext.getContentChar(),_MYKEY)
    if verifier.verify():
        print "Key length: "+str(_KEYLENGTHFOUND)
        print "Key: "+str(_MYKEY)
        print "".join(str(chr(el)) for el in verifier.getPlainContent())
    else:
        print "No Key founded"
    #################################
