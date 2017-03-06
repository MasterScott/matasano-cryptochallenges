from problem_12 import new_encryption_oracle, find_blocksize
import random
from string import printable

RANDOM_PREFIX = ''.join(random.choice(printable) for _ in range(random.randrange(0, 20)))
# print len(RANDOM_PREFIX)


def oracle(adversary_input):
    return new_encryption_oracle(RANDOM_PREFIX + adversary_input)


def find_oracle_added_length(blocksize):
    adversary_input = ''
    previous_length = len(oracle(adversary_input))
    while True:
        adversary_input += '0'
        current_length = len(oracle(adversary_input))
        if current_length > previous_length:
            return current_length - len(adversary_input) - blocksize


def find_padding_length(blocksize):
    adversary_input = '0'*64
    zero_encrypted_block = oracle(adversary_input)[2*blocksize:3*blocksize]
    change_counter = 1
    while True:
        adversary_input = change_counter*'1' + '0'*(64-change_counter)
        current_second_block = oracle(adversary_input)[2*blocksize:3*blocksize]
        if current_second_block != zero_encrypted_block:
            return 2*blocksize - change_counter + 1
        change_counter += 1


def find_single_ecb_character(blocksize, decrypted, start_padding_length, unknown_text_length):
    bypass_start_padding = '0'*(2*blocksize - start_padding_length)
    input_padding = bypass_start_padding + '0'*(blocksize*(unknown_text_length/blocksize + 1) - len(decrypted) - 1)
    test_padding = input_padding + decrypted
    block_position = (len(test_padding) - len(bypass_start_padding))/blocksize

    ciphertext = oracle(input_padding)[2*blocksize:]
    cipher_blocks = [ciphertext[i*blocksize:(i+1)*blocksize] for i in range(len(ciphertext)/blocksize)]

    for test_char in printable:
        test_character = test_padding + test_char

        test_character_ciphertext = oracle(test_character)[2*blocksize:]
        test_blocks = [test_character_ciphertext[i*blocksize:(i+1)*blocksize] for i in range(len(test_character_ciphertext)/blocksize)]

        if test_blocks[block_position] == cipher_blocks[block_position]:
            return test_char


if __name__ == '__main__':
    blocksize = find_blocksize(oracle)

    oracle_added_length = find_oracle_added_length(blocksize)
    start_padding_length = find_padding_length(blocksize)
    unknown_text_length = oracle_added_length - start_padding_length

    decrypted = ''
    while len(decrypted) < unknown_text_length:
        decrypted += find_single_ecb_character(blocksize, decrypted, start_padding_length, unknown_text_length)
    print decrypted.decode('base64')
