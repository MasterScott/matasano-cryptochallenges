from english_frequencies import score_text
from string import printable


with open('4.txt', 'r') as f:
    inputs = f.readlines()

decoded_inputs = [i.strip('\n').decode('hex') for i in inputs]

scores = {}
for en, plain_input in enumerate(decoded_inputs):
    for l in printable:
        decrypted_test_output = ''.join([chr(ord(l) ^ ord(i)) for i in plain_input])
        scores[(l, plain_input)] = (decrypted_test_output, score_text(decrypted_test_output))

sorted_score_items = sorted(scores.items(), key=lambda x: x[1][1])
print sorted_score_items[-1][1][0]
