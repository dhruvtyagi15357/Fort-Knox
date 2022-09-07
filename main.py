import read_write as rw
import cryptRSA as rsaa
import cryptAES as aess
def line(l = 80):
    print('_' * l)

def intro():
    print('''Instructions on how to use the program:
    
    NOTE 1: MAKE SURE THAT YOU DO NOT CHANGE THE FILE NAME AFTER KEY GENERATION OR ENCRYPTION OF THE FILE.
    NOTE 2: If the program is unable to encrypt the text file, change the file's name's length by 1 character and grnerate new keys to proceed with the encryption. 
    NOTE 3: Make sure to remove the keys/passwords from the program's directory and store them at a secure place if required.

0.) Make sure that the files required by the program are in the same directory as the program.
1.) view a file:
	To view a file, just type in the file name and the file content will be displayed on the screen.
2.) Get / Generate keys:
	When requested, enter the name of file you want to use the keys for.
	If the length of file name is odd, You will be prompted to enter 4 passwords that you want to use for key and stored in the file password.json.
	If the length of file name is even, The program will take some time and generate public and private key pairs that are stored in public_key.json and private_key.json respectively.
	You may send the public_key.json to the sender of the message so that he can encrypt the plain text file.
3.) Encrypt a file:
	When requested, enter the name of file you want to use the keys for.
	If the length of file name is odd, you need to make sure that the file named password.json is present in the same directory and contains the passwords that you want to encrypt your file with.
	If the length of file name is even, make sure that the file named public_key.json is present in the same directory and contains the recievers public keys.
4.) Decrypt file:
	When requested, enter the name of file you want to use the keys for.
	If the length of file name is odd, you need to make sure that the files named password.json and private_AES.json are present in the same directory and contains the passwords and salts, nonces and tags that were used while encrypting the file.
	If the length of file name is even, make sure that the file named private_key.json is present in the same directory and contains the recievers private keys.
''')

def main():
    exit = False
    while not exit:
        print('0.) Introduction to the application')
        print('1.) View a file')
        print('2.) Get/Generate keys')
        print('3.) Encrypt file')
        print('4.) Decrypt file')
        print('9.) EXIT')
        option = int(input("Select an option: "))
        
        if option == 9:
            exit = True

        elif option == 0:
            line()        
            intro()
            line()
        
        elif option == 1:
            fname = input("Enter the file name: ")
            print('BEGINNING OF MESSAGE')
            line()
            message = rw.read_message(fname)
            print(message)
            line()
            print('ENDING OF MESSAGE')
        
        elif option == 2:
            fname = input("Enter the file name: ")
            if len(fname) % 2 == 0:
                keypairs = rsaa.gen_key()
                public_keys = []
                private_keys = []
                for i in keypairs:
                    public_keys.append(i[0])
                    private_keys.append(i[1])

                rw.write_keys_list(public_keys)
                rw.write_keys_list(private_keys, name = 'private_key.json')
                print('Public keys stored in the file public_key.json')
                print('Private keys stored in the file private_key.json')

            else:
                passwords = aess.get_passwords()
                rw.write_keys_list(keys = passwords, name = 'password.json')
                print('Passwords stored in the file password.json')
            


        elif option == 3:
            fname = input("Enter the file name: ")
            if len(fname) % 2 == 0:
                pukey = rw.read_keys_list()
                message = rw.read_message(fname).encode()
                message = rsaa.encrypt(message, pukey)
                rw.write_message(message, fname)
            else:
                passwords = rw.read_keys_list('password.json')
                message = rw.read_message(fname)
                dictionary = aess.encrypt(message, passwords)
                rw.write_message(dictionary[0].encode(), fname)
                dictionary.pop(0)
                rw.write_AES_keys(dictionary)
            print('Message encrypted successfully!')
        
        elif option == 4:
            fname = input("Enter the file name: ")
            if len(fname) % 2 == 0:
                prkey = rw.read_keys_list('private_key.json')
                message = rw.read_message(fname).encode()
                message = rsaa.decrypt(message, prkey)
                rw.write_message(message, fname)
            else:
                passwords = rw.read_keys_list('password.json')
                cipher_text = rw.read_message(fname)
                dictionary = rw.read_JSON('private_AES.json')
                plain_text = aess.decrypt(cipher_text, passwords, dictionary)
                rw.write_message(plain_text, fname)

            print('Message decrypted successfully!')
        
        else:
            print('Invalid choice')


if __name__ == '__main__':
    main()
    input('Enter any key to exit the program.')