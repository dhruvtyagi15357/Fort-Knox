from base64 import b64encode, b64decode
from hashlib import scrypt
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes

def get_passwords():
    passwords = []
    for i in range(0, 4):
        x = input('Enter password (' + str(i+1) + '/4) : ').encode()
        passwords.append(x)
    return passwords


def encrypt(plain_text, passwords):
    # generate a random salt
    salts = []
    private_keys = []
    ciphers = []
    tags = []
    for i in range(0, 4):
        salts.append(get_random_bytes(AES.block_size))
        # use the Scrypt KDF to get a private key from the password
        private_keys.append(scrypt(passwords[i].encode(), salt=salts[i], n=2**14, r=8, p=1, dklen=32))
        # create cipher config
        ciphers.append(AES.new(private_keys[i], AES.MODE_GCM))
        
    cipher_text, tag = ciphers[0].encrypt_and_digest(bytes(plain_text, 'utf-8'))
    cipher_text = b64encode(cipher_text).decode('utf-8')
    tags.append(tag)
    length = len(cipher_text)
    ct1 = cipher_text[:int(1/3 * length)]
    ct2 = cipher_text[int(1/3 * length):int(2/3 * length)]
    ct3 = cipher_text[int(2/3 * length):]

    ct1, tag = ciphers[1].encrypt_and_digest(bytes(ct1, 'utf-8'))
    tags.append(tag)
    ct1 = b64encode(ct1).decode('utf-8')
    
    ct2, tag = ciphers[2].encrypt_and_digest(bytes(ct2, 'utf-8'))
    tags.append(tag)
    ct2 = b64encode(ct2).decode('utf-8')

    ct3, tag = ciphers[3].encrypt_and_digest(bytes(ct3, 'utf-8'))
    tags.append(tag)
    ct3 = b64encode(ct3).decode('utf-8')


    cipher_text = ct1 + '\n' + ct2 + '\n' + ct3
    list_enc_dict = [cipher_text]

    for i in range(0, 4):
        list_enc_dict.append({
            'salt' : b64encode(salts[i]).decode('utf-8'),
            'nonce' : b64encode(ciphers[i].nonce).decode('utf-8'),
            'tag' : b64encode(tags[i]).decode('utf-8')
        })

    return list_enc_dict

def decrypt(cipher_text, passwords, enc_dict):
    # decode the dictionary entries from base64
    cipher_texts = cipher_text.split('\n')
    for i in range(0, len(cipher_texts)):
        cipher_texts[i] = b64decode(cipher_texts[i])

    salts = []
    nonces = []
    tags = []
    private_keys = []
    ciphers = []
    for i in range(0, 4):
        nonces.append(b64decode(enc_dict['key ' + str(i)]['nonce']))
        salts.append(b64decode(enc_dict['key ' + str(i)]['salt']))
        tags.append(b64decode(enc_dict['key ' + str(i)]['tag']))
        # generate the private key from the password and salt
        private_keys.append(scrypt(passwords[i].encode(), salt=salts[i], n=2**14, r=8, p=1, dklen=32))
        # create the cipher config
        ciphers.append(AES.new(private_keys[i], AES.MODE_GCM, nonce=nonces[i]))

    pt1 = ciphers[1].decrypt_and_verify(cipher_texts[0], tags[1])
    pt2 = ciphers[2].decrypt_and_verify(cipher_texts[1], tags[2])
    pt3 = ciphers[3].decrypt_and_verify(cipher_texts[2], tags[3])

    cipher_text = pt1+pt2+pt3
    cipher_text = b64decode(cipher_text)

    final_plain_text = ciphers[0].decrypt_and_verify(cipher_text, tags[0])

    return final_plain_text

def main():
    input('This file is not intended to be executed by the user. Press any key to exit.')

if __name__ == '__main__':
    main()