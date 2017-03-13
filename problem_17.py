import random
from string import printable
from crypto_library import cbc_aes_encrypt, cbc_aes_decrypt, InvalidPaddingError, remove_pkcs_7_padding


class Oracle(object):
    def __init__(self):
        self.key = ''.join(random.choice(printable) for _ in range(16))
        self.input_list = [
            'MDAwMDAwTm93IHRoYXQgdGhlIHBhcnR5IGlzIGp1bXBpbmc=',
            'MDAwMDAxV2l0aCB0aGUgYmFzcyBraWNrZWQgaW4gYW5kIHRoZSBWZWdhJ3MgYXJlIHB1bXBpbic=',
            'MDAwMDAyUXVpY2sgdG8gdGhlIHBvaW50LCB0byB0aGUgcG9pbnQsIG5vIGZha2luZw==',
            'MDAwMDAzQ29va2luZyBNQydzIGxpa2UgYSBwb3VuZCBvZiBiYWNvbg==',
            'MDAwMDA0QnVybmluZyAnZW0sIGlmIHlvdSBhaW4ndCBxdWljayBhbmQgbmltYmxl',
            'MDAwMDA1SSBnbyBjcmF6eSB3aGVuIEkgaGVhciBhIGN5bWJhbA==',
            'MDAwMDA2QW5kIGEgaGlnaCBoYXQgd2l0aCBhIHNvdXBlZCB1cCB0ZW1wbw==',
            'MDAwMDA3SSdtIG9uIGEgcm9sbCwgaXQncyB0aW1lIHRvIGdvIHNvbG8=',
            'MDAwMDA4b2xsaW4nIGluIG15IGZpdmUgcG9pbnQgb2g=',
            'MDAwMDA5aXRoIG15IHJhZy10b3AgZG93biBzbyBteSBoYWlyIGNhbiBibG93'
        ]
        self.plaintext = random.choice(self.input_list)
        self.iv = ''.join(random.choice(printable) for _ in range(16))

    def encrypt(self):
        return cbc_aes_encrypt(self.plaintext, self.iv, self.key), self.iv

    def consume(self, ciphertext, iv):
        try:
            cbc_aes_decrypt(ciphertext, iv, self.key)
            return True
        except InvalidPaddingError:
            return False


def decrypt_block(oracle, iv, ciphertext, block_start, blocksize=16):
    is_final_block = block_start == len(ciphertext) - blocksize
    ciphertext = ciphertext[:block_start+blocksize]

    iv_ciphertext = iv + ciphertext
    iv_block_start = block_start + blocksize
    decrypted_suffix = ''
    while len(decrypted_suffix) < 16:
        padding_value = len(decrypted_suffix) + 1

        cipher_prefix = iv_ciphertext[:iv_block_start-len(decrypted_suffix)-1]
        cipher_suffix = ''.join([
            chr(
                padding_value ^
                ord(decrypted_suffix[i]) ^
                ord(iv_ciphertext[iv_block_start-len(decrypted_suffix)+i])
            ) for i in range(len(decrypted_suffix))
        ])
        remaining_cipher = iv_ciphertext[iv_block_start:]

        for test_char_code in range(255, -1, -1):
            cipher_test_char_code = chr(
                test_char_code ^
                ord(iv_ciphertext[iv_block_start-padding_value])
            )
            test_iv_ciphertext = ''.join([
                cipher_prefix,
                cipher_test_char_code,
                cipher_suffix,
                remaining_cipher
            ])
            test_iv = test_iv_ciphertext[:blocksize]
            test_ciphertext = test_iv_ciphertext[blocksize:]
            if oracle.consume(test_ciphertext, test_iv):
                cardinality = test_char_code ^ 1 if (is_final_block and decrypted_suffix == '') else 1  # cardinality helps identify the case when the actual padding of the ciphertext is being decrypted
                solution = cardinality * chr(test_char_code ^ padding_value)
                break
        decrypted_suffix = solution + decrypted_suffix
    return decrypted_suffix


def decrypt_ciphertext(oracle, iv, ciphertext, blocksize=16):
    solution = ''
    for block_start in range(0, len(ciphertext), blocksize):
        solved_block = decrypt_block(oracle, iv, ciphertext, block_start)
        solution += solved_block
    return solution


if __name__ == '__main__':
    blocksize = 16
    oracle = Oracle()
    ciphertext, iv = oracle.encrypt()

    decrypted_plaintext = decrypt_ciphertext(oracle, iv, ciphertext)
    print 'Plaintext:', repr(remove_pkcs_7_padding(decrypted_plaintext))
    print 'Base-64 Decoded:', repr(remove_pkcs_7_padding(decrypted_plaintext).decode('base64'))
