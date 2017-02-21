from crypto_library import cbc_aes_encrypt, ecb_aes, BLOCKSIZE
from string import printable
import random


def generate_random_string(length):
    return ''.join(random.choice(printable) for _ in range(length))


def cbc_encryption(plaintext, key):
    iv = generate_random_string(BLOCKSIZE)
    return cbc_aes_encrypt(plaintext, iv, key)


def ecb_encryption(plaintext, key):
    return ecb_aes(plaintext, key)


def encryption_oracle(plaintext):
    encryption_schemes = [cbc_encryption, ecb_encryption]

    key = generate_random_string(16)

    padding_before = generate_random_string(random.randrange(5, 11))
    padding_after = generate_random_string(random.randrange(5, 11))

    ciphertext = encryption_schemes[random.randrange(0, 2)](''.join((padding_before, plaintext, padding_after)), key)

    return ciphertext


def distinguish_encryption_mode(ciphertext):
    blocks = [ciphertext[i*BLOCKSIZE:(i+1)*BLOCKSIZE] for i in range(len(ciphertext)/BLOCKSIZE)]
    if len(blocks) < 4:
        return 'Insufficient input'
    if blocks[1] == blocks[2]:
        return 'ecb'
    return 'cbc'


def main():
    plaintext = '0'*100

    ciphertext = encryption_oracle(plaintext)
    adversary_output = distinguish_encryption_mode(ciphertext)

    print adversary_output


if __name__ == '__main__':
    main()
