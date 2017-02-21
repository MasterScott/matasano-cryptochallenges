from Crypto.Cipher import AES

BLOCKSIZE = 16


def apply_pkcs_7_padding(plaintext, blocksize=BLOCKSIZE):
    padding_length = blocksize - len(plaintext) % blocksize
    pad = chr(padding_length)
    return ''.join((plaintext, pad*padding_length))


def cbc_aes_encrypt(plaintext, iv, key, blocksize=BLOCKSIZE):
    aes_obj = AES.new(key)

    plaintext = apply_pkcs_7_padding(plaintext, blocksize)
    plain_blocks = [plaintext[i*blocksize:(i+1)*blocksize] for i in range(len(plaintext)/blocksize)]
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
    xor_block = iv

    plain_blocks = []
    for cipher_block in cipher_blocks:
        xored_block = aes_obj.decrypt(cipher_block)

        plain_block = ''.join([chr(ord(xored_block[i]) ^ ord(xor_block[i])) for i in range(blocksize)])
        plain_blocks.append(plain_block)

        xor_block = cipher_block
    return ''.join(plain_blocks)


def ecb_aes(text, key, blocksize=BLOCKSIZE):
    aes_obj = AES.new(key)

    text = apply_pkcs_7_padding(text, blocksize)
    blocks = [text[i*blocksize:(i+1)*blocksize] for i in range(len(text)/blocksize)]
    cleared_blocks = []
    for block in blocks:
        cleared_block = aes_obj.decrypt(block)
        cleared_blocks.append(cleared_block)
    return ''.join(cleared_blocks)