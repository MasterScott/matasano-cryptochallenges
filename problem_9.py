def apply_pkcs_7_padding(plaintext, block_size):
    padding_length = block_size - len(plaintext) % block_size
    pad = chr(padding_length)
    return ''.join((plaintext, pad*padding_length))


if __name__ == '__main__':
    plaintext = 'YELLOW SUBMARINE'
    padded_plaintext = apply_pkcs_7_padding(plaintext, 20)
    print [padded_plaintext]
