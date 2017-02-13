import sys

hex_string_1 = sys.argv[1]
hex_string_2 = sys.argv[2]

input_1 = hex_string_1.decode('hex')
print hex_string_1, input_1
input_2 = hex_string_2.decode('hex')
print hex_string_2, input_2

output = ''.join([chr(ord(a) ^ ord(b)) for a, b in zip(input_1, input_2)])

print output.encode('hex'), output
