from Crypto.Cipher import AES


def ecb_aes(text, key, blocksize):
    aes_obj = AES.new(key)
    blocks = [text[i*blocksize:(i+1)*blocksize] for i in range(len(text)/blocksize)]
    cleared_blocks = []
    for block in blocks:
        cleared_block = aes_obj.decrypt(block)
        cleared_blocks.append(cleared_block)
    return ''.join(cleared_blocks)


if __name__ == '__main__':
    KEY = 'YELLOW SUBMARINE'
    BLOCKSIZE = 16

    with open('7.txt', 'r') as f:
        base64_encoded_input = ''.join(f.readlines())

    ciphertext = base64_encoded_input.decode('base64')
    plaintext = ecb_aes(ciphertext, KEY, BLOCKSIZE)

    print plaintext
