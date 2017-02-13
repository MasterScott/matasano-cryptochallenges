import sys

hex_string = sys.argv[1]
print hex_string.decode('hex').encode('base64')
