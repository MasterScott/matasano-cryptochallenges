from Crypto.Cipher import AES
from math import ceil
from struct import pack

BLOCKSIZE = 16


class InvalidPaddingError(Exception):
    '''Custom exception to handle cases of invalid PKCS#7 padding.'''
    pass


def break_to_blocks(text, blocksize):
    return [text[i*blocksize:(i+1)*blocksize] for i in range(len(text)/blocksize)]


def apply_pkcs_7_padding(plaintext, blocksize=BLOCKSIZE):
    padding_length = blocksize - len(plaintext) % blocksize
    pad = chr(padding_length)
    return ''.join((plaintext, pad*padding_length))


def remove_pkcs_7_padding(plaintext):
    pad_start = -ord(plaintext[-1])
    if len(set(plaintext[pad_start:])) == 1:
        return plaintext[:pad_start]
    raise InvalidPaddingError('Invalid PKCS#7 padding')


def cbc_aes_encrypt(plaintext, iv, key, blocksize=BLOCKSIZE):
    aes_obj = AES.new(key)

    plaintext = apply_pkcs_7_padding(plaintext, blocksize)
    plain_blocks = break_to_blocks(plaintext, blocksize)
    xor_block = iv
    encrypted_blocks = []
    for plain_block in plain_blocks:
        xored_block = ''.join([chr(ord(plain_block[i]) ^ ord(xor_block[i])) for i in range(blocksize)])

        encrypted_block = aes_obj.encrypt(xored_block)
        encrypted_blocks.append(encrypted_block)

        xor_block = encrypted_block
    return ''.join(encrypted_blocks)


def cbc_aes_decrypt(ciphertext, iv, key, blocksize=BLOCKSIZE):
    aes_obj = AES.new(key)

    cipher_blocks = [ciphertext[i*blocksize:(i+1)*blocksize] for i in range(len(ciphertext)/blocksize)]
    cipher_blocks = break_to_blocks(ciphertext, blocksize)
    xor_block = iv

    plain_blocks = []
    for cipher_block in cipher_blocks:
        xored_block = aes_obj.decrypt(cipher_block)

        plain_block = ''.join([chr(ord(xored_block[i]) ^ ord(xor_block[i])) for i in range(blocksize)])
        plain_blocks.append(plain_block)

        xor_block = cipher_block
    return remove_pkcs_7_padding(''.join(plain_blocks))


def ecb_aes_encrypt(text, key, blocksize=BLOCKSIZE):
    aes_obj = AES.new(key)

    text = apply_pkcs_7_padding(text, blocksize)
    blocks = break_to_blocks(text, blocksize)
    cleared_blocks = []
    for block in blocks:
        cleared_block = aes_obj.encrypt(block)
        cleared_blocks.append(cleared_block)
    return ''.join(cleared_blocks)


def ecb_aes_decrypt(ciphertext, key, blocksize=BLOCKSIZE):
    aes_obj = AES.new(key)
    plaintext = aes_obj.decrypt(ciphertext)
    return remove_pkcs_7_padding(plaintext)


def ctr_aes(text, key, nonce, nonce_format, counter_format, blocksize=BLOCKSIZE):
    aes_obj = AES.new(key)
    input_block_num = int(ceil(len(text)/float(blocksize)))
    keystream = ''
    for counter in range(input_block_num):
        plain_keystream_block = ''.join((
            pack(nonce_format, nonce),
            pack(counter_format, counter)
        ))
        encrypted_keystream_block = aes_obj.encrypt(plain_keystream_block)
        keystream += encrypted_keystream_block
    output = ''.join([chr(ord(keystream[i]) ^ ord(text[i])) for i in range(len(text))])
    return output
