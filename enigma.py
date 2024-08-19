import json

class Enigma:

    #constructor for the enigma
    def __init__(self, hash_map, wheels, reflector_map):
        self.hash_map = hash_map
        self.wheels = wheels
        self.reflector_map = reflector_map

    def encrypt(self, message):
        #Todo: add code

#Function outside the class, gets source to json file, and returns fitting enigma,
#In case something went wrong, exception will be raised.

class JSONFileError(Exception):
    def __init__(self):
        super().__init__()

def load_enigma_from_path(path):
    try:
        with open(path, 'r') as f:
            dictionary = json.load(f)
    except Exception:
        raise JSONFileError
    if 'rotators' not in dictionary or 'wheels' not in dictionary or 'reflectors' not in dictionary:
        raise JSONFileError
    return Enigma(dictionary['rotators'], dictionary['wheels'], dictionary['reflector'])
