import json

def write_JSON(data, name):
    with open(name, 'w') as outfile:
        json.dump(data, outfile, indent=4, ensure_ascii=False)

def read_JSON(name):
    with open(name, 'r') as readfile:
        data = json.load(readfile)
    return data

def read_keys_AES():
    print("read AES keys!")

def write_AES_keys(list_dicts):
    final_dict = {
        'key 0' : list_dicts[0],
        'key 1' : list_dicts[1],
        'key 2' : list_dicts[2],
        'key 3' : list_dicts[3]
    }
    write_JSON(final_dict, 'private_AES.json')

def write_keys_list(keys, name = 'public_key.json', n = 3):  # public or private key as a bool(0 = Public, 1 = Private), keys as a list
    data = {}                                 # Takes a list of bytes as input.
    data['keys'] = []
    for i in range(0, n+1, 1):
        data['keys'].append({
            'key '+ str(i): keys[i].decode()
        })

    write_JSON(data, name)

def read_message(filename):  # name of file as a string
    file1 = open(filename, 'r')
    message = file1.read()
    file1.close()
    return message

def write_message(message, fname):
    with open(fname, 'w') as file:
        file.write(message.decode())

def read_keys_list(name = 'public_key.json'): # reads keys from json file   (0 = Public key file, 1 = Private key file)
                                              #gives a list of strings as outputs.
    key_list = []
    data = read_JSON(name)
    for i,j in zip(data['keys'], range(0, 4)):
        key_list.append(i['key ' + str(j)])

    return key_list


def main():
    input('This file is not intended to be executed by the user. Press any key to exit.')

if __name__ == '__main__':
    main()
