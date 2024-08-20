import json
import sys

class Enigma:

    #constructor for the enigma
    def __init__(self, hash_map, wheels, reflector_map):
        self.hash_map = hash_map
        self.wheels = wheels
        self.reflector_map = reflector_map

    def encrypt(self, message):
        final_message = ''
        return final_message
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
    if 'hash_map' not in dictionary or 'wheels' not in dictionary or 'reflector_map' not in dictionary:
        raise JSONFileError
    return Enigma(dictionary['hash_map'], dictionary['wheels'], dictionary['reflector_map'])

if __name__ == '__main__':
    #Getting the flags from the shell
    args_dict = {}
    for i in range(1, len(sys.argv), 2):
        if sys.argv[i] != '-c' and sys.argv[i] != '-i' and sys.argv[i] != '-o':
            sys.stderr.write("Usage: python3 enigma.py -c <config_file> -i <input_file> -o <output_file>")
            exit(1)
        args_dict[sys.argv[i]] = sys.argv[i + 1]
    try:
        #loading the message to encrypt
        enigma = load_enigma_from_path(args_dict['-c'])
        lines_to_encrypt = []
        with open(args_dict['-i'], 'r') as f_in:
            for line in f_in:
                lines_to_encrypt.append(line)
        #printing to -o or to the common printing
        if '-o' in args_dict:
            with open(args_dict['-o'], 'w') as f_out:
                for line in lines_to_encrypt:
                    f_out.write(enigma.encrypt(line))
        else:
            for line in lines_to_encrypt:
                print(enigma.encrypt(line))
    except Exception:
        sys.stderr.write("The enigma script has encountered an error")
        exit(1)