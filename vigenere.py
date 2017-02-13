import binascii
from string import printable
from english_frequencies import score_single_characters, score_text

KEYSIZE = [i for i in range(2, 101)]  # The possible keysizes
CANDIDATE_CHECKS = 3  # The number of keysize candidates to check


def calculate_edit_distance(text_a, text_b):
    bitstream_a = int(binascii.hexlify(text_a), 16)
    bitstream_b = int(binascii.hexlify(text_b), 16)
    xored = bin(bitstream_a ^ bitstream_b)
    return sum([1 for i in xored if i == '1'])


def calculate_keysize_distance(text, keysize):
    normalization_factor = 20 if len(text)/keysize >= 20 else len(text)/keysize
    blocks = [(text[i:keysize+i], text[keysize+i:2*keysize+i]) for i in range(0, normalization_factor*keysize, keysize)]
    return sum([calculate_edit_distance(i, j)/float(keysize) for (i, j) in blocks])/float(normalization_factor)


def get_text_blocks(text, keysize):
    return [text[keysize*i:keysize*(i+1)] for i in range(len(text)/keysize + 1)]


def get_transposed_blocks(blocks):
    transposed_blocks = []
    for idx in range(len(blocks[0])):
        bl = []
        for i, b in enumerate(blocks):
            try:
                bl.append(b[idx])
            except IndexError:
                if i != len(blocks) - 1:
                    assert("Incorrect block")
        transposed_blocks.append(''.join(bl))
    return transposed_blocks


def decrypt_single_xored_text(text):
    scores = {}
    for l in printable:
        decrypted_text = ''.join([chr(ord(l) ^ ord(i)) for i in text])
        scores[(l, text)] = (decrypted_text, score_single_characters(decrypted_text))

    sorted_score_items = sorted(scores.items(), key=lambda x: x[1][1])
    return sorted_score_items[-1][1][0]


def get_decrypted_blocks(blocks):
    return [decrypt_single_xored_text(b) for b in blocks]


def recreate_trasposed_text(transposed_blocks):
    valid_text = ''
    for idx in range(len(transposed_blocks[0])):
        for b in transposed_blocks:
            try:
                valid_text += b[idx]
            except IndexError:
                if idx != len(transposed_blocks) - 1:
                    assert("Incorrect block")
    return valid_text


def solve_repeating_key_xor(text):
    keysize_distances = {}
    for keysize in KEYSIZE:
        keysize_distances[keysize] = calculate_keysize_distance(text, keysize)
    sorted_keysizes = sorted(keysize_distances.items(), key=lambda x: x[1])
    possible_keysizes = sorted_keysizes[:CANDIDATE_CHECKS]

    possible_solutions = {}
    for keysize, _ in possible_keysizes:
        blocks = get_text_blocks(text, keysize)
        transposed_blocks = get_transposed_blocks(blocks)
        decrypted_blocks = get_decrypted_blocks(transposed_blocks)
        recreated_text = recreate_trasposed_text(decrypted_blocks)
        possible_solutions[keysize] = recreated_text

    correct_solution = sorted(possible_solutions.items(), key=lambda x: score_text(x[1]), reverse=True)[0][1]
    return correct_solution
