import sys
from string import ascii_letters
from english_frequencies import score_text

hex_input = sys.argv[1]
decoded_input = hex_input.decode('hex')

scores = {}
for l in ascii_letters + ' ':
    decrypted_test_output = ''.join([chr(ord(l) ^ ord(i)) for i in decoded_input])
    scores[l] = (decrypted_test_output, score_text(decrypted_test_output))
sorted_score_items = sorted(scores.items(), key=lambda x: x[1][1])
print sorted_score_items[-1]
