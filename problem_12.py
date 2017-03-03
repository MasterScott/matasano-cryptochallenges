from crypto_library import ecb_aes
from problem_11 import distinguish_encryption_mode
from string import printable
'''
from crypto_library import BLOCKSIZE
import random

ENCRYPTION_KEY = ''.join(random.choice(printable) for _ in range(BLOCKSIZE))
'''


def new_encryption_oracle(adversary_input):
    ENCRYPTION_KEY = ',y!3<CWn@1?wwF]\x0b'
    unknown_input = 'Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK'
    return ecb_aes(adversary_input+unknown_input, ENCRYPTION_KEY)


def find_blocksize(oracle):
    adversary_input = ''
    previous_length = len(oracle(adversary_input))
    found_block_change = False
    while True:
        adversary_input += '0'
        current_length = len(oracle(adversary_input))
        if current_length > previous_length:
            if found_block_change:
                return current_length - previous_length
            found_block_change = True
            previous_length = current_length


def find_unknown_text_length(blocksize):
    adversary_input = ''
    previous_length = len(new_encryption_oracle(adversary_input))
    while True:
        adversary_input += '0'
        current_length = len(new_encryption_oracle(adversary_input))
        if current_length > previous_length:
            return current_length - len(adversary_input) - blocksize


def find_single_ecb_character(blocksize, decrypted, unknown_text_length):
    input_padding = '0'*(blocksize*(unknown_text_length/blocksize + 1) - len(decrypted) - 1)
    test_padding = input_padding + decrypted
    block_position = len(test_padding)/blocksize

    for test_char in printable:
        test_character = test_padding + test_char

        test_character_ciphertext = new_encryption_oracle(test_character)
        test_blocks = [test_character_ciphertext[i*blocksize:(i+1)*blocksize] for i in range(len(test_character_ciphertext)/blocksize)]

        ciphertext = new_encryption_oracle(input_padding)
        cipher_blocks = [ciphertext[i*blocksize:(i+1)*blocksize] for i in range(len(ciphertext)/blocksize)]

        if test_blocks[block_position] == cipher_blocks[block_position]:
            return test_char


if __name__ == '__main__':
    blocksize = find_blocksize(new_encryption_oracle)
    unknown_text_length = find_unknown_text_length(blocksize)

    chosen_input = '0'*(3*blocksize)
    detection_ciphertext = new_encryption_oracle(chosen_input)
    encryption_mode = distinguish_encryption_mode(detection_ciphertext)
    if encryption_mode == 'ecb':
        decrypted = ''
        while len(decrypted) < unknown_text_length:
            decrypted += find_single_ecb_character(blocksize, decrypted, unknown_text_length)
        print decrypted.decode('base64')
