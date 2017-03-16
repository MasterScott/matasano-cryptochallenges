from crypto_library import ctr_aes

blocksize = 16
key = 'YELLOW SUBMARINE'
nonce = 0
nonce_format = '<q'
counter_format = '<Q'
ciphertext = 'L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ=='.decode('base64')
print repr(ctr_aes(ciphertext, key, nonce, nonce_format, counter_format, blocksize))
