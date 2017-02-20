from collections import defaultdict


def score_ECB_ciphertext(ciphertext):
    blocks = [ciphertext[i*16:(i+1)*16] for i in range(len(ciphertext)/16)]
    block_counts = defaultdict(int)
    for b in blocks:
        block_counts[b] += 1
    return len(blocks) - len(block_counts)


if __name__ == '__main__':
    with open('8.txt', 'r') as f:
        hex_encoded_ciphertexts = f.readlines()

    ciphertexts = [i.strip('\n').decode('hex') for i in hex_encoded_ciphertexts]
    scored_ciphertexts = {}
    for c in ciphertexts:
        scored_ciphertexts[c] = score_ECB_ciphertext(c)
    sorted_scored_ciphertexts = sorted(scored_ciphertexts.items(), key=lambda x: x[1], reverse=True)
    print sorted_scored_ciphertexts[0]
