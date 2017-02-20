from Crypto.Cipher import AES

KEY = 'YELLOW SUBMARINE'
IV = KEY.encode('hex').upper()

with open('7.txt', 'r') as f:
    base64_encoded_input = ''.join(f.readlines())

ciphertext = base64_encoded_input.decode('base64')
aes_obj = AES.new(KEY, AES.MODE_ECB, IV=IV)
plaintext = aes_obj.decrypt(ciphertext)

print plaintext
