from Crypto.PublicKey import RSA as rsa
from Crypto.Cipher import PKCS1_OAEP
from base64 import b64encode, b64decode

def gen_key(keylen = 2048):
    key_pair = []
    for i in range(0, 4):
        n = rsa.generate(keylen)
        key_pair.append([n.publickey().exportKey(), n.exportKey()])        #generates 4 public key / private key pairs and returns them
    return key_pair

def encrypt(message, pukey):
    pukey_ = []
    for i in pukey:
        a = rsa.import_key(i)
        pukey_.append(a)
    encryptor = []
    for i in pukey_:
        encryptor.append(PKCS1_OAEP.new(i))
    
    encmessage = []
    
    encmessage.append(encryptor[0].encrypt(message))
    encmessage[0] = b64encode(encmessage[0])
    ct = encmessage[0].decode()
    length_ct = len(ct)
    encmessage[0] = ct[:int(length_ct/3)]                         # first 1/3 of CT
    encmessage.append(ct[int(length_ct/3):int(length_ct*2/3)])    # second 1/3 of CT
    encmessage.append(ct[int(length_ct*2/3):])                    # third 1/3 of CT

    encmessage[0] = encryptor[1].encrypt(encmessage[0].encode())
    encmessage[1] = encryptor[2].encrypt(encmessage[1].encode())
    encmessage[2] = encryptor[3].encrypt(encmessage[2].encode())
    final_ct = b''
    for i in range(3):
        encmessage[i] = b64encode(encmessage[i])
        final_ct = final_ct+encmessage[i]+b'\n'
    return final_ct

def decrypt(message, prkey):
    prkey_ = []
    
    for i in prkey:
        a = rsa.import_key(i)
        prkey_.append(a)
    decryptor = []
    for i in prkey_:
        decryptor.append(PKCS1_OAEP.new(i))
    message = message.split(b'\n')
    message.pop()
    for i in range(len(message)):
        message[i] = b64decode(message[i])

    for i in range(1, len(decryptor)):
        message[i-1] = decryptor[i].decrypt(message[i-1])
    
    message = message[0]+message[1]+message[2]
    message = b64decode(message)
    message = decryptor[0].decrypt(message)

    return message
    
def main():

    input('This file is not intended to be executed by the user. Press any key to exit.')

if __name__ == '__main__':
    main()