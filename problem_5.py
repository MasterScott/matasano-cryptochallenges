def xor_encrypt(key, text):
    xored = []
    for idx, ch in enumerate(text):
        xored.append(chr(ord(key[idx % len(key)]) ^ ord(ch)))
    return ''.join(xored)


if __name__ == '__main__':
    correct_xored = ["0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f"]
    texts = ["Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"]
    key = "ICE"
    for i, text in enumerate(texts):
        xored_text = xor_encrypt(key, text)
        print xored_text.encode('hex')
        print correct_xored[i]
