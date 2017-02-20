from Crypto.Cipher import AES


def cbc_aes_encrypt(plaintext, iv, key):
    aes_obj = AES.new(key)

    plain_blocks = [plaintext[i*len(iv):(i+1)*len(iv)] for i in range(len(plaintext)/len(iv))]
    xor_block = iv
    encrypted_blocks = []
    for plain_block in plain_blocks:
        xored_block = ''.join([chr(ord(plain_block[i]) ^ ord(xor_block[i])) for i in range(len(plain_block))])

        encrypted_block = aes_obj.encrypt(xored_block)
        encrypted_blocks.append(encrypted_block)

        xor_block = encrypted_block
    return ''.join(encrypted_blocks)


def cbc_aes_decrypt(ciphertext, iv, key):
    aes_obj = AES.new(key)

    cipher_blocks = [ciphertext[i*len(iv):(i+1)*len(iv)] for i in range(len(ciphertext)/len(iv))]
    xor_block = iv

    plain_blocks = []
    for cipher_block in cipher_blocks:
        xored_block = aes_obj.decrypt(cipher_block)

        plain_block = ''.join([chr(ord(xored_block[i]) ^ ord(xor_block[i])) for i in range(len(xored_block))])
        plain_blocks.append(plain_block)

        xor_block = cipher_block
    return ''.join(plain_blocks)


if __name__ == '__main__':
    IV = '\x00'*16
    KEY = 'YELLOW SUBMARINE'

    with open('10.txt', 'r') as f:
        ciphertext = ''.join(f.readlines()).decode('base64')

    print cbc_aes_decrypt(ciphertext, IV, KEY)
