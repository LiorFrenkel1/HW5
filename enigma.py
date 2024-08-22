import json
import sys

class Enigma:

    #constructor for the enigma
    def __init__(self, hash_map, wheels, reflector_map):
        self.hash_map = hash_map
        self.wheels = wheels
        self.reflector_map = reflector_map

    def encrypt(self, message):
        inverse_hash_map = {value: key for key, value in self.hash_map.items()}
        hash_map = self.hash_map.copy()
        wheels = self.wheels.copy()
        reflector_map = self.reflector_map.copy()
        final_message = ''
        encryptCounter = 0
        for c in message:
            if c == "\n" :
                final_message += "\n"
            elif c == " " :
                final_message += " "
            else :
                encryptCounter += 1
                i = hash_map[c]
                if (((2 * wheels[0]) - wheels[1] + wheels[2]) % 26) != 0:
                    i += (((2 * wheels[0]) - wheels[1] + wheels[2]) % 26)
                else:
                    i += 1
                i = i % 26
                c1 = inverse_hash_map[i]
                c2 = reflector_map[c1]
                i = hash_map[c2]
                if (((2 * wheels[0]) - wheels[1] + wheels[2]) % 26) != 0:
                    i -= (((2 * wheels[0]) - wheels[1] + wheels[2]) % 26)
                else:
                    i -= 1
                i = i % 26
                c3 = inverse_hash_map[i]
                final_message += c3
            wheels[0] += 1
            if wheels[0] > 8 :
                wheels[0] = 1
            if encryptCounter % 2 == 0:
                wheels[1] *= 2
            else:
                wheels[1] -= 1
            if encryptCounter % 10 == 0:
                wheels[2] = 10
            elif encryptCounter % 3 == 0:
                wheels[2] = 5
            else:
                wheels[2] = 0
        return final_message

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
    isError = False
    for i in range(1, len(sys.argv), 2):
        if sys.argv[i] != '-c' and sys.argv[i] != '-i' and sys.argv[i] != '-o':
            isError = True
        else:
            args_dict[sys.argv[i]] = sys.argv[i + 1]
    if '-c' not in args_dict or '-i' not in args_dict or isError:
        sys.stderr.write("Usage: python3 enigma.py -c <config_file> -i <input_file> -o <output_file>")
        exit(1)
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