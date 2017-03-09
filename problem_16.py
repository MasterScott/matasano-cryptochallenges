import random
from string import printable
from crypto_library import cbc_aes_encrypt, cbc_aes_decrypt
from urllib import quote

AES_KEY = ''.join(random.choice(printable) for _ in range(16))
BLOCKSIZE = 16
PREFIX = "comment1=cooking%20MCs;userdata=1"
SUFFIX = ";comment2=%20like%20a%20pound%20of%20bacon"


def encode(plaintext):
    return cbc_aes_encrypt(PREFIX+quote(plaintext)+SUFFIX, AES_KEY, AES_KEY)


def decode(ciphertext):
    return cbc_aes_decrypt(ciphertext, AES_KEY, AES_KEY)


def check_admin(plaintext):
    return ';admin=true;' in plaintext

ciphertext = encode('0'*48)
cipher_blocks = [ciphertext[i*BLOCKSIZE:(i+1)*BLOCKSIZE] for i in range(len(ciphertext)/BLOCKSIZE)]

attack_string = ';admin=true;a='
xored_attack_string = ''.join([chr(ord('0') ^ ord(i)) for i in attack_string])
pad_prefix = '_'*(BLOCKSIZE - len(PREFIX) % BLOCKSIZE)
attack_start = BLOCKSIZE*(len(PREFIX+pad_prefix) / BLOCKSIZE)

cipher_prefix = ciphertext[:attack_start]
cipher_attack = ''.join([chr(ord(ciphertext[i]) ^ ord(xored_attack_string[i-attack_start])) for i in range(attack_start, attack_start+len(xored_attack_string))])
cipher_rest = ciphertext[attack_start+len(xored_attack_string):]

plaintext = decode(cipher_prefix + cipher_attack + cipher_rest)
print 'Ciphertext:', repr(ciphertext)
print 'Plaintext:', repr(plaintext)
print check_admin(plaintext)
