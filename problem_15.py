from crypto_library import remove_pkcs_7_padding, InvalidPaddingError


valid = 'ICE ICE BABY\x04\x04\x04\x04'
invalid_1 = 'ICE ICE BABY\x05\x05\x05\x05'
invalid_2 = 'ICE ICE BABY\x01\x02\x03\x04'

try:
    print remove_pkcs_7_padding(valid)
except InvalidPaddingError:
    print 'Invalid padding:', repr(valid)
try:
    print remove_pkcs_7_padding(invalid_1)
except InvalidPaddingError:
    print 'Invalid padding:', repr(invalid_1)
try:
    print remove_pkcs_7_padding(invalid_2)
except InvalidPaddingError:
    print 'Invalid padding:', repr(invalid_2)
